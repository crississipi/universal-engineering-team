import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

SPEC = importlib.util.spec_from_file_location(
    "sync_copilot_skills", SCRIPTS / "sync-copilot-skills.py"
)
if SPEC is None or SPEC.loader is None:
    raise ImportError("Could not load scripts/sync-copilot-skills.py")
SYNC_MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SYNC_MODULE
SPEC.loader.exec_module(SYNC_MODULE)
synchronize = SYNC_MODULE.synchronize


class CopilotSkillSyncTests(unittest.TestCase):
    def make_repo(self, root: Path):
        (root / "docs/team").mkdir(parents=True)
        (root / "docs/team/expected-roles.yml").write_text(
            "roles:\n  - backend-developer\n  - qa-manager\n", encoding="utf-8"
        )
        for role in ("backend-developer", "qa-manager"):
            folder = root / "skills" / role
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(
                f"---\nname: {role}\ndescription: Test skill.\n---\n# {role}\n",
                encoding="utf-8",
            )
            (folder / "references").mkdir()
            (folder / "references/example.md").write_text("reference", encoding="utf-8")

    def test_write_copies_full_skill_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            self.assertEqual(synchronize(root, write=True), [])
            self.assertEqual(
                (root / ".github/skills/backend-developer/references/example.md").read_text(),
                "reference",
            )
            self.assertEqual(synchronize(root), [])

    def test_check_detects_modified_mirror(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            synchronize(root, write=True)
            (root / ".github/skills/qa-manager/SKILL.md").write_text("drift", encoding="utf-8")
            self.assertTrue(any("out of sync" in item for item in synchronize(root)))

    def test_refuses_unmarked_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            (root / ".github/skills").mkdir(parents=True)
            (root / ".github/skills/custom").mkdir()
            with self.assertRaisesRegex(ValueError, "without the generator marker"):
                synchronize(root, write=True)


if __name__ == "__main__":
    unittest.main()
