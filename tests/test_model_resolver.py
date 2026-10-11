"""Behavioral contract tests for scripts/resolve_models.py (stdlib only)."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "universal-orchestrator" / "scripts" / "resolve_models.py"
CURRENT_CATALOG = Path(__file__).resolve().parent / "fixtures" / "catalog-runtime.txt"


def model(identifier, description, efforts=("low", "medium", "high"), **extra):
    return {"id": identifier, "description": description,
            "reasoning_efforts": list(efforts), **extra}


CATALOG = [
    model("luna-6.2", "Fast and affordable model for easier tasks.", ("low", "medium")),
    model("luna-6.10", "Fast and affordable model for easier tasks.", ("low", "medium", "high")),
    model("nova-1", "Fast, affordable, and efficient model for routine work.", ("low", "medium")),
    model("sol-7.1", "Frontier intelligence for demanding review tasks.", ("low", "medium", "high")),
    model("opaque-x9", "A stable model with no reliable family or speed description.", ("medium",)),
    model("gone-1", "Fast and affordable model.", available=False),
    model("old-1", "Fast and affordable model.", deprecated=True),
    model("blocked-1", "Fast and affordable model."),
]


def load_module():
    if not SCRIPT.is_file():
        raise FileNotFoundError(f"resolver not present: {SCRIPT}")
    spec = importlib.util.spec_from_file_location("resolve_models_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import resolver at {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ModelResolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resolver = load_module()

    def resolve(self, catalog=CATALOG, **kwargs):
        return self.resolver.resolve_models(catalog, **kwargs)

    def test_parse_catalog_text_and_json_forms(self):
        text = "- `luna-current`: Fast and affordable model. Reasoning efforts: low, medium (default), high\n"
        parsed = self.resolver.parse_catalog(text)
        self.assertEqual(parsed[0]["id"], "luna-current")
        self.assertTrue(set(parsed[0].get("reasoning_efforts", [])) >= {"low", "medium", "high"})
        for payload in (CATALOG, {"models": CATALOG}):
            self.assertEqual(len(self.resolver.parse_catalog(json.dumps(payload))), len(CATALOG))
        wrapped_text = json.dumps({"description": "- `wrapped`: Fast and affordable model. Reasoning efforts: low, medium (default)\n"})
        self.assertEqual(self.resolver.parse_catalog(wrapped_text)[0]["id"], "wrapped")

    def test_fast_economical_current_luna_is_executor_and_newer_replaces_old(self):
        result = self.resolve()
        self.assertEqual(result["worker"], "luna-6.10")
        self.assertNotEqual(result["worker"], "luna-6.2")

    def test_future_fast_economical_family_is_eligible_and_sol_reviews(self):
        catalog = [CATALOG[2], CATALOG[3]]
        result = self.resolve(catalog)
        self.assertEqual(result["worker"], "nova-1")
        self.assertEqual(result["reviewer"], "sol-7.1")

    def test_new_economical_family_with_higher_version_beats_present_luna(self):
        catalog = [model("gpt-6-luna", "Fast and affordable model for easier tasks."),
                   model("nova-7.2", "New efficient and economical model for routine tasks.")]
        self.assertEqual(self.resolve(catalog)["worker"], "nova-7.2")

    def test_latest_new_family_beats_unmarked_luna_across_families(self):
        catalog = [model("luna-6.10", "Fast and affordable model for easier tasks."),
                   model("nova-1", "Latest fast affordable model for everyday work.")]
        self.assertEqual(self.resolve(catalog)["worker"], "nova-1")

    def test_economical_model_outranks_premium_fast_model(self):
        catalog = [model("premium-9.9", "Latest fast premium model."),
                   model("nova-1", "Fast affordable model for routine work.")]
        self.assertEqual(self.resolve(catalog)["worker"], "nova-1")

    def test_recent_valid_release_date_beats_old_date_across_families(self):
        catalog = [model("alpha-6.10", "Fast affordable model.", released_at="2024-03-15T12:00:00Z"),
                   model("beta-1", "Fast affordable model.", released_at="2026-09-20T08:30:00Z")]
        self.assertEqual(self.resolve(catalog)["worker"], "beta-1")

    def test_same_family_numeric_successor_beats_older_latest_label(self):
        catalog = [model("nova-6.10", "Latest fast affordable model."),
                   model("nova-7.0", "Fast affordable model.")]
        self.assertEqual(self.resolve(catalog)["worker"], "nova-7.0")

    def test_worker_suitability_precedes_version_within_same_family(self):
        catalog = [model("nova-1", "Fast affordable"),
                   model("nova-2", "Frontier premium"),
                   model("other-1", "Fast premium")]
        self.assertEqual(self.resolve(catalog)["worker"], "nova-1")

    def test_reviewer_suitability_precedes_version_within_same_family(self):
        catalog = [model("judge-1", "Advanced frontier"),
                   model("judge-2", "Fast affordable for easier tasks"),
                   model("other-1", "Fast affordable")]
        self.assertEqual(self.resolve(catalog)["reviewer"], "judge-1")

    def test_real_current_catalog_has_five_models_and_resolves_luna_and_sol(self):
        parsed = self.resolver.parse_catalog(CURRENT_CATALOG.read_text(encoding="utf-8"))
        self.assertEqual(len(parsed), 5)
        result = self.resolve(parsed)
        self.assertEqual(result["worker"], "gpt-6-luna")
        self.assertIn(result["reviewer"], {item["id"] for item in parsed})

    def test_versions_are_numeric_not_lexicographic(self):
        result = self.resolve([CATALOG[0], CATALOG[1]])
        self.assertEqual(result["worker"], "luna-6.10")

    def test_unavailable_deprecated_and_excluded_models_never_selected(self):
        result = self.resolve(excluded=["blocked-1"])
        self.assertNotIn(result["worker"], {"gone-1", "old-1", "blocked-1"})
        self.assertNotIn(result["reviewer"], {"gone-1", "old-1", "blocked-1"})

    def test_invalid_override_is_rejected(self):
        with self.assertRaises((ValueError, KeyError)):
            self.resolve(worker="not-in-catalog")

    def test_efforts_are_supported_or_none(self):
        result = self.resolve([model("one", "Fast and affordable.", ("low",))])
        self.assertIn(result["worker_effort"], {"low", None})
        self.assertIn(result["reviewer_effort"], {None, "low"})
        by_id = {m["id"]: set(m["reasoning_efforts"]) for m in [model("one", "Fast and affordable.", ("low",))]}
        for role, key in (("worker", "worker_effort"), ("reviewer", "reviewer_effort")):
            chosen = result[role]
            self.assertTrue(result[key] is None or result[key] in by_id.get(chosen, set()))

    def test_empty_catalog_has_safe_fallback_shape(self):
        result = self.resolve([])
        self.assertIsNone(result["worker"])
        self.assertIsNone(result["reviewer"])
        self.assertIsInstance(result["warnings"], list)
        self.assertIsInstance(result["rationale"], dict)

    def test_opaque_id_is_stable_and_uncertainty_is_explained(self):
        opaque = [CATALOG[4]]
        first = self.resolve(opaque)
        second = self.resolve(opaque)
        self.assertEqual(first["worker"], second["worker"])
        self.assertIn("opaque-x9", {first["worker"], first["reviewer"]})
        rationale = json.dumps(first["rationale"], ensure_ascii=False).lower()
        warnings = json.dumps(first["warnings"], ensure_ascii=False).lower()
        self.assertTrue(any(word in rationale + warnings for word in ("unknown", "opaque", "uncertain", "doubt", "description", "unclassified")))

    def test_head_policy_preserves_primary_and_result_contract(self):
        result = self.resolve()
        self.assertIn("head_policy", result)
        self.assertIn("worker", result)
        self.assertIn("reviewer", result)
        self.assertIsInstance(result["warnings"], list)
        self.assertIsInstance(result["rationale"], dict)

    def test_cli_json_output_and_errors_do_not_modify_primary_script(self):
        original = SCRIPT.read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            catalog_path = Path(directory) / "catalog.json"
            catalog_path.write_text(json.dumps(CATALOG), encoding="utf-8")
            good = subprocess.run([sys.executable, str(SCRIPT), "--catalog", str(catalog_path),
                                   "--task-kind", "implementation", "--exclude", "blocked-1"],
                                  capture_output=True, text=True, encoding="utf-8", timeout=15)
            self.assertEqual(good.returncode, 0, good.stderr)
            data = json.loads(good.stdout)
            self.assertIn("worker", data)
            self.assertIn("head_policy", data)
            bad = subprocess.run([sys.executable, str(SCRIPT), "--catalog", str(catalog_path),
                                  "--worker", "missing-model"], capture_output=True,
                                 text=True, encoding="utf-8", timeout=15)
            self.assertNotEqual(bad.returncode, 0)
            self.assertEqual(SCRIPT.read_bytes(), original)

    def test_cli_reads_catalog_from_stdin(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--task-kind", "mechanical"],
                                input=json.dumps(CATALOG), capture_output=True, text=True,
                                encoding="utf-8", timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIsInstance(json.loads(result.stdout), dict)


if __name__ == "__main__":
    unittest.main()
