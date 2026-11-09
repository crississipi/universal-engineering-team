#!/usr/bin/env python3
"""Copilot VS Code hooks: create prompt state and enforce task-report publication."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
STATE_ROOT = ROOT / ".copilot-runtime" / "task-state"
PENDING_ROOT = ROOT / ".copilot-runtime" / "task-completion-pending"
GENERATOR = ROOT / "scripts" / "report-task-completion.py"


def emit(value: dict) -> None:
    sys.stdout.write(json.dumps(value, separators=(",", ":")) + "\n")


def event_value(event: dict, camel: str, snake: str):
    return event.get(camel, event.get(snake))


def session_key(session_id: str) -> str:
    return hashlib.sha256(session_id.encode("utf-8")).hexdigest()


def parse_timestamp(value) -> datetime:
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value / 1000, tz=timezone.utc)
    if isinstance(value, str):
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("Hook timestamp must include a timezone offset.")
        return parsed.astimezone(timezone.utc)
    return datetime.now(timezone.utc)


def python_executable() -> str:
    candidates = [
        ROOT / ".venv" / "Scripts" / "python.exe",
        ROOT / ".venv" / "bin" / "python",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return sys.executable


def start(event: dict) -> int:
    session_id = event_value(event, "sessionId", "session_id")
    if not isinstance(session_id, str) or not session_id:
        raise ValueError("UserPromptSubmit event is missing a valid session ID.")
    started_at = parse_timestamp(event.get("timestamp")).isoformat().replace("+00:00", "Z")
    execution_seed = f"{session_id}:{started_at}:{uuid.uuid4().hex}"
    execution_id = "copilot-" + hashlib.sha256(execution_seed.encode()).hexdigest()[:24]
    STATE_ROOT.mkdir(parents=True, exist_ok=True)
    PENDING_ROOT.mkdir(parents=True, exist_ok=True)
    state = {
        "execution_id": execution_id,
        "session_id_hash": session_key(session_id),
        "started_at": started_at,
        "prompt_reference": "copilot-session:" + session_key(session_id)[:16],
        "report_attempts": 0,
    }
    target = STATE_ROOT / f"{session_key(session_id)}.json"
    temporary = target.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, target)
    emit({})
    return 0


def block_or_warn(state: dict, state_path: Path, reason: str) -> int:
    state["report_attempts"] = int(state.get("report_attempts", 0)) + 1
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    if state["report_attempts"] <= 3:
        emit({
            "decision": "block",
            "reason": reason + (
                "\nCreate the report input JSON at: "
                f".copilot-runtime/task-completion-pending/{state['execution_id']}.json"
                "\nRead the exact state file at: "
                f".copilot-runtime/task-state/{state['session_id_hash']}.json"
                "\nUse the task-completion schema at "
                "schemas/executions/task-completion-report.schema.json. Copy the "
                "execution_id, started_at, and prompt_reference values from that "
                "state file. Include only roles whose canonical "
                "SKILL.md content you actually read. Record exact verification "
                "outcomes; do not invent evidence. Then finish the turn so this hook "
                "can validate and publish the report."
            ),
        })
    else:
        print(
            "WARNING: Task completion report was not published after three hook retries; "
            "the turn will be allowed to end without a report.",
            file=sys.stderr,
        )
        emit({})
    return 0


def stop(event: dict) -> int:
    session_id = event_value(event, "sessionId", "session_id")
    if not isinstance(session_id, str) or not session_id:
        print("WARNING: Stop event has no session ID; report enforcement skipped.", file=sys.stderr)
        emit({})
        return 0

    key = session_key(session_id)
    state_path = STATE_ROOT / f"{key}.json"
    if not state_path.is_file():
        print("WARNING: No prompt-start state exists; report enforcement skipped.", file=sys.stderr)
        emit({})
        return 0

    state = json.loads(state_path.read_text(encoding="utf-8"))
    execution_id = state.get("execution_id")
    pending_path = PENDING_ROOT / f"{execution_id}.json"

    if not pending_path.is_file():
        return block_or_warn(state, state_path, "A terminal task-completion report input is missing.")

    try:
        report = json.loads(pending_path.read_text(encoding="utf-8"))
        if not isinstance(report, dict):
            raise ValueError("Report input must be a JSON object.")
        if report.get("execution_id") != execution_id:
            raise ValueError("Report execution_id does not match this prompt's execution ID.")
        if report.get("started_at") != state.get("started_at"):
            raise ValueError("Report started_at does not match the captured prompt-start timestamp.")
        task = report.get("task")
        if not isinstance(task, dict) or task.get("prompt_reference") != state.get("prompt_reference"):
            raise ValueError("Report task.prompt_reference does not match the captured prompt reference.")
        result = subprocess.run(
            [python_executable(), str(GENERATOR), str(pending_path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
        if result.returncode != 0:
            details = (result.stdout + "\n" + result.stderr).strip()
            raise ValueError(details or f"Report generator exited with {result.returncode}.")
        for cleanup_path in (pending_path, state_path):
            try:
                cleanup_path.unlink(missing_ok=True)
            except OSError as cleanup_error:
                print(f"WARNING: Could not remove local hook state {cleanup_path}: {cleanup_error}", file=sys.stderr)
        emit({})
        return 0
    except (OSError, ValueError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
        return block_or_warn(
            state, state_path,
            "The task-completion report could not be validated or published: " + str(exc),
        )


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1 or args[0] not in {"start", "stop"}:
        print("Usage: copilot-task-hook.py start|stop", file=sys.stderr)
        emit({})
        return 2
    try:
        raw = sys.stdin.read()
        event = json.loads(raw) if raw.strip() else {}
        if not isinstance(event, dict):
            raise ValueError("Hook event must be a JSON object.")
        return start(event) if args[0] == "start" else stop(event)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Copilot task hook error: {exc}", file=sys.stderr)
        emit({})
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
