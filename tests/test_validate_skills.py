"""Regression tests for scripts/validate-skills.py frontmatter parsing."""

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
VALIDATOR_PATH = SCRIPTS_DIR / "validate-skills.py"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

spec = importlib.util.spec_from_file_location(
    "validate_skills",
    VALIDATOR_PATH,
)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ParseSkillTests(unittest.TestCase):
    def setUp(self):
        validator.errors.clear()

    def parse_content(self, content):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_path = Path(temp_dir) / "SKILL.md"
            skill_path.write_text(content, encoding="utf-8")
            result = validator.parse_skill(skill_path)
        return result, list(validator.errors)

    def test_valid_frontmatter_returns_mapping(self):
        metadata, errors = self.parse_content(
            "---\nname: backend-developer\n"
            "description: Builds backend services\n---\n\n# Backend\n"
        )

        self.assertEqual(
            metadata,
            {
                "name": "backend-developer",
                "description": "Builds backend services",
            },
        )
        self.assertEqual(errors, [])

    def test_malformed_frontmatter_reports_cleanly(self):
        metadata, errors = self.parse_content(
            "---\nname: [unterminated\ndescription: Broken YAML\n---\n"
        )

        self.assertIsNone(metadata)
        self.assertEqual(len(errors), 1)
        self.assertIn("invalid YAML frontmatter", errors[0])

    def test_missing_frontmatter_closer_reports_cleanly(self):
        metadata, errors = self.parse_content(
            "---\nname: backend-developer\n"
            "description: Builds backend services\n"
        )

        self.assertIsNone(metadata)
        self.assertTrue(
            any("missing YAML frontmatter closer" in error for error in errors)
        )

    def test_non_mapping_frontmatter_reports_cleanly(self):
        metadata, errors = self.parse_content(
            "---\n- backend-developer\n- Builds backend services\n---\n"
        )

        self.assertIsNone(metadata)
        self.assertTrue(
            any("frontmatter must be a YAML mapping" in error for error in errors)
        )

    def test_non_delimiter_line_does_not_close_frontmatter(self):
        metadata, errors = self.parse_content(
            "---\nname: backend-developer\n---not-a-delimiter\n"
        )

        self.assertIsNone(metadata)
        self.assertTrue(
            any("missing YAML frontmatter closer" in error for error in errors)
        )

    def test_missing_required_frontmatter_values_are_reported(self):
        metadata, errors = self.parse_content(
            "---\nname: backend-developer\ndescription: '   '\n---\n"
        )

        self.assertIsNotNone(metadata)
        self.assertEqual(len(errors), 1)
        self.assertIn("missing or invalid 'description'", errors[0])


class ManifestSourceDriftTests(unittest.TestCase):
    def setUp(self):
        validator.errors.clear()

    def fixtures(self):
        roles = {"roles": ["backend-developer"]}
        ownership = {
            "artifacts": [{
                "id": "ART-BACKEND",
                "name": "Backend Package",
                "owner": "backend-developer",
                "primary_producer": "backend-developer",
                "contributors": ["qa-manager"],
            }],
            "handoffs": [],
        }
        matrix = (
            "| Producer | Consumer | Output | Relationship | Trigger |\n"
            "|---|---|---|---|---|\n"
            "| `ART-BACKEND` | `ART-QUALITY-EVIDENCE` | "
            "Backend tests | `required_input` | For implemented scope. |"
        )
        manifest = {
            "version": 1,
            "sources": {
                "roles": "docs/team/expected-roles.yml",
                "artifacts": "docs/team/ownership.yml",
                "handoffs": "docs/team/ownership.yml",
                "relationships": "docs/team/producer-consumer-matrix.md",
                "handoff_contract": "docs/team/handoff-contract-schema.md",
                "handoff_acceptance": "docs/team/handoff-acceptance-rules.md",
                "handoff_escalation": "docs/team/handoff-escalation-rules.md",
                "workflow_lifecycle": "docs/team/workflow-lifecycle.md",
                "execution_records": "docs/team/execution-record-model.md",
            },
            "roles": [{
                "id": "backend-developer",
                "skill": "skills/backend-developer/SKILL.md",
            }],
            "artifacts": [{
                "id": "ART-BACKEND",
                "name": "Backend Package",
                "owner": "backend-developer",
                "primary_producer": "backend-developer",
                "contributors": ["qa-manager"],
            }],
            "relationships": [{
                "id": "REL-ART-BACKEND--ART-QUALITY-EVIDENCE",
                "producer_artifact_id": "ART-BACKEND",
                "consumer_artifact_id": "ART-QUALITY-EVIDENCE",
                "relationship_type": "required_input",
                "output": "Backend tests",
                "condition": "For implemented scope.",
            }],
            "handoffs": [],
        }
        return manifest, roles, ownership, matrix

    def test_matching_manifest_sources_have_no_drift(self):
        self.assertEqual(
            validator.compare_manifest_sources(*self.fixtures()),
            [],
        )

    def test_artifact_owner_drift_is_reported(self):
        manifest, roles, ownership, matrix = self.fixtures()
        manifest["artifacts"][0]["owner"] = "delivery-lead"
        problems = validator.compare_manifest_sources(
            manifest, roles, ownership, matrix
        )
        self.assertTrue(any("artifact ownership projection drifts" in x for x in problems))

    def test_relationship_drift_is_reported(self):
        manifest, roles, ownership, matrix = self.fixtures()
        manifest["relationships"][0]["relationship_type"] = "feedback"
        problems = validator.compare_manifest_sources(
            manifest, roles, ownership, matrix
        )
        self.assertTrue(any("producer-consumer relationships drift" in x for x in problems))

    def test_formal_handoff_drift_is_reported(self):
        manifest, roles, ownership, matrix = self.fixtures()
        manifest["handoffs"].append({"id": "HOF-EXAMPLE"})
        problems = validator.compare_manifest_sources(
            manifest, roles, ownership, matrix
        )
        self.assertTrue(any("formal handoffs drift" in x for x in problems))




if __name__ == "__main__":
    unittest.main()
