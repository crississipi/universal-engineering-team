"""Tests for role requirement-anchor traceability validation."""

from pathlib import Path
import importlib.util
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

SCRIPT = SCRIPTS_DIR / "validate-requirements.py"
spec = importlib.util.spec_from_file_location("validate_requirements", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class RequirementTraceabilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.roles = ["alpha-role", "beta-role"]
        (self.root / "docs/evaluation/baseline").mkdir(parents=True)
        for role in self.roles:
            (self.root / "skills" / role).mkdir(parents=True)
        self.write_baseline()
        self.write_skill("alpha-role", "REQ-ALPHA-01")
        self.write_skill("beta-role", "REQ-BETA-01")

    def tearDown(self):
        self.temp.cleanup()

    def write_baseline(self, override=None):
        rows = [
            "| Canonical role | Pilot coverage | Baseline scenario ID (proposed) | Role requirement anchor | Design state |",
            "|---|---|---|---|---|",
        ]
        for role, req_id in (override or {
            "alpha-role": "REQ-ALPHA-01",
            "beta-role": "REQ-BETA-01",
        }).items():
            rows.append(
                f"| {role} | None | SCEN-BASELINE-{role.upper()} | {req_id} | Not designed |"
            )
        path = self.root / "docs/evaluation/baseline/README.md"
        path.write_text("\n".join(rows) + "\n", encoding="utf-8")

    def write_skill(self, role, req_id, *, section=True, statement=True):
        if section:
            marker = f"## 1. Identity and boundaries\n\n<!-- {req_id} -->"
        else:
            marker = f"## Other section\n\n<!-- {req_id} -->"
        if statement:
            marker += "\n**Requirement:** Own and deliver the role's defined outcome."
        path = self.root / "skills" / role / "SKILL.md"
        path.write_text(marker + "\n\n## 2. Activation\n", encoding="utf-8")

    def errors(self):
        return validator.validate_requirement_anchors(self.root, self.roles)

    def test_accepts_unique_anchors_mapped_to_baseline_register(self):
        self.assertEqual(self.errors(), [])

    def test_rejects_missing_anchor(self):
        self.write_skill("alpha-role", "REQ-ALPHA-01", section=True)
        path = self.root / "skills/alpha-role/SKILL.md"
        path.write_text("## 1. Identity and boundaries\n\nNo marker.\n", encoding="utf-8")
        self.assertTrue(any("expected exactly one" in item for item in self.errors()))

    def test_rejects_duplicate_requirement_ids_across_roles(self):
        self.write_skill("beta-role", "REQ-ALPHA-01")
        self.assertTrue(any("Duplicate requirement ID" in item for item in self.errors()))

    def test_rejects_anchor_outside_identity_section(self):
        self.write_skill("alpha-role", "REQ-ALPHA-01", section=False)
        self.assertTrue(any("must appear in Identity and boundaries" in item for item in self.errors()))

    def test_rejects_missing_adjacent_requirement_statement(self):
        self.write_skill("alpha-role", "REQ-ALPHA-01", statement=False)
        self.assertTrue(any("must be followed by" in item for item in self.errors()))

    def test_rejects_baseline_register_anchor_mismatch(self):
        self.write_baseline({
            "alpha-role": "REQ-OTHER-01",
            "beta-role": "REQ-BETA-01",
        })
        self.assertTrue(any("must reference REQ-ALPHA-01" in item for item in self.errors()))


if __name__ == "__main__":
    unittest.main()
