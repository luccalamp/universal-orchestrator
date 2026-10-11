"""Resolve worker and reviewer models from a session catalog."""

import argparse
import json
import re
import sys
from datetime import datetime, timezone


def _items(value):
    if isinstance(value, dict):
        value = value.get("models", [])
    if not isinstance(value, list):
        raise ValueError("catalog must be a JSON list or an object with a models list")
    return [item for item in value if isinstance(item, dict) and isinstance(item.get("id"), str)]


def parse_catalog(text: str) -> list[dict]:
    """Parse JSON exports or the human-readable model catalog."""
    try:
        data = json.loads(text)
        if isinstance(data, dict) and isinstance(data.get("description"), str):
            data = data["description"]
        else:
            return _items(data)
    except json.JSONDecodeError:
        data = text
    if not isinstance(data, str):
        raise ValueError("catalog description must be text")
    result = []
    # Parse only documented catalog lines; never treat arbitrary source as data.
    pattern = re.compile(r"^\s*-\s+`([^`]+)`\s*:\s*(.*)$")
    for line in data.splitlines():
        match = pattern.match(line)
        if not match:
            continue
        model_id, description = match.groups()
        effort_match = re.search(r"Reasoning efforts?\s*:\s*([^\.\n]+)", description, re.I)
        efforts, default = [], None
        if effort_match:
            for part in effort_match.group(1).split(","):
                effort = re.sub(r"\s*\(default\)\s*", "", part, flags=re.I).strip().lower()
                if "(default)" in part.lower():
                    default = effort
                if re.fullmatch(r"[a-z][a-z0-9_-]*", effort):
                    efforts.append(effort)
        result.append({"id": model_id.strip(), "description": description,
                       "reasoning_efforts": efforts, "default_reasoning_effort": default})
    return result


def _version(model_id):
    return tuple(int(n) for n in re.findall(r"\d+", model_id))


def _family(model_id):
    """Normalize numeric version segments away to group model families."""
    return re.sub(r"[-_.]+", "-", re.sub(r"\d+(?:\.\d+)*", "", model_id.lower())).strip("-_")


def _date(item):
    value = item.get("released_at")
    if not isinstance(value, str):
        return ""
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).isoformat()
    except ValueError:
        return ""


def _effort(item, preferred):
    efforts = item.get("reasoning_efforts")
    if not isinstance(efforts, list):
        efforts = []
    efforts = [str(x).lower() for x in efforts]
    if preferred in efforts:
        return preferred
    if item.get("default_reasoning_effort") in efforts:
        return item["default_reasoning_effort"]
    return efforts[0] if efforts else None


def resolve_models(catalog: list[dict], excluded: list[str] | None = None,
                   worker: str | None = None, reviewer: str | None = None,
                   task_kind: str = "implementation") -> dict:
    excluded_set = set(excluded or [])
    entries = _items(catalog)
    available = []
    for item in entries:
        if item["id"] in excluded_set or item.get("available") is False or item.get("deprecated") is True:
            continue
        available.append(item)
    by_id = {item["id"]: item for item in available}
    for label, override in (("worker", worker), ("reviewer", reviewer)):
        if override is not None and override not in by_id:
            raise ValueError(f"{label} override {override!r} is absent, unavailable, deprecated, or excluded")

    def role_class(item, role):
        desc = str(item.get("description", "")).lower()
        economical = any(s in desc for s in ("affordable", "economical", "cost-efficient", "cost efficient", "low-cost", "low cost", "budget"))
        quick = any(s in desc for s in ("fast", "faster", "quick", "efficient", "low latency", "small"))
        general = any(s in desc for s in ("general", "workhorse", "everyday"))
        advanced = any(s in desc for s in ("advanced", "frontier", "most capable", "complex", "powerful"))
        hint = item["id"].lower()
        # Names are weak hints and never outrank explicit catalog descriptions.
        name_hint = any(t in hint for t in ("luna", "mini", "lite"))
        worker_class = int(economical), int(quick or (not economical and name_hint))
        reviewer_class = int(general or advanced)
        return worker_class if role == "worker" else (reviewer_class,)

    def best_for_role(role):
        # Within each family, role suitability precedes numeric version.
        families = {}
        for item in available:
            key = _family(item["id"])
            families.setdefault(key, []).append(item)
        leaders = [max(group, key=lambda item: role_class(item, role) + (_version(item["id"]), item["id"]))
                   for group in families.values()]

        def cross_family(item):
            desc = str(item.get("description", "")).lower()
            current = int(any(t in desc for t in ("latest", "current")))
            older = int("older" in desc)
            freshness = _date(item)
            metadata = (current, -older, freshness)
            return role_class(item, role) + metadata + (_version(item["id"]), item["id"])

        return max(leaders, key=cross_family) if leaders else None

    def temporal_evidence(item):
        desc = str(item.get("description", "")).lower()
        return (any(t in desc for t in ("latest", "current", "older")) or bool(_date(item)))

    chosen = {}
    for role, override in (("worker", worker), ("reviewer", reviewer)):
        if override:
            chosen[role] = by_id[override]
        elif available:
            chosen[role] = best_for_role(role)
        else:
            chosen[role] = None

    warnings = []
    if not available:
        warnings.append("No eligible catalog models; run locally with the conversation's main model.")
    else:
        family_leaders = {}
        for candidate in available:
            family_leaders.setdefault(_family(candidate["id"]), []).append(candidate)
        if len(family_leaders) > 1:
            leaders = [max(group, key=lambda item: (_version(item["id"]), item["id"]))
                       for group in family_leaders.values()]
            if not any(temporal_evidence(item) for item in leaders):
                warnings.append("Cross-family freshness is uncertain: catalog leaders lack comparable current/older or release-date metadata.")
        for role, item in chosen.items():
            desc = str(item.get("description", "")).lower()
            if role == "worker":
                cost_evidence = any(s in desc for s in ("affordable", "economical", "cost-efficient", "cost efficient", "low-cost", "low cost", "budget"))
                speed_evidence = any(s in desc for s in ("fast", "faster", "quick", "efficient", "low latency", "small"))
                name_hint = any(t in item["id"].lower() for t in ("luna", "mini", "lite"))
                if not cost_evidence and (speed_evidence or name_hint):
                    warnings.append("worker cost suitability is inferred only from speed or a weak family-name hint.")
                elif not cost_evidence and not speed_evidence and not name_hint:
                    warnings.append("worker selection has no clear cost or capability evidence; using stable catalog ranking.")
            elif not any(s in desc for s in ("general", "workhorse", "everyday", "advanced", "frontier", "most capable", "complex", "powerful")):
                warnings.append("reviewer suitability has no clear capability evidence; using stable catalog ranking.")
    worker_effort = _effort(chosen["worker"], "low" if task_kind == "mechanical" else "medium") if chosen["worker"] else None
    reviewer_effort = _effort(chosen["reviewer"], "high") if chosen["reviewer"] else None
    rationale = {role: ({"id": item["id"], "description": item.get("description", ""),
                         "selection": "explicit override" if ((worker if role == "worker" else reviewer) is not None) else "catalog ranking"} if item else None)
                 for role, item in chosen.items()}
    return {"worker": chosen["worker"]["id"] if chosen["worker"] else None,
            "reviewer": chosen["reviewer"]["id"] if chosen["reviewer"] else None,
            "worker_effort": worker_effort, "reviewer_effort": reviewer_effort,
            "head_policy": "conversation model remains unchanged", "warnings": warnings,
            "rationale": rationale}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Resolve models from a catalog")
    parser.add_argument("--catalog", help="catalog file (defaults to stdin)")
    parser.add_argument("--exclude", action="append", default=[])
    parser.add_argument("--worker")
    parser.add_argument("--reviewer")
    parser.add_argument("--task-kind", choices=("mechanical", "implementation"), default="implementation")
    args = parser.parse_args(argv)
    try:
        if args.catalog:
            with open(args.catalog, encoding="utf-8") as stream:
                source = stream.read()
        else:
            source = sys.stdin.read()
        parsed = parse_catalog(source)
        print(json.dumps(resolve_models(parsed, args.exclude, args.worker, args.reviewer, args.task_kind), ensure_ascii=False))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"resolve_models: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
