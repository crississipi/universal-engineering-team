#!/usr/bin/env python3
"""Validate scenario specifications and one-to-one review records."""

from pathlib import Path
import re
import sys

from validation_common import (
    ROOT,
    expected_roles,
    load_yaml,
    report,
    requirement_id,
    safe_repo_path,
)

SCENARIO_DIR = ROOT / "tests/scenarios"
REVIEW_DIR = ROOT / "docs/reviews"

SCENARIO_ID_RE = re.compile(r"^SCEN-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
CRITERION_ID_RE = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)*$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")

SCENARIO_STATUSES = {"draft", "approved"}
REVIEW_DECISIONS = {"pass", "needs_changes", "blocked"}


def yaml_files(folder):
    if not folder.exists():
        return []

    return sorted(
        list(folder.rglob("*.yml")) + list(folder.rglob("*.yaml"))
    )


def main():
    errors, warnings = [], []
    roles = set(expected_roles())

    scenario_paths = yaml_files(SCENARIO_DIR)
    review_paths = yaml_files(REVIEW_DIR)

    scenarios = {}
    declared_review_paths = {}

    for path in scenario_paths:
        try:
            data = load_yaml(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        if not isinstance(data, dict):
            errors.append(f"{path.relative_to(ROOT)} must contain a mapping")
            continue

        scenario_id = data.get("id")
        role = data.get("role")
        status = data.get("status")
        required = data.get("required_requirements")
        criteria = data.get("criteria")
        review_record = data.get("review_record")
        evidence = data.get("evidence")

        if (
            not isinstance(scenario_id, str)
            or not SCENARIO_ID_RE.fullmatch(scenario_id)
        ):
            errors.append(f"{path.relative_to(ROOT)} has an invalid scenario ID")
            continue

        if scenario_id in scenarios:
            errors.append(f"Duplicate scenario ID: {scenario_id}")
            continue

        scenarios[scenario_id] = path

        if not isinstance(role, str) or role not in roles:
            errors.append(f"{scenario_id}: role is not a canonical role")

        if not isinstance(status, str) or status not in SCENARIO_STATUSES:
            errors.append(f"{scenario_id}: status must be draft or approved")

        if (
            not isinstance(required, list)
            or any(not requirement_id(value) for value in required)
            or len(required) != len(set(required))
        ):
            errors.append(
                f"{scenario_id}: required_requirements must be a unique "
                "list of valid REQ IDs"
            )
            required_set = set()
        else:
            required_set = set(required)

        if not isinstance(criteria, list) or not criteria:
            errors.append(f"{scenario_id}: criteria must be a non-empty list")
            criteria = []

        criterion_ids = set()

        for index, criterion in enumerate(criteria):
            label = f"{scenario_id}.criteria[{index}]"

            if not isinstance(criterion, dict):
                errors.append(f"{label} must be a mapping")
                continue

            criterion_id = criterion.get("id")
            description = criterion.get("description")
            weight = criterion.get("weight")
            critical = criterion.get("critical")
            requirement_ref = criterion.get("requirement_ref")

            if (
                not isinstance(criterion_id, str)
                or not CRITERION_ID_RE.fullmatch(criterion_id)
            ):
                errors.append(f"{label}.id is invalid")
            elif criterion_id in criterion_ids:
                errors.append(
                    f"{scenario_id}: duplicate criterion ID {criterion_id}"
                )
            else:
                criterion_ids.add(criterion_id)

            if not isinstance(description, str) or not description.strip():
                errors.append(f"{label}.description must be non-empty")

            if (
                not isinstance(weight, (int, float))
                or isinstance(weight, bool)
                or weight <= 0
            ):
                errors.append(f"{label}.weight must be a positive number")

            if not isinstance(critical, bool):
                errors.append(f"{label}.critical must be true or false")

            if (
                not requirement_id(requirement_ref)
                or requirement_ref not in required_set
            ):
                errors.append(
                    f"{label}.requirement_ref must appear in "
                    "required_requirements"
                )

        expected_record = f"docs/reviews/scenario-{scenario_id}.yml"

        if status == "approved" and review_record != expected_record:
            errors.append(
                f"{scenario_id}: approved scenarios require review_record "
                f"to equal {expected_record}"
            )
        elif review_record is None:
            if status == "approved":
                errors.append(
                    f"{scenario_id}: approved scenarios require a review record"
                )
        elif review_record != expected_record:
            errors.append(
                f"{scenario_id}: review_record must equal {expected_record} "
                "when supplied"
            )
        else:
            try:
                review_path = safe_repo_path(
                    review_record,
                    required_prefix=REVIEW_DIR,
                )
                declared_review_paths[scenario_id] = review_path

                if not review_path.is_file():
                    errors.append(
                        f"{scenario_id}: missing review record {review_record}"
                    )
            except ValueError as exc:
                errors.append(f"{scenario_id}: {exc}")

        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{scenario_id}: evidence must be a non-empty list")
            evidence = []

        for index, item in enumerate(evidence):
            label = f"{scenario_id}.evidence[{index}]"

            if not isinstance(item, dict):
                errors.append(f"{label} must be a mapping")
                continue

            raw_path = item.get("path")
            commit = item.get("commit")

            expected_skill = (
                f"skills/{role}/SKILL.md" if isinstance(role, str) else None
            )

            if raw_path != expected_skill:
                errors.append(f"{label}.path must equal {expected_skill!r}")
                continue

            try:
                skill_path = safe_repo_path(
                    raw_path,
                    required_prefix=ROOT / "skills",
                )

                if not skill_path.is_file():
                    errors.append(f"{label}: evidence skill file does not exist")
                else:
                    skill_text = skill_path.read_text(encoding="utf-8")

                    for req_id in required_set:
                        anchor = f"<!-- {req_id} -->"

                        if anchor not in skill_text:
                            errors.append(
                                f"{label}: missing exact anchor {anchor}"
                            )
            except (ValueError, OSError) as exc:
                errors.append(f"{label}: {exc}")

            if not isinstance(commit, str) or not SHA_RE.fullmatch(commit):
                errors.append(
                    f"{label}.commit must be a full lowercase 40-character SHA"
                )

    review_ids = {}

    for path in review_paths:
        try:
            data = load_yaml(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        if not isinstance(data, dict):
            errors.append(f"{path.relative_to(ROOT)} must contain a mapping")
            continue

        scenario_id = data.get("scenario_id")

        if not isinstance(scenario_id, str):
            errors.append(
                f"{path.relative_to(ROOT)} must contain scenario_id"
            )
            continue

        if scenario_id in review_ids:
            errors.append(f"Multiple review records for {scenario_id}")
        else:
            review_ids[scenario_id] = path.resolve()

        if scenario_id not in scenarios:
            errors.append(
                f"Orphan review record: {path.relative_to(ROOT)}"
            )

        decision = data.get("decision")
        reviewer = data.get("reviewer")
        runs = data.get("runs")

        if (
            not isinstance(decision, str)
            or decision not in REVIEW_DECISIONS
        ):
            errors.append(
                f"{path.relative_to(ROOT)}: invalid review decision"
            )

        if not isinstance(reviewer, str) or not reviewer.strip():
            errors.append(
                f"{path.relative_to(ROOT)}: reviewer must be non-empty"
            )

        if not isinstance(runs, int) or isinstance(runs, bool) or runs < 1:
            errors.append(
                f"{path.relative_to(ROOT)}: runs must be a positive integer"
            )

    for scenario_id in scenarios:
        declared = declared_review_paths.get(scenario_id)
        actual = review_ids.get(scenario_id)

        if declared is None:
            continue

        if actual is None:
            errors.append(f"{scenario_id}: no matching review record found")
        elif actual != declared.resolve():
            errors.append(
                f"{scenario_id}: review record does not match declared path"
            )

    if not scenario_paths and not review_paths:
        warnings.append(
            "No scenarios or review records exist yet; evaluation has not been "
            "initialized. Do not fabricate evaluation data."
        )

    return report(errors, warnings, "Scenario validation")


if __name__ == "__main__":
    sys.exit(main())