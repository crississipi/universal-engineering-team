"""Tests for scenario approval and post-run review lifecycle."""

from contextlib import redirect_stdout
from pathlib import Path
import importlib.util
import io
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

SCRIPT = SCRIPTS_DIR / "validate-scenarios.py"
spec = importlib.util.spec_from_file_location("validate_scenarios", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ScenarioLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.scenario_dir = self.root / "scenarios"
        self.review_dir = self.root / "reviews"
        self.scenario_dir.mkdir()
        self.review_dir.mkdir()
        self.scenario_id = "SCEN-TEST-BACKEND"
        self.scenario_path = self.scenario_dir / "scenario.yml"

    def tearDown(self):
        self.temp.cleanup()

    def scenario(self, **overrides):
        data = {
            "id": self.scenario_id,
            "role": "backend-developer",
            "status": "draft",
            "required_requirements": ["REQ-BACKEND-01"],
            "criteria": [{
                "id": "CORRECTNESS",
                "description": "Implements the stated behavior correctly.",
                "weight": 100,
                "critical": True,
                "requirement_ref": "REQ-BACKEND-01",
            }],
            "review_record": None,
            "evidence": [{
                "path": "skills/backend-developer/SKILL.md",
                "commit": "a" * 40,
            }],
        }
        data.update(overrides)
        return data

    def write_yaml(self, path, data):
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def run_validator(self):
        original_safe_path = validator.safe_repo_path

        def safe_path(raw_path, required_prefix=None):
            if isinstance(raw_path, str) and raw_path.startswith("docs/reviews/"):
                return self.review_dir / Path(raw_path).name
            return original_safe_path(raw_path, required_prefix)

        output = io.StringIO()
        with (
            patch.object(validator, "SCENARIO_DIR", self.scenario_dir),
            patch.object(validator, "REVIEW_DIR", self.review_dir),
            patch.object(validator, "safe_repo_path", safe_path),
            redirect_stdout(output),
        ):
            code = validator.main()
        return code, output.getvalue()

    def test_draft_scenario_can_exist_without_fabricated_review(self):
        self.write_yaml(self.scenario_path, self.scenario())
        code, output = self.run_validator()
        self.assertEqual(code, 0, output)
        self.assertIn("Scenario validation passed", output)

    def test_approved_scenario_requires_pre_run_approval_metadata(self):
        self.write_yaml(
            self.scenario_path,
            self.scenario(status="approved"),
        )
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("approved scenarios require an approval mapping", output)

    def test_approved_scenario_with_approval_does_not_require_run_review(self):
        self.write_yaml(
            self.scenario_path,
            self.scenario(
                status="approved",
                approval={
                    "approved_by": "Human reviewer",
                    "approved_at": "2026-11-03T15:00:00Z",
                },
            ),
        )
        code, output = self.run_validator()
        self.assertEqual(code, 0, output)

    def test_post_run_review_is_separate_and_accepts_actual_run_count(self):
        review_path = f"docs/reviews/scenario-{self.scenario_id}.yml"
        self.write_yaml(
            self.scenario_path,
            self.scenario(review_record=review_path),
        )
        self.write_yaml(
            self.review_dir / Path(review_path).name,
            {
                "scenario_id": self.scenario_id,
                "decision": "pass",
                "reviewer": "Human reviewer",
                "runs": 3,
            },
        )
        code, output = self.run_validator()
        self.assertEqual(code, 0, output)

    def test_post_run_review_rejects_zero_runs(self):
        review_path = f"docs/reviews/scenario-{self.scenario_id}.yml"
        self.write_yaml(
            self.scenario_path,
            self.scenario(review_record=review_path),
        )
        self.write_yaml(
            self.review_dir / Path(review_path).name,
            {
                "scenario_id": self.scenario_id,
                "decision": "pass",
                "reviewer": "Human reviewer",
                "runs": 0,
            },
        )
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("runs must be a positive integer", output)


    def test_rejects_criteria_whose_weights_do_not_total_100(self):
        criteria = [
            {
                "id": "CORRECTNESS",
                "description": "Implements the stated behavior correctly.",
                "weight": 60,
                "critical": True,
                "requirement_ref": "REQ-BACKEND-01",
            },
            {
                "id": "EVIDENCE",
                "description": "Provides reproducible verification evidence.",
                "weight": 50,
                "critical": False,
                "requirement_ref": "REQ-BACKEND-01",
            },
        ]
        self.write_yaml(self.scenario_path, self.scenario(criteria=criteria))
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("criterion weights must total 100; found 110", output)

    def test_rejects_non_finite_criterion_weights(self):
        criteria = self.scenario()["criteria"]
        criteria[0]["weight"] = float("nan")
        self.write_yaml(self.scenario_path, self.scenario(criteria=criteria))
        code, output = self.run_validator()
        self.assertEqual(code, 1)
        self.assertIn("weight must be a finite positive number", output)


if __name__ == "__main__":
    unittest.main()
