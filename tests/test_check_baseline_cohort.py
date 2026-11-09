"""Tests for baseline cohort revision and execution-environment readiness."""

from pathlib import Path
import hashlib
import importlib.util
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check-baseline-cohort.py"
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
try:
    SPEC = importlib.util.spec_from_file_location("check_baseline_cohort", SCRIPT)
    checker = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(checker)
finally:
    sys.path.remove(str(SCRIPTS))


class BaselineCohortReadinessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "cohort.yml"
        self.roles = ["backend-developer", "product-analyst"]
        self.prompts = {
            role: f"Exact prompt for {role}\n" for role in self.roles
        }
        self.base = "a" * 40
        self.scenario_commit = "b" * 40
        self.skill_commit = "c" * 40
        self.cohort = self.valid_cohort()

    def tearDown(self):
        self.temp.cleanup()

    def valid_cohort(self):
        pins = []
        for role in self.roles:
            scenario_id = f"SCEN-BASELINE-{role.upper()}"
            pins.append({
                "scenario_id": scenario_id,
                "role": role,
                "scenario_commit": self.scenario_commit,
                "skill_commit": self.skill_commit,
                "prompt_sha256": hashlib.sha256(self.prompts[role].encode("utf-8")).hexdigest(),
            })
        return {
            "schema_version": 1,
            "cohort_id": "controlled-test-cohort",
            "purpose": "Test cohort",
            "repository_base_commit": self.base,
            "execution_environment": {
                "provider": "Provider",
                "model_display_label": "Model label",
                "model_identifier": "model-id",
                "model_version": "version-1",
                "mode": "agent",
                "configuration": {
                    "temperature": 0,
                    "reasoning_effort": "medium",
                    "other_material_settings": [],
                },
                "tool_permissions": "Declared tool permissions",
                "operating_environment": "Isolated local worktree",
            },
            "scenario_pins": pins,
            "notes": [],
        }

    def write(self, data=None):
        self.path.write_text(
            yaml.safe_dump(self.cohort if data is None else data, sort_keys=False),
            encoding="utf-8",
        )

    def mocked_git(self):
        def show(commit, path):
            if path.startswith("tests/scenarios/"):
                role = path.split("SCEN-BASELINE-", 1)[1][:-4].lower()
                role = role.replace("technical-writer-knowledge-engineer", "technical-writer-knowledge-engineer")
                scenario_id = f"SCEN-BASELINE-{role.upper()}"
                return yaml.safe_dump({
                    "id": scenario_id,
                    "role": role,
                    "task_prompt": self.prompts[role],
                })
            return "# canonical skill\n"
        return (
            patch.object(checker, "git_commit_exists", return_value=True),
            patch.object(checker, "commit_contains", return_value=True),
            patch.object(checker, "git_file", side_effect=show),
            patch.object(checker, "expected_roles", return_value=self.roles),
        )

    def validate(self):
        patches = self.mocked_git()
        with patches[0], patches[1], patches[2], patches[3]:
            return checker.validate_cohort(self.path)

    def test_complete_cohort_pins_pass(self):
        self.write()
        errors, blockers = self.validate()
        self.assertEqual(errors, [])
        self.assertEqual(blockers, [])

    def test_unpinned_values_are_blockers_not_invented_defaults(self):
        self.cohort["repository_base_commit"] = None
        env = self.cohort["execution_environment"]
        env["provider"] = None
        env["configuration"]["temperature"] = None
        self.cohort["scenario_pins"][0]["scenario_commit"] = None
        self.cohort["scenario_pins"][0]["skill_commit"] = None
        self.cohort["scenario_pins"][0]["prompt_sha256"] = None
        self.write()
        errors, blockers = self.validate()
        self.assertEqual(errors, [])
        self.assertTrue(any("repository_base_commit is not pinned" in item for item in blockers))
        self.assertTrue(any("execution_environment.provider is not recorded" in item for item in blockers))
        self.assertTrue(any("temperature is not recorded" in item for item in blockers))
        self.assertTrue(any("scenario_commit is not pinned" in item for item in blockers))
        self.assertTrue(any("skill_commit is not pinned" in item for item in blockers))
        self.assertTrue(any("prompt_sha256 is not pinned" in item for item in blockers))

    def test_prompt_hash_must_match_exact_pinned_task_prompt_bytes(self):
        self.cohort["scenario_pins"][0]["prompt_sha256"] = "d" * 64
        self.write()
        errors, _ = self.validate()
        self.assertTrue(any("prompt_sha256 does not match" in item for item in errors))

    def test_missing_canonical_scenario_pin_is_rejected(self):
        self.cohort["scenario_pins"].pop()
        self.write()
        errors, _ = self.validate()
        self.assertTrue(any("missing canonical scenario pins" in item for item in errors))

    def test_duplicate_scenario_pin_is_rejected(self):
        self.cohort["scenario_pins"].append(dict(self.cohort["scenario_pins"][0]))
        self.write()
        errors, _ = self.validate()
        self.assertTrue(any("duplicate cohort scenario pin" in item for item in errors))

    def test_non_ancestor_revision_is_rejected(self):
        self.write()
        patches = list(self.mocked_git())
        patches[1] = patch.object(checker, "commit_contains", return_value=False)
        with patches[0], patches[1], patches[2], patches[3]:
            errors, _ = checker.validate_cohort(self.path)
        self.assertTrue(any("is not an ancestor" in item for item in errors))

    def test_schema_rejects_malformed_revision_pin(self):
        self.cohort["scenario_pins"][0]["scenario_commit"] = "not-a-git-sha"
        self.write()
        errors, _ = self.validate()
        self.assertTrue(any("scenario_commit" in item for item in errors))

    def test_environment_unknown_values_block_readiness(self):
        self.cohort["execution_environment"]["model_version"] = "unknown"
        self.write()
        errors, blockers = self.validate()
        self.assertEqual(errors, [])
        self.assertTrue(any("model_version is not recorded" in item for item in blockers))


if __name__ == "__main__":
    unittest.main()
