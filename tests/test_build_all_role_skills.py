"""Tests for canonical consolidated role-skill generation."""

from pathlib import Path
import importlib.util
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build-all-role-skills.py"
spec = importlib.util.spec_from_file_location("build_all_role_skills", SCRIPT)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ConsolidatedRoleSkillsTests(unittest.TestCase):
    def make_repo(self, roles, skills):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "docs/team").mkdir(parents=True)
        (root / "skills").mkdir()
        role_lines = "\n".join(f"  - {role}" for role in roles)
        (root / "docs/team/expected-roles.yml").write_text(
            f"version: 1\nroles:\n{role_lines}\n", encoding="utf-8"
        )
        for role, content in skills.items():
            folder = root / "skills" / role
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(content, encoding="utf-8")
        return temp, root

    def test_render_uses_canonical_skill_content_and_expected_order(self):
        temp, root = self.make_repo(
            ["alpha-role", "beta-role"],
            {
                "alpha-role": "---\nname: alpha-role\ndescription: Alpha\n---\n\n# Alpha Role\n\nCanonical alpha.",
                "beta-role": "---\nname: beta-role\ndescription: Beta\n---\n\n# Beta Role\n\nCanonical beta.",
            },
        )
        with temp:
            output = builder.render(root)
        self.assertLess(output.index("<!-- ROLE: alpha-role -->"), output.index("<!-- ROLE: beta-role -->"))
        self.assertIn("Canonical alpha.", output)
        self.assertIn("Canonical beta.", output)
        self.assertIn(builder.BEGIN, output)
        self.assertIn(builder.END, output)

    def test_missing_skill_is_rejected(self):
        temp, root = self.make_repo(["missing-role"], {})
        with temp, self.assertRaisesRegex(ValueError, "Missing canonical skill"):
            builder.render(root)

    def test_frontmatter_role_mismatch_is_rejected(self):
        temp, root = self.make_repo(
            ["alpha-role"],
            {"alpha-role": "---\nname: beta-role\ndescription: Wrong\n---\n\n# Alpha\n"},
        )
        with temp, self.assertRaisesRegex(ValueError, "frontmatter name"):
            builder.render(root)

    def test_duplicate_role_is_rejected(self):
        temp, root = self.make_repo(["alpha-role", "alpha-role"], {
            "alpha-role": "---\nname: alpha-role\ndescription: Alpha\n---\n\n# Alpha\n"
        })
        with temp, self.assertRaisesRegex(ValueError, "duplicate role"):
            builder.render(root)


if __name__ == "__main__":
    unittest.main()
