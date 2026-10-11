"""Fail-closed publication scan of Git-tracked files only (Python 3.10+)."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("private-path", re.compile(r"(?i)(?:\b[A-Z]:[\\/](?:Users|Documents and Settings)[\\/][^\s\"'<>|]+|(?<![\w.])/(?:home|Users|Volumes|mnt|private|root)/[^\s\"'<>|]+)")),
    ("personal-email", re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")),
    ("credential-file", re.compile(r"(?i)(?:^|/)(?:\.env(?:\.[^/]*)?|config\.toml|token[^/]*\.json|[^/]*(?:secret|credential|private[-_.]?config|personal[-_.]?config)[^/]*|id_(?:rsa|ed25519)|[^/]+\.(?:pem|key|p12|pfx))$")),
    ("private-artifact-path", re.compile(r"(?i)(?:^|/)(?:coordination|deliverables|skill-backups|media|cache|__pycache__|\.codex|\.agents|\.cache|\.secrets?)(?:/|$)|\.(?:pyc|pyo|zip|7z|tar|gz|sqlite3?|db|mp4|mov|webm|mp3|wav|png|jpe?g|webp|pdf|pkl)$")),
    ("token", re.compile(r"(?i)\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{20,}|AIza[0-9A-Za-z_-]{30,})\b")),
    ("pem-private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
)


def tracked_entries(root: Path) -> list[tuple[str, str, str, str]]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "--stage", "-z"], cwd=root, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RuntimeError("not a Git repository") from exc
    entries = []
    for record in result.stdout.split(b"\0"):
        if not record:
            continue
        metadata, name = record.split(b"\t", 1)
        mode, object_id, stage = metadata.decode("ascii").split()
        entries.append((name.decode("utf-8", "surrogateescape"), mode, object_id, stage))
    if not entries:
        raise RuntimeError("no tracked files")
    return entries


def findings(root: Path) -> list[tuple[str, str, int]]:
    found: list[tuple[str, str, int]] = []
    for name, mode, object_id, stage in tracked_entries(root):
        if stage != "0":
            found.append((name, "unmerged-index", 1))
            continue
        if mode not in {"100644", "100755"}:
            found.append((name, "non-regular-file", 1))
            continue
        normalized = name.replace("\\", "/")
        for rule, pattern in RULES[2:4]:
            if pattern.search(normalized):
                found.append((name, rule, 1))
        try:
            blob = subprocess.run(
                ["git", "cat-file", "blob", object_id], cwd=root, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            ).stdout
        except (OSError, subprocess.CalledProcessError):
            found.append((name, "unreadable-index-blob", 1))
            continue
        if len(blob) > 256 * 1024 or b"\0" in blob:
            found.append((name, "binary-or-oversized-file", 1))
            continue
        try:
            text = blob.decode("utf-8")
        except UnicodeError:
            found.append((name, "non-utf8-file", 1))
            continue
        for number, line in enumerate(text.splitlines(), 1):
            for rule, pattern in RULES[:2] + RULES[4:]:
                for match in pattern.finditer(line):
                    if rule == "personal-email" and match.group(0).casefold() == "noreply@github.com":
                        continue
                    found.append((name, rule, number))
    return sorted(set(found))


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        results = findings(root)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    for path, rule, line in results:
        print(f"{path}:{rule}:{line}")
    return 1 if results else 0


if __name__ == "__main__":
    raise SystemExit(main())
