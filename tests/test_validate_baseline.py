"""Tests for the dedicated baseline run-record validator."""

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

spec = importlib.util.spec_from_file_location(
    "validate_baseline", SCRIPTS / "validate-baseline.py"
)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def valid_scenario(status="approved"):
    return {
        "id": "SCEN-BASELINE-TEST",
        "role": "product-analyst",
        "rubric_version": "baseline-v1",
        "status": status,
        "approval": {"approved_by": "human-reviewer", "approved_at": "2026-11-08T10:00:00Z"},
        "required_requirements": ["REQ-TEST-01"],
        "criteria": [
            {"id": "C1", "requirement_ref": "REQ-TEST-01", "weight": 100}
        ],
    }


class BaselineRunRecordValidationTests(unittest.TestCase):
    def setUp(self):
        self.schema = validator.load_schema(ROOT)
        evidence_root = ROOT / "evaluations" / "baseline" / "evidence"
        evidence_root.mkdir(parents=True, exist_ok=True)
        self.temp_evidence = tempfile.TemporaryDirectory(dir=evidence_root)
        self.evidence_dir = Path(self.temp_evidence.name)
        self.addCleanup(self.temp_evidence.cleanup)
        self.prompt_file = self.evidence_dir / "prompt-used.md"
        self.prompt_file.write_text("Approved test prompt\n", encoding="utf-8")
        self.prompt_path = self.prompt_file.relative_to(ROOT).as_posix()

    def make_record(self, scenario=None):
        import hashlib
        scenario = scenario or valid_scenario()
        digest = hashlib.sha256(self.prompt_file.read_bytes()).hexdigest()
        return {
            "evaluation_track": "repository-baseline",
            "run_id": "BASELINE-SCEN-BASELINE-TEST-RUN-01",
            "scenario_id": "SCEN-BASELINE-TEST",
            "role": "product-analyst",
            "rubric_version": "baseline-v1",
            "run_number": 1,
            "started_at": "2026-11-08T10:01:00Z",
            "execution_environment": {
                "provider": "test-provider",
                "model_display_label": "Test Model",
                "model_identifier": "test-model",
                "model_version": "1",
                "mode": "agent",
                "configuration": {
                    "temperature": "unknown",
                    "reasoning_effort": "unknown",
                    "other_material_settings": [],
                },
                "tool_permissions": "read-only",
                "operating_environment": "isolated test environment",
            },
            "revisions": {
                "repository_base_commit": "a" * 40,
                "scenario_commit": "b" * 40,
                "skill_commit": "c" * 40,
                "scenario_path": "tests/scenarios/SCEN-BASELINE-TEST.yml",
                "skill_path": "skills/product-analyst/SKILL.md",
            },
            "input": {
                "prompt_path": self.prompt_path,
                "prompt_sha256": digest,
                "additional_context_references": [],
            },
            "evidence": {
                "output_artifacts": [],
                "transcript_path": "unknown",
                "git_status_path": "unknown",
                "command_results": [],
                "tool_behavior_summary": "No tools used.",
                "errors_or_interruptions": [],
                "redactions_performed": [],
            },
            "scores": [{"criterion_id": "C1", "score": None, "rationale": None}],
            "critical_failures": [],
            "limitations": [],
            "comparability": {
                "cohort_id": "test-cohort",
                "comparable_within_scenario_cohort": None,
                "deviations": [],
            },
            "review": {
                "reviewer": None,
                "reviewed_at": None,
                "decision": None,
                "notes": None,
            },
        }

    def test_schema_is_valid_draft_2020_12(self):
        self.assertEqual(
            self.schema.META_SCHEMA["$schema"],
            "https://json-schema.org/draft/2020-12/schema",
        )

    def test_valid_record_passes_schema_and_cross_reference_checks(self):
        record = self.make_record()
        path = ROOT / "evaluations/baseline/runs/SCEN-BASELINE-TEST-run-01.yml"
        errors = validator.validate_record(
            path, record, {"SCEN-BASELINE-TEST": valid_scenario()}, ROOT, self.schema
        )
        self.assertEqual(errors, [])

    def test_draft_scenario_cannot_have_baseline_run_record(self):
        record = self.make_record()
        path = ROOT / "evaluations/baseline/runs/SCEN-BASELINE-TEST-run-01.yml"
        errors = validator.validate_record(
            path, record, {"SCEN-BASELINE-TEST": valid_scenario("draft")}, ROOT, self.schema
        )
        self.assertTrue(any("[BLV012]" in error for error in errors))

    def test_score_criterion_must_match_scenario_rubric(self):
        record = self.make_record()
        record["scores"][0]["criterion_id"] = "NOT-IN-RUBRIC"
        path = ROOT / "evaluations/baseline/runs/SCEN-BASELINE-TEST-run-01.yml"
        errors = validator.validate_record(
            path, record, {"SCEN-BASELINE-TEST": valid_scenario()}, ROOT, self.schema
        )
        self.assertTrue(any("[BLV021]" in error for error in errors))

    def test_prompt_hash_must_match_preserved_prompt_bytes(self):
        record = self.make_record()
        record["input"]["prompt_sha256"] = "0" * 64
        path = ROOT / "evaluations/baseline/runs/SCEN-BASELINE-TEST-run-01.yml"
        errors = validator.validate_record(
            path, record, {"SCEN-BASELINE-TEST": valid_scenario()}, ROOT, self.schema
        )
        self.assertTrue(any("[BLV023]" in error for error in errors))

    def test_utc_yaml_timestamps_keep_z_suffix(self):
        path = self.evidence_dir / "timestamp.yml"
        path.write_text('started_at: "2026-11-08T10:01:00Z"\\n', encoding="utf-8")
        self.assertEqual(
            validator.load_yaml(path)["started_at"],
            "2026-11-08T10:01:00Z",
        )

    def test_duplicate_yaml_mapping_keys_are_rejected(self):
        path = self.evidence_dir / "duplicate.yml"
        path.write_text("run_number: 1\nrun_number: 2\n", encoding="utf-8")
        with self.assertRaises(Exception) as context:
            validator.load_yaml(path)
        self.assertIn("found duplicate key", str(context.exception))

    def test_schema_rejects_out_of_range_scores(self):
        record = self.make_record()
        record["scores"][0]["score"] = 101
        path = ROOT / "evaluations/baseline/runs/SCEN-BASELINE-TEST-run-01.yml"
        errors = validator.validate_record(
            path, record, {"SCEN-BASELINE-TEST": valid_scenario()}, ROOT, self.schema
        )
        self.assertTrue(any("[BLV010]" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
