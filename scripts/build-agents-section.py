#!/usr/bin/env python3
"""Generate or check the cross-cutting requirement section in AGENTS.md."""

from pathlib import Path
import argparse
import re
import sys

from validation_common import ROOT, requirement_id

SOURCE = ROOT / "docs/team/cross-cutting.md"
TARGET = ROOT / "AGENTS.md"

BEGIN = "<!-- BEGIN GENERATED CROSS-CUTTING REQUIREMENTS -->"
END = "<!-- END GENERATED CROSS-CUTTING REQUIREMENTS -->"


def parse_requirements():
    text = SOURCE.read_text(encoding="utf-8")
    sections = re.split(r"(?m)^## ", text)[1:]
    requirements = []

    for section in sections:
        lines = section.splitlines()

        if not lines:
            continue

        heading = lines[0].strip()
        match = re.match(
            r"^(REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*)\s+—\s+(.+)$",
            heading,
        )

        if not match:
            continue

        req_id, title = match.groups()
        body = "\n".join(lines[1:])

        if f"<!-- {req_id} -->" not in body:
            raise ValueError(f"Missing canonical anchor for {req_id}")

        statement = re.search(r"(?m)^Requirement:\s*(.+)$", body)

        if not statement:
            raise ValueError(f"Missing Requirement: statement for {req_id}")

        if not requirement_id(req_id):
            raise ValueError(f"Invalid requirement ID: {req_id}")

        requirements.append((req_id, title, statement.group(1).strip()))

    if not requirements:
        raise ValueError("No valid requirements found in cross-cutting.md")

    ids = [item[0] for item in requirements]

    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate requirement IDs in cross-cutting.md")

    return requirements


def render(requirements):
    lines = [
        BEGIN,
        "## Cross-cutting requirements",
        "",
    ]

    for req_id, title, statement in requirements:
        lines.extend(
            [
                f"<!-- {req_id} -->",
                f"- **{title}:** {statement}",
                "",
            ]
        )

    lines.append(END)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    try:
        requirements = parse_requirements()
        generated = render(requirements)
        content = TARGET.read_text(encoding="utf-8")

        has_begin = BEGIN in content
        has_end = END in content

        if has_begin != has_end:
            raise ValueError("AGENTS.md contains an incomplete generated section")

        if has_begin:
            start = content.index(BEGIN)
            finish = content.index(END, start) + len(END)
            updated = content[:start] + generated + content[finish:]
        else:
            anchor = "## Definition of done"

            if anchor not in content:
                raise ValueError(
                    "Could not find '## Definition of done' in AGENTS.md"
                )

            updated = content.replace(
                anchor,
                generated + "\n\n" + anchor,
                1,
            )

        if args.write:
            TARGET.write_text(updated.rstrip() + "\n", encoding="utf-8")
            print("Generated cross-cutting section written to AGENTS.md")
            return 0

        if content != updated:
            print(
                "AGENTS.md is out of sync. Run "
                "python scripts/build-agents-section.py --write"
            )
            return 1

        print("AGENTS.md generated section is synchronized.")
        return 0

    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())