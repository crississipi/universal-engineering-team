
"""Unit tests for scripts/validate-handoffs.py."""

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
VALIDATOR_PATH = SCRIPTS_DIR / "validate-handoffs.py"

# Make validation_common importable by the dynamically loaded validator.
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

spec = importlib.util.spec_from_file_location(
    "validate_handoffs",
    VALIDATOR_PATH,
)

validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidateHandoffsTests(unittest.TestCase):

    def setUp(self):
        self.roles = {
            "api-manager",
            "backend-developer",
        }

        self.artifacts = {
            "ART-API-CONTRACT": {
                "id": "ART-API-CONTRACT",
                "owner": "api-manager",
                "primary_producer": "api-manager",
            },
            "ART-BACKEND": {
                "id": "ART-BACKEND",
                "owner": "backend-developer",
                "primary_producer": "backend-developer",
            },
        }

        self.matrix = {
            ("ART-API-CONTRACT", "ART-BACKEND"): "conditional_input",
        }

        self.contract = {
            "id": "HOF-API-BACKEND-001",
            "contract_version": "1.0",
            "from_role": "api-manager",
            "to_role": "backend-developer",
            "artifact_id": "ART-API-CONTRACT",
            "consumer_artifact_id": "ART-BACKEND",
            "relationship_type": "conditional_input",
            "purpose": "Provide the approved API contract for backend implementation.",
            "activation_condition": (
                "The project includes backend implementation of "
                "an API or event interface."
            ),
            "required_outputs": [
                "Approved API specification.",
                "Request and response schemas.",
            ],
            "required_context": [
                "Relevant requirement identifiers.",
                "Applicable API version.",
            ],
            "acceptance_checks": [
                "The API specification is present and parses successfully.",
                "Affected endpoints have request and response definitions.",
            ],
            "status": "proposed",
        }

    def validate(self, contract=None, matrix=None, artifacts=None, seen_ids=None):
        """Run the validator's actual single-contract validation function."""
        errors = []

        validator.validate_handoff(
            item=contract if contract is not None else self.contract,
            index=0,
            roles=self.roles,
            artifacts=artifacts if artifacts is not None else self.artifacts,
            matrix=matrix if matrix is not None else self.matrix,
            seen_ids=seen_ids if seen_ids is not None else set(),
            errors=errors,
        )

        return errors

    def test_valid_contract_passes(self):
        errors = self.validate()

        self.assertEqual(errors, [])

    def test_duplicate_handoff_id_is_rejected(self):
        errors = []
        seen_ids = set()

        validator.validate_handoff(
            item=self.contract,
            index=0,
            roles=self.roles,
            artifacts=self.artifacts,
            matrix=self.matrix,
            seen_ids=seen_ids,
            errors=errors,
        )

        validator.validate_handoff(
            item=self.contract,
            index=1,
            roles=self.roles,
            artifacts=self.artifacts,
            matrix=self.matrix,
            seen_ids=seen_ids,
            errors=errors,
        )

        self.assertTrue(
            any("Duplicate handoff ID" in error for error in errors)
        )

    def test_producer_owner_must_match_source_role(self):
        artifacts = {
            **self.artifacts,
            "ART-API-CONTRACT": {
                "id": "ART-API-CONTRACT",
                "owner": "backend-developer",
                "primary_producer": "api-manager",
            },
        }

        errors = self.validate(artifacts=artifacts)

        self.assertTrue(
            any("owner must match from_role" in error for error in errors)
        )

    def test_conditional_contract_requires_activation_condition(self):
        contract = {
            **self.contract,
            "activation_condition": "",
        }

        errors = self.validate(contract=contract)

        self.assertTrue(
            any(
                "activation_condition is required" in error
                for error in errors
            )
        )

    def test_relationship_type_must_match_matrix(self):
        matrix = {
            ("ART-API-CONTRACT", "ART-BACKEND"): "required_input",
        }

        errors = self.validate(matrix=matrix)

        self.assertTrue(
            any(
                "matrix declares" in error
                for error in errors
            )
        )

    def test_package_pair_must_exist_in_matrix(self):
        errors = self.validate(matrix={})

        self.assertTrue(
            any(
                "does not exist in producer-consumer-matrix.md" in error
                for error in errors
            )
        )

    def test_invalid_contract_status_is_rejected(self):
        contract = {
            **self.contract,
            "status": "approved",
        }

        errors = self.validate(contract=contract)

        self.assertTrue(
            any(".status must be one of" in error for error in errors)
        )

    def test_non_string_relationship_does_not_crash(self):
        contract = {
            **self.contract,
            "relationship_type": [],
        }

        errors = self.validate(contract=contract)

        self.assertTrue(
            any(
                ".relationship_type must be one of" in error
                for error in errors
            )
        )

    def test_matrix_parser_reads_relationship(self):
        matrix_content = """\
| Producer package | Consumer package | Output consumed | Relationship | Trigger / boundary |
|---|---|---|---|---|
| `ART-API-CONTRACT` | `ART-BACKEND` | API schemas | `conditional_input` | When applicable |
"""

        with tempfile.TemporaryDirectory() as temp_dir:
            matrix_path = Path(temp_dir) / "producer-consumer-matrix.md"
            matrix_path.write_text(matrix_content, encoding="utf-8")

            errors = []
            relationships = validator.parse_relationship_matrix(
                matrix_path,
                errors,
            )

        self.assertEqual(errors, [])
        self.assertEqual(
            relationships,
            {
                ("ART-API-CONTRACT", "ART-BACKEND"): "conditional_input",
            },
        )


if __name__ == "__main__":
    unittest.main()
