#!/usr/bin/env python3
"""Validate unique, role-scoped requirement anchors and baseline traceability."""

from pathlib import Path
import re
import sys

from validation_common import ROOT, expected_roles, report, requirement_id

ANCHOR_RE = re.compile(r"(?m)^<!-- (REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*) -->$")
IDENTITY_RE = re.compile(
    r"(?ms)^## 1\. Identity and boundaries\s*\n(.*?)(?=^## |\Z)"
)
BASELINE_REGISTER = Path("docs/evaluation/baseline/README.md")


def validate_requirement_anchors(root=ROOT, roles=None):
    """Return structural traceability errors for canonical role skills."""
    errors = []
    roles = expected_roles() if roles is None else roles
    if not isinstance(roles, list) or not roles:
        return ["Canonical role inventory must be a non-empty list"]

    baseline_path = root / BASELINE_REGISTER
    try:
        baseline_lines = baseline_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        return [f"Cannot read {BASELINE_REGISTER.as_posix()}: {exc}"]

    baseline_rows = {}
    for line in baseline_lines:
        if not line.startswith("|"):
            continue
        columns = [value.strip() for value in line.split("|")[1:-1]]
        if len(columns) == 5 and columns[0] in roles:
            if columns[0] in baseline_rows:
                errors.append(
                    f"Baseline register contains duplicate rows for {columns[0]}"
                )
            baseline_rows[columns[0]] = columns

    seen_ids = {}
    for role in roles:
        skill_path = root / "skills" / role / "SKILL.md"
        try:
            content = skill_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{skill_path.as_posix()}: cannot read role skill: {exc}")
            continue

        markers = list(ANCHOR_RE.finditer(content))
        if len(markers) != 1:
            errors.append(
                f"{skill_path.as_posix()}: expected exactly one role requirement "
                f"anchor; found {len(markers)}"
            )
            continue

        marker = markers[0]
        requirement = marker.group(1)
        if not requirement_id(requirement):
            errors.append(
                f"{skill_path.as_posix()}: invalid requirement ID {requirement!r}"
            )
            continue

        previous = seen_ids.get(requirement)
        if previous:
            errors.append(
                f"Duplicate requirement ID {requirement}: {previous} and {role}"
            )
        else:
            seen_ids[requirement] = role

        identity = IDENTITY_RE.search(content)
        if not identity:
            errors.append(
                f"{skill_path.as_posix()}: missing Identity and boundaries section"
            )
            continue

        identity_markers = list(ANCHOR_RE.finditer(identity.group(1)))
        if len(identity_markers) != 1 or identity_markers[0].group(1) != requirement:
            errors.append(
                f"{skill_path.as_posix()}: {requirement} must appear in "
                "Identity and boundaries"
            )

        following_lines = content[marker.end():].splitlines()
        next_content = next((line.strip() for line in following_lines if line.strip()), "")
        if not next_content or next_content.startswith(("## ", "<!--")):
            errors.append(
                f"{skill_path.as_posix()}: {requirement} must be followed by "
                "its role requirement statement"
            )

        row = baseline_rows.get(role)
        expected_scenario = f"SCEN-BASELINE-{role.upper()}"
        if not row:
            errors.append(
                f"{BASELINE_REGISTER.as_posix()}: missing baseline row for {role}"
            )
            continue
        if row[2] != expected_scenario:
            errors.append(
                f"{BASELINE_REGISTER.as_posix()}: {role} scenario ID must be "
                f"{expected_scenario}"
            )
        if requirement not in row[3]:
            errors.append(
                f"{BASELINE_REGISTER.as_posix()}: {role} row must reference "
                f"{requirement}"
            )

    return errors


def main():
    try:
        errors = validate_requirement_anchors()
    except ValueError as exc:
        errors = [str(exc)]

    if errors:
        return report(errors, [], "Requirement traceability validation")

    print(
        "Requirement traceability passed: all canonical role anchors are "
        "unique, correctly placed, and mapped to the baseline register."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
