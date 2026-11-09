import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
import sys

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "copilot-task-hook.py"
SPEC = importlib.util.spec_from_file_location("copilot_task_hook", SCRIPT)
hook = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = hook
SPEC.loader.exec_module(hook)


class CopilotTaskHookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        hook.ROOT = root
        hook.STATE_ROOT = root / ".copilot-runtime/task-state"
        hook.PENDING_ROOT = root / ".copilot-runtime/task-completion-pending"
        hook.GENERATOR = root / "scripts/report-task-completion.py"
        self.session_id = "test-session-123"
        self.event = {
            "sessionId": self.session_id,
            "timestamp": 1794225600000,
            "prompt": "sensitive prompt text must not be persisted",
        }

    def tearDown(self):
        self.temp.cleanup()

    def invoke(self, fn, event):
        output = io.StringIO()
        with redirect_stdout(output):
            result = fn(event)
        return result, json.loads(output.getvalue())

    def test_start_creates_state_without_storing_prompt_text(self):
        code, output = self.invoke(hook.start, self.event)
        self.assertEqual(code, 0)
        self.assertEqual(output, {})
        state_path = hook.STATE_ROOT / f"{hook.session_key(self.session_id)}.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertTrue(state["execution_id"].startswith("copilot-"))
        self.assertNotIn("sensitive prompt text", state_path.read_text(encoding="utf-8"))

    def test_stop_blocks_when_report_is_missing(self):
        self.invoke(hook.start, self.event)
        code, output = self.invoke(hook.stop, {"sessionId": self.session_id})
        self.assertEqual(code, 0)
        self.assertEqual(output["decision"], "block")
        self.assertIn(".copilot-runtime/task-completion-pending/", output["reason"])

    def test_stop_publishes_matching_pending_report(self):
        self.invoke(hook.start, self.event)
        state_path = hook.STATE_ROOT / f"{hook.session_key(self.session_id)}.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        hook.PENDING_ROOT.mkdir(parents=True, exist_ok=True)
        pending = hook.PENDING_ROOT / f"{state['execution_id']}.json"
        pending.write_text(json.dumps({
            "execution_id": state["execution_id"],
            "started_at": state["started_at"],
            "task": {"prompt_reference": state["prompt_reference"]},
        }), encoding="utf-8")
        with patch.object(hook, "python_executable", return_value="python"):
            with patch.object(hook.subprocess, "run", return_value=type("R", (), {
                "returncode": 0, "stdout": "", "stderr": ""
            })()) as run:
                code, output = self.invoke(hook.stop, {"sessionId": self.session_id})
        self.assertEqual(code, 0)
        self.assertEqual(output, {})
        run.assert_called_once()
        self.assertFalse(pending.exists())
        self.assertFalse(state_path.exists())


if __name__ == "__main__":
    unittest.main()
