"""Tests for baseline pre-run governance checks."""

from pathlib import Path
import importlib.util
import tempfile
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check-baseline-governance.py"
SPEC = importlib.util.spec_from_file_location("check_baseline_governance", SCRIPT)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class BaselineGovernanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.scenario_dir = self.root / "scenarios"
        self.scenario_dir.mkdir()
        self.register_path = self.root / "stakeholder-decisions.yml"
        self.roles = ["backend-developer", "product-analyst"]
        self.decision_ids = {"METRICS", "TIMEZONE"}

    def tearDown(self):
        self.temp.cleanup()

    def write_yaml(self, path, data):
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def scenarios(self, approved=False):
        for role in self.roles:
            scenario_id = f"SCEN-BASELINE-{role.upper().replace('-', '-')}"
            data = {
                "id": scenario_id,
                "role": role,
                "status": "approved" if approved else "draft",
                "approval": {
                    "approved_by": "Authorized reviewer",
                    "approved_at": "2026-11-08T12:00:00Z",
                } if approved else None,
            }
            self.write_yaml(self.scenario_dir / f"{scenario_id}.yml", data)

    def decisions(self, status="open"):
        records = []
        for decision_id in sorted(self.decision_ids):
            item = {
                "id": decision_id,
                "question": f"Confirm {decision_id}",
                "owner": "Authorized stakeholder",
                "affected_roles": ["backend-developer"],
                "status": status,
                "decision": "Confirmed outcome" if status != "open" else None,
                "rationale": "Recorded rationale" if status != "open" else None,
                "authorized_by": "Decision owner" if status != "open" else None,
                "authorized_at": "2026-11-08T12:00:00Z" if status != "open" else None,
                "evidence_ref": "docs/decision-record.md" if status != "open" else None,
                "non_scored_scope": "Affected assertions are excluded" if status == "non_scored" else None,
            }
            records.append(item)
        self.write_yaml(self.register_path, {"schema_version": 1, "decisions": records})

    def patches(self):
        return (
            patch.object(checker, "SCENARIO_DIR", self.scenario_dir),
            patch.object(checker, "DECISION_REGISTER", self.register_path),
            patch.object(checker, "expected_roles", lambda: self.roles),
            patch.object(checker, "EXPECTED_DECISIONS", self.decision_ids),
        )

    def test_open_decisions_and_draft_scenarios_block_governance(self):
        self.scenarios(approved=False)
        self.decisions("open")
        with self.patches()[0], self.patches()[1], self.patches()[2], self.patches()[3]:
            scenario_errors, scenario_blockers = checker.validate_scenario_approvals()
            decision_errors, decision_blockers = checker.validate_decision_register()
        self.assertEqual(scenario_errors, [])
        self.assertEqual(decision_errors, [])
        self.assertEqual(len(scenario_blockers), 2)
        self.assertEqual(len(decision_blockers), 2)

    def test_approved_scenarios_and_confirmed_decisions_clear_governance(self):
        self.scenarios(approved=True)
        self.decisions("confirmed")
        with self.patches()[0], self.patches()[1], self.patches()[2], self.patches()[3]:
            scenario_errors, scenario_blockers = checker.validate_scenario_approvals()
            decision_errors, decision_blockers = checker.validate_decision_register()
        self.assertEqual(scenario_errors, [])
        self.assertEqual(scenario_blockers, [])
        self.assertEqual(decision_errors, [])
        self.assertEqual(decision_blockers, [])

    def test_non_scored_disposition_requires_explicit_scope(self):
        self.decisions("non_scored")
        data = yaml.safe_load(self.register_path.read_text(encoding="utf-8"))
        data["decisions"][0]["non_scored_scope"] = None
        self.write_yaml(self.register_path, data)
        with patch.object(checker, "EXPECTED_DECISIONS", self.decision_ids):
            errors, blockers = checker.validate_decision_register(self.register_path)
        self.assertTrue(any("non_scored_scope is required" in item for item in errors))
        self.assertEqual(blockers, [])

    def test_open_decision_cannot_contain_authorization_metadata(self):
        self.decisions("open")
        data = yaml.safe_load(self.register_path.read_text(encoding="utf-8"))
        data["decisions"][0]["authorized_by"] = "Someone"
        self.write_yaml(self.register_path, data)
        with patch.object(checker, "EXPECTED_DECISIONS", self.decision_ids):
            errors, _ = checker.validate_decision_register(self.register_path)
        self.assertTrue(any("open decisions must not contain authorized_by" in item for item in errors))

    def test_rejects_duplicate_decision_ids(self):
        self.decisions("open")
        data = yaml.safe_load(self.register_path.read_text(encoding="utf-8"))
        data["decisions"].append(dict(data["decisions"][0]))
        self.write_yaml(self.register_path, data)
        with patch.object(checker, "EXPECTED_DECISIONS", self.decision_ids):
            errors, _ = checker.validate_decision_register(self.register_path)
        self.assertTrue(any("duplicate stakeholder decision ID" in item for item in errors))

    def test_rejects_missing_required_decision(self):
        self.decisions("open")
        data = yaml.safe_load(self.register_path.read_text(encoding="utf-8"))
        data["decisions"].pop()
        self.write_yaml(self.register_path, data)
        with patch.object(checker, "EXPECTED_DECISIONS", self.decision_ids):
            errors, _ = checker.validate_decision_register(self.register_path)
        self.assertTrue(any("missing required decisions" in item for item in errors))

    def test_rejects_invalid_authorization_timestamp(self):
        self.decisions("confirmed")
        data = yaml.safe_load(self.register_path.read_text(encoding="utf-8"))
        data["decisions"][0]["authorized_at"] = "yesterday"
        self.write_yaml(self.register_path, data)
        with patch.object(checker, "EXPECTED_DECISIONS", self.decision_ids):
            errors, _ = checker.validate_decision_register(self.register_path)
        self.assertTrue(any("authorized_at must be a valid ISO-8601 timestamp" in item for item in errors))

    def test_approved_scenario_requires_complete_metadata(self):
        self.scenarios(approved=True)
        scenario_path = next(self.scenario_dir.glob("*.yml"))
        data = yaml.safe_load(scenario_path.read_text(encoding="utf-8"))
        data["approval"]["approved_by"] = " "
        self.write_yaml(scenario_path, data)
        with patch.object(checker, "SCENARIO_DIR", self.scenario_dir), patch.object(checker, "expected_roles", lambda: self.roles):
            errors, blockers = checker.validate_scenario_approvals()
        self.assertTrue(any("approval.approved_by must be non-empty" in item for item in errors))
        self.assertEqual(blockers, [])

    def test_noncanonical_and_duplicate_scenario_roles_are_rejected(self):
        self.scenarios(approved=True)
        duplicate_id = "SCEN-BASELINE-DUPLICATE"
        self.write_yaml(self.scenario_dir / f"{duplicate_id}.yml", {
            "id": duplicate_id,
            "role": "backend-developer",
            "status": "approved",
            "approval": {"approved_by": "Reviewer", "approved_at": "2026-11-08T12:00:00Z"},
        })
        with patch.object(checker, "SCENARIO_DIR", self.scenario_dir), patch.object(checker, "expected_roles", lambda: self.roles):
            errors, _ = checker.validate_scenario_approvals()
        self.assertTrue(any("duplicate baseline scenario role" in item for item in errors))
        self.assertTrue(any("expected 2 baseline scenarios; found 3" in item for item in errors))


    def test_rejects_non_string_decision_status_and_scenario_role(self):
        self.decisions("open")
        data = yaml.safe_load(self.register_path.read_text(encoding="utf-8"))
        data["decisions"][0]["status"] = ["open"]
        self.write_yaml(self.register_path, data)
        with patch.object(checker, "EXPECTED_DECISIONS", self.decision_ids), patch.object(checker, "expected_roles", lambda: self.roles):
            decision_errors, _ = checker.validate_decision_register(self.register_path)
        self.assertTrue(any("status must be open, confirmed, or non_scored" in item for item in decision_errors))

        self.scenarios(approved=True)
        scenario_path = next(self.scenario_dir.glob("*.yml"))
        scenario = yaml.safe_load(scenario_path.read_text(encoding="utf-8"))
        scenario["role"] = ["backend-developer"]
        self.write_yaml(scenario_path, scenario)
        with patch.object(checker, "SCENARIO_DIR", self.scenario_dir), patch.object(checker, "expected_roles", lambda: self.roles):
            scenario_errors, _ = checker.validate_scenario_approvals()
        self.assertTrue(any("role is not canonical" in item for item in scenario_errors))


if __name__ == "__main__":
    unittest.main()
