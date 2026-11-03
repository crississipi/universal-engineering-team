"""Tests for the integrated execution validator."""

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
import sys
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

spec = importlib.util.spec_from_file_location(
    "validate_execution", SCRIPTS / "validate-execution.py"
)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class IntegratedExecutionValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT)
        self.directory = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def write_records(self):
        for filename, (wrapper, _) in validator.RECORD_FILES.items():
            payload = [] if filename not in {"execution.yml", "closure.yml"} else {}
            (self.directory / filename).write_text(
                f"{wrapper}: " + ("[]" if isinstance(payload, list) else "{}") + "\n",
                encoding="utf-8",
            )

    def test_schema_catalog_loads_all_ten_record_schemas(self):
        catalog, registry = validator.load_schema_catalog()
        self.assertEqual(set(catalog), set(validator.RECORD_FILES))
        self.assertIsNotNone(registry)

    def test_duplicate_yaml_keys_are_rejected(self):
        path = self.directory / "duplicate.yml"
        path.write_text("execution:\n  status: planned\n  status: released\n", encoding="utf-8")
        with self.assertRaises(Exception) as context:
            validator.load_yaml_document(path)
        self.assertIn("duplicate key", str(context.exception))

    def test_all_required_documents_parse_with_canonical_wrappers(self):
        self.write_records()
        records, errors = validator.parse_execution_documents(self.directory)
        self.assertEqual(errors, [])
        self.assertEqual(set(records), set(validator.RECORD_FILES))

    def test_missing_and_malformed_documents_are_reported(self):
        self.write_records()
        (self.directory / "execution.yml").write_text("execution: [", encoding="utf-8")
        (self.directory / "closure.yml").unlink()
        _, errors = validator.parse_execution_documents(self.directory)
        self.assertTrue(any("[EXV002]" in error for error in errors))
        self.assertTrue(any("[EXV003]" in error for error in errors))

    def test_invalid_record_shape_produces_schema_finding(self):
        self.write_records()
        records, parse_errors = validator.parse_execution_documents(self.directory)
        catalog, registry = validator.load_schema_catalog()
        self.assertEqual(parse_errors, [])
        errors = validator.validate_documents(self.directory, records, catalog, registry)
        self.assertTrue(any("[EXV005]" in error for error in errors))

    def test_schema_failure_skips_cross_record_and_lifecycle(self):
        self.write_records()
        catalog, registry = validator.load_schema_catalog()
        with patch.object(validator, "validate_documents", return_value=["[EXV005] invalid schema instance"]), \
             patch.object(validator, "load_existing_validator") as load_validator:
            result = validator.validate_execution(
                self.directory, catalog, registry,
            )
        self.assertEqual(result["checks"]["schema"], "failed")
        self.assertEqual(result["checks"]["cross_record"], "skipped")
        self.assertEqual(result["checks"]["lifecycle"], "skipped")
        load_validator.assert_not_called()

    def test_parse_failure_skips_all_dependent_checks(self):
        self.write_records()
        (self.directory / "closure.yml").unlink()
        with patch.object(validator, "load_schema_catalog") as load_schemas, \
             patch.object(validator, "load_existing_validator") as load_validator:
            result = validator.validate_execution(self.directory)
        self.assertEqual(result["checks"]["parsing"], "failed")
        self.assertEqual(result["checks"]["schema"], "skipped")
        self.assertEqual(result["checks"]["cross_record"], "skipped")
        self.assertEqual(result["checks"]["lifecycle"], "skipped")
        load_schemas.assert_not_called()
        load_validator.assert_not_called()

    def test_both_existing_validators_run_after_parse_and_schema_pass(self):
        self.write_records()
        catalog, registry = validator.load_schema_catalog()
        fake_records = {
            filename: {wrapper: [] if filename not in {"execution.yml", "closure.yml"} else {}}
            for filename, (wrapper, _) in validator.RECORD_FILES.items()
        }
        fake_validators = (
            ("cross_record", "references.py", "references"),
            ("lifecycle", "lifecycle.py", "lifecycle"),
        )
        with patch.object(validator, "parse_execution_documents", return_value=(fake_records, [])), \
             patch.object(validator, "validate_documents", return_value=[]), \
             patch.object(validator, "load_existing_validator", return_value=lambda directory: 0) as load_validator:
            result = validator.validate_execution(
                self.directory, catalog, registry, validators=fake_validators,
            )
        self.assertEqual(result["checks"]["schema"], "passed")
        self.assertEqual(result["checks"]["cross_record"], "passed")
        self.assertEqual(result["checks"]["lifecycle"], "passed")
        self.assertEqual(load_validator.call_count, 2)

    def test_execution_path_must_be_direct_child_of_executions(self):
        with self.assertRaises(ValueError):
            validator.resolve_execution_directory("../outside")


if __name__ == "__main__":
    unittest.main()
