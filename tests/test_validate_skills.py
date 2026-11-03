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


if __name__ == "__main__":
    unittest.main()
