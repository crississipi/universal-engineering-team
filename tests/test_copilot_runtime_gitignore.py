import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CopilotRuntimeGitIgnoreTests(unittest.TestCase):
    def test_runtime_state_and_pending_reports_are_gitignored(self):
        paths = (
            ".copilot-runtime/task-state/test.json",
            ".copilot-runtime/task-completion-pending/test.json",
        )
        for path in paths:
            with self.subTest(path=path):
                result = subprocess.run(
                    ["git", "check-ignore", "--no-index", "--", path],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(
                    result.returncode,
                    0,
                    msg=(
                        f"{path} is not ignored by .gitignore. "
                        f"stdout={result.stdout!r}, stderr={result.stderr!r}"
                    ),
                )


if __name__ == "__main__":
    unittest.main()
