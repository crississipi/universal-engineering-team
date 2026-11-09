#!/usr/bin/env python3
"""Validate and render one structured task-completion report."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys

from jsonschema import Draft202012Validator, FormatChecker

from validation_common import ROOT

SCHEMA_PATH = ROOT / "schemas/executions/task-completion-report.schema.json"
REPORT_ROOT = ROOT / "reports/task-completions"
EXECUTION_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,127}$")


def load_and_validate(input_path: Path):
    try:
        report = json.loads(input_path.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not read JSON input or schema: {exc}") from exc

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(
        validator.iter_errors(report),
        key=lambda error: (list(map(str, error.absolute_path)), error.message),
    )
    if errors:
        details = []
        for error in errors:
            location = ".".join(str(part) for part in error.absolute_path) or "<document>"
            details.append(f"{location}: {error.message}")
        raise ValueError("Task completion report is invalid:\n- " + "\n- ".join(details))

    if report["completed_at"] < report["started_at"]:
        raise ValueError("completed_at must not precede started_at")

    for role in report["activated_roles"]:
        expected_path = f"skills/{role['role']}/SKILL.md"
        if role["skill_path"] != expected_path:
            raise ValueError(
                f"{role['role']}: skill_path must be the canonical path {expected_path}"
            )
        if not (ROOT / expected_path).is_file():
            raise ValueError(f"{role['role']}: canonical skill file does not exist: {expected_path}")

    return report


def render_markdown(report: dict) -> str:
    lines = [
        f"# Task Completion Report: {report['execution_id']}",
        "",
        f"**Status:** {report['status']}",
        f"**Started:** {report['started_at']}",
        f"**Completed:** {report['completed_at']}",
        "",
        "## Task",
        "",
        report["task"]["objective"],
        "",
        f"**Prompt reference:** {report['task']['prompt_reference'] or 'Not supplied'}",
        "",
        "## Outcome",
        "",
        report["summary"],
        "",
        "## Activated roles and skills",
        "",
    ]

    if report["activated_roles"]:
        for role in report["activated_roles"]:
            lines.extend([
                f"### {role['role']}",
                f"- Skill: `{role['skill_path']}`",
                f"- Skill revision: {role['skill_revision'] or 'Not recorded'}",
                f"- Skill loaded: {str(role['skill_loaded']).lower()}",
                f"- Contribution: {role['contribution']}",
                "",
            ])
    else:
        lines.extend(["No specialist role was activated.", ""])

    lines.extend(["## Deliverables", ""])
    if report["deliverables"]:
        for item in report["deliverables"]:
            lines.append(f"- **{item['action']}** `{item['path']}` — {item['description']}")
    else:
        lines.append("No file or external deliverable was recorded.")
    lines.extend(["", "## Verification", ""])
    if report["verification"]:
        for check in report["verification"]:
            lines.append(
                f"- **{check['status']}** {check['check']}: {check['result']}"
                + (f" (Evidence: {check['evidence_reference']})" if check["evidence_reference"] else "")
            )
    else:
        lines.append("No verification checks were recorded.")
    lines.extend(["", "## Decisions", ""])
    if report["decisions"]:
        for item in report["decisions"]:
            lines.extend([
                f"- **{item['decision']}**",
                f"  - Authority: {item['authority'] or 'Not recorded'}",
                f"  - Rationale: {item['rationale']}",
                f"  - Evidence: {item['evidence_reference'] or 'Not supplied'}",
            ])
    else:
        lines.append("No decisions were recorded.")
    lines.extend(["", "## Issues and warnings", ""])
    if report["issues"]:
        for item in report["issues"]:
            lines.append(
                f"- **{item['severity']}** (blocking={str(item['blocking']).lower()}): "
                f"{item['description']}"
            )
    else:
        lines.append("No issues were recorded.")
    lines.extend(["", "## Next steps", ""])
    if report["next_steps"]:
        lines.extend(f"- {step}" for step in report["next_steps"])
    else:
        lines.append("None recorded.")
    lines.append("")
    return "\n".join(lines)


def write_report(report: dict, output_root: Path = REPORT_ROOT):
    execution_id = report["execution_id"]
    if not EXECUTION_ID_RE.fullmatch(execution_id):
        raise ValueError("execution_id contains unsupported characters")
    destination = output_root / execution_id
    destination.mkdir(parents=True, exist_ok=True)
    json_path = destination / "report.json"
    markdown_path = destination / "report.md"
    if json_path.exists() or markdown_path.exists():
        raise FileExistsError(
            f"Report already exists for {execution_id}; use a new execution ID. "
            "Existing reports are not overwritten."
        )

    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(render_markdown(report), encoding="utf-8")
    return json_path, markdown_path


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate and render one terminal task-completion report."
    )
    parser.add_argument("input_json", help="Path to a JSON task-completion record.")
    parser.add_argument(
        "--output-root",
        help="Optional output root (default: reports/task-completions).",
    )
    args = parser.parse_args(argv)

    try:
        report = load_and_validate(Path(args.input_json))
        output_root = Path(args.output_root).resolve() if args.output_root else REPORT_ROOT
        json_path, markdown_path = write_report(report, output_root)
    except (OSError, ValueError, FileExistsError) as exc:
        print(f"ERROR: {exc}")
        return 2

    print(f"Task completion report created: {json_path.relative_to(ROOT) if json_path.is_relative_to(ROOT) else json_path}")
    print(f"Human-readable report created: {markdown_path.relative_to(ROOT) if markdown_path.is_relative_to(ROOT) else markdown_path}")
    print(f"Status: {report['status']}")
    print("This generator validates report structure; it does not authenticate execution claims.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
