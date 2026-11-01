#!/usr/bin/env python3
"""Validate explicit artifact ownership records."""

import sys

from validation_common import ROOT, expected_roles, load_yaml, report, safe_repo_path

MANIFEST = ROOT / "docs/team/ownership.yml"
CLASSIFICATIONS = {"internal", "external_input", "terminal_output", "shared"}
STATUSES = {"proposed", "active", "deprecated"}


def main():
    errors, warnings = [], []

    try:
        data = load_yaml(MANIFEST)
        roles = set(expected_roles())

        if not isinstance(data, dict):
            raise ValueError("ownership.yml must contain a YAML mapping")

        if data.get("roles") != expected_roles():
            errors.append(
                "ownership.yml roles must match expected-roles.yml in order"
            )

        artifacts = data.get("artifacts")

        if not isinstance(artifacts, list):
            errors.append("ownership.yml artifacts must be a list")
            artifacts = []

        seen_ids = set()

        for index, item in enumerate(artifacts):
            label = f"artifacts[{index}]"

            if not isinstance(item, dict):
                errors.append(f"{label} must be a mapping")
                continue

            artifact_id = item.get("id")
            owner = item.get("owner")
            producer = item.get("primary_producer")
            contributors = item.get("contributors", [])
            classification = item.get("classification")
            status = item.get("status", "proposed")
            paths = item.get("paths", [])

            if not isinstance(artifact_id, str) or not artifact_id.strip():
                errors.append(f"{label}.id must be a non-empty string")
            elif artifact_id in seen_ids:
                errors.append(f"Duplicate artifact ID: {artifact_id}")
            else:
                seen_ids.add(artifact_id)

            if not isinstance(owner, str) or owner not in roles:
                errors.append(f"{label}.owner must be a canonical role")

            if not isinstance(producer, str) or producer not in roles:
                errors.append(
                    f"{label}.primary_producer must be a canonical role"
                )

            if (
                not isinstance(contributors, list)
                or any(
                    not isinstance(role, str) or role not in roles
                    for role in contributors
                )
            ):
                errors.append(
                    f"{label}.contributors must contain valid role slugs"
                )

            if (
                not isinstance(classification, str)
                or classification not in CLASSIFICATIONS
            ):
                errors.append(f"{label}.classification is invalid")

            if not isinstance(status, str) or status not in STATUSES:
                errors.append(f"{label}.status is invalid")

            if not isinstance(paths, list):
                errors.append(f"{label}.paths must be a list")
            else:
                for raw_path in paths:
                    try:
                        safe_repo_path(raw_path)
                    except ValueError as exc:
                        errors.append(f"{label}: {exc}")

        if not artifacts:
            warnings.append(
                "No artifact records exist yet; add them only after ownership "
                "has been verified."
            )

        return report(errors, warnings, "Artifact ownership validation")

    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())