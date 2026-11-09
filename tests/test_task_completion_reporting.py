"""Tests for task completion report validation and rendering."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def load_script(name, filename):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


reporter = load_script("report_task_completion", "report-task-completion.py")


class TaskCompletionReportingTests(unittest.TestCase):
    def valid_report(self):
        return {
            "schema_version": 1,
            "execution_id": "EXE-test-001",
            "task": {"objective": "Implement a small API change", "prompt_reference": "prompt-001"},
            "status": "completed",
            "started_at": "2026-11-09T10:00:00Z",
            "completed_at": "2026-11-09T10:05:00Z",
            "summary": "The API change was implemented.",
            "activated_roles": [{
                "role": "backend-developer",
                "skill_path": "skills/backend-developer/SKILL.md",
                "skill_revision": "abc123",
                "skill_loaded": True,
                "contribution": "Implemented the API change."
            }],
            "deliverables": [{
                "path": "src/api/example.py",
                "action": "modified",
                "description": "Updated the handler."
            }],
            "verification": [{
                "check": "unit tests",
                "status": "passed",
                "result": "12 tests passed",
                "evidence_reference": "test-output.txt"
            }],
            "decisions": [],
            "issues": [],
            "next_steps": []
        }

    def test_valid_report_is_accepted_and_rendered(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            source = Path(temp) / "input.json"
            source.write_text(json.dumps(self.valid_report()), encoding="utf-8")
            report = reporter.load_and_validate(source)
            markdown = reporter.render_markdown(report)
            self.assertIn("Task Completion Report: EXE-test-001", markdown)
            self.assertIn("backend-developer", markdown)
            self.assertIn("unit tests", markdown)

    def test_missing_role_skill_is_rejected(self):
        report = self.valid_report()
        report["activated_roles"][0]["skill_path"] = "skills/frontend-developer/SKILL.md"
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            source = Path(temp) / "input.json"
            source.write_text(json.dumps(report), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "canonical path"):
                reporter.load_and_validate(source)

    def test_unloaded_skill_is_rejected_by_schema(self):
        report = self.valid_report()
        report["activated_roles"][0]["skill_loaded"] = False
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            source = Path(temp) / "input.json"
            source.write_text(json.dumps(report), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "skill_loaded"):
                reporter.load_and_validate(source)

    def test_completion_cannot_precede_start(self):
        report = self.valid_report()
        report["completed_at"] = "2026-11-09T09:59:00Z"
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            source = Path(temp) / "input.json"
            source.write_text(json.dumps(report), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must not precede"):
                reporter.load_and_validate(source)

    def test_existing_report_is_never_overwritten(self):
        report = self.valid_report()
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            reporter.write_report(report, Path(temp))
            with self.assertRaises(FileExistsError):
                reporter.write_report(report, Path(temp))

    def test_blocked_and_failed_tasks_can_be_reported(self):
        for status in ("blocked", "failed", "completed_with_warnings"):
            report = self.valid_report()
            report["status"] = status
            with tempfile.TemporaryDirectory(dir=ROOT) as temp:
                source = Path(temp) / "input.json"
                source.write_text(json.dumps(report), encoding="utf-8")
                self.assertEqual(reporter.load_and_validate(source)["status"], status)


if __name__ == "__main__":
    unittest.main()
