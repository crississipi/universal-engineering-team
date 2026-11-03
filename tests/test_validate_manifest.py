"""Tests for the manifest declaration validator."""

import copy
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

spec = importlib.util.spec_from_file_location(
    "validate_manifest", SCRIPTS / "validate-manifest.py"
)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ManifestValidationTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {
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
            "roles": [
                {"id": "backend-developer", "skill": "skills/backend-developer/SKILL.md"},
                {"id": "qa-manager", "skill": "skills/qa-manager/SKILL.md"},
            ],
            "artifacts": [
                {"id": "ART-BACKEND", "name": "Backend Package", "owner": "backend-developer", "primary_producer": "backend-developer", "contributors": ["qa-manager"]},
                {"id": "ART-QUALITY-EVIDENCE", "name": "Quality Package", "owner": "qa-manager", "primary_producer": "qa-manager", "contributors": ["backend-developer"]},
            ],
            "relationships": [{
                "id": "REL-ART-BACKEND--ART-QUALITY-EVIDENCE",
                "producer_artifact_id": "ART-BACKEND",
                "consumer_artifact_id": "ART-QUALITY-EVIDENCE",
                "relationship_type": "required_input",
                "output": "Backend tests",
                "condition": "Required for verification.",
            }],
            "handoffs": [],
        }
        self.roles = {"roles": ["backend-developer", "qa-manager"]}
        self.ownership = {
            "roles": ["backend-developer", "qa-manager"],
            "artifacts": [
                {"id": "ART-BACKEND", "owner": "backend-developer", "primary_producer": "backend-developer", "contributors": ["qa-manager"]},
                {"id": "ART-QUALITY-EVIDENCE", "owner": "qa-manager", "primary_producer": "qa-manager", "contributors": ["backend-developer"]},
            ],
            "handoffs": [],
        }
        tick = chr(96)
        self.matrix = (
            "| Producer | Consumer | Output | Relationship | Trigger / boundary |\n"
            "|---|---|---|---|---|\n"
            f"| {tick}ART-BACKEND{tick} | {tick}ART-QUALITY-EVIDENCE{tick} | Backend tests | "
            f"{tick}required_input{tick} | Required for verification. |"
        )
        self.schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "additionalProperties": False,
            "required": ["version", "sources", "roles", "artifacts", "relationships", "handoffs"],
            "properties": {
                "version": {"const": 1},
                "sources": {"type": "object"},
                "roles": {"type": "array"},
                "artifacts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "owner": {"type": "string"},
                            "primary_producer": {"type": "string"},
                            "contributors": {"type": "array"},
                        },
                    },
                },
                "relationships": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "id": {"type": "string"},
                            "producer_artifact_id": {"type": "string"},
                            "consumer_artifact_id": {"type": "string"},
                            "relationship_type": {"type": "string"},
                            "output": {"type": "string"},
                            "condition": {"type": "string"},
                        },
                    },
                },
                "handoffs": {"type": "array"},
            },
        }

    def validate(self):
        return validator.validate_manifest(
            self.manifest, self.schema, self.roles,
            self.ownership, self.matrix, check_skill_paths=False,
        )

    def test_valid_manifest_passes(self):
        self.assertEqual(self.validate(), [])

    def test_unknown_role_reference_fails(self):
        self.manifest["roles"][0]["id"] = "security-engineer"
        self.manifest["roles"][0]["skill"] = "skills/security-engineer/SKILL.md"
        self.assertTrue(any("unknown role reference" in error for error in self.validate()))

    def test_unknown_artifact_reference_fails(self):
        self.manifest["relationships"][0]["consumer_artifact_id"] = "ART-MISSING"
        self.assertTrue(any("unknown artifact reference" in error for error in self.validate()))

    def test_missing_matrix_mirror_edge_fails(self):
        self.manifest["relationships"] = []
        self.assertTrue(any("missing relationship mirror" in error for error in self.validate()))

    def test_conflicting_duplicate_relationship_fails(self):
        duplicate = copy.deepcopy(self.manifest["relationships"][0])
        duplicate["relationship_type"] = "feedback"
        self.manifest["relationships"].append(duplicate)
        self.assertTrue(any("conflicting duplicate declaration" in error for error in self.validate()))

    def test_conditional_handoff_requires_activation_condition(self):
        self.manifest["relationships"][0]["relationship_type"] = "conditional_input"
        self.matrix = self.matrix.replace("required_input", "conditional_input")
        self.manifest["handoffs"] = [{
            "id": "HOF-BACKEND-QA-001", "contract_version": "1.0",
            "from_role": "backend-developer", "to_role": "qa-manager",
            "artifact_id": "ART-BACKEND", "consumer_artifact_id": "ART-QUALITY-EVIDENCE",
            "relationship_type": "conditional_input", "purpose": "Verify backend work.",
            "required_outputs": ["Backend tests"], "required_context": [],
            "acceptance_checks": ["Tests pass."], "status": "proposed",
        }]
        self.ownership["handoffs"] = copy.deepcopy(self.manifest["handoffs"])
        self.assertTrue(any("activation_condition" in error for error in self.validate()))

    def test_handoff_producer_must_own_and_produce_source_artifact(self):
        self.manifest["handoffs"] = [{
            "id": "HOF-BACKEND-QA-001", "contract_version": "1.0",
            "from_role": "qa-manager", "to_role": "qa-manager",
            "artifact_id": "ART-BACKEND", "consumer_artifact_id": "ART-QUALITY-EVIDENCE",
            "relationship_type": "required_input", "purpose": "Verify backend work.",
            "required_outputs": ["Backend tests"], "required_context": [],
            "acceptance_checks": ["Tests pass."], "status": "proposed",
        }]
        self.ownership["handoffs"] = copy.deepcopy(self.manifest["handoffs"])
        errors = self.validate()
        self.assertTrue(any("from_role must own producer artifact" in error for error in errors))
        self.assertTrue(any("from_role must be the primary producer" in error for error in errors))

    def test_handoff_consumer_must_own_consumer_artifact(self):
        self.manifest["handoffs"] = [{
            "id": "HOF-BACKEND-QA-001", "contract_version": "1.0",
            "from_role": "backend-developer", "to_role": "backend-developer",
            "artifact_id": "ART-BACKEND", "consumer_artifact_id": "ART-QUALITY-EVIDENCE",
            "relationship_type": "required_input", "purpose": "Verify backend work.",
            "required_outputs": ["Backend tests"], "required_context": [],
            "acceptance_checks": ["Tests pass."], "status": "proposed",
        }]
        self.ownership["handoffs"] = copy.deepcopy(self.manifest["handoffs"])
        self.assertTrue(any("to_role must own consumer artifact" in error for error in self.validate()))

    def test_feedback_does_not_block_progress(self):
        self.assertFalse(validator.relationship_requires_input("feedback"))
        self.assertFalse(validator.relationship_requires_input("conditional_input"))
        self.assertTrue(validator.relationship_requires_input("conditional_input", activated=True))
        self.assertTrue(validator.relationship_requires_input("required_input"))

    def test_relationship_rejects_unsupported_acceptance_field(self):
        self.manifest["relationships"][0]["acceptance_required"] = True
        self.assertTrue(any("Additional properties are not allowed" in error for error in self.validate()))


if __name__ == "__main__":
    unittest.main()
