#!/usr/bin/env python3
"""Validate directional artifact handoffs between canonical roles."""

from pathlib import Path
import sys

from validation_common import expected_roles, load_yaml, report

MANIFEST = Path(__file__).resolve().parents[1] / "docs/team/ownership.yml"

def main():
    errors, warnings = [], []

    try:
        data = load_yaml(MANIFEST)

        if not isinstance(data, dict):
            raise ValueError("ownership.yml must contain a YAML mapping")

        roles = set(expected_roles())
        artifacts = data.get("artifacts", [])
        handoffs = data.get("handoffs")

        if not isinstance(artifacts, list):
            errors.append("ownership.yml artifacts must be a list")
            artifacts = []

        if not isinstance(handoffs, list):
            errors.append("ownership.yml handoffs must be a list")
            handoffs = []

        artifact_ids = {
            item["id"]
            for item in artifacts
            if isinstance(item, dict)
            and isinstance(item.get("id"), str)
        }

        seen_ids = set()

        for index, item in enumerate(handoffs):
            label = f"handoffs[{index}]"

            if not isinstance(item, dict):
                errors.append(f"{label} must be a mapping")
                continue

            handoff_id = item.get("id")
            source = item.get("from_role")
            target = item.get("to_role")
            artifact_id = item.get("artifact_id")

            if not isinstance(handoff_id, str) or not handoff_id.strip():
                errors.append(f"{label}.id must be a non-empty string")
            elif handoff_id in seen_ids:
                errors.append(f"Duplicate handoff ID: {handoff_id}")
            else:
                seen_ids.add(handoff_id)

            if not isinstance(source, str) or source not in roles:
                errors.append(f"{label}.from_role is invalid")

            if not isinstance(target, str) or target not in roles:
                errors.append(f"{label}.to_role is invalid")

            if isinstance(source, str) and source == target:
                errors.append(f"{label} cannot hand off to the same role")

            if (
                not isinstance(artifact_id, str)
                or artifact_id not in artifact_ids
            ):
                errors.append(
                    f"{label}.artifact_id must reference a declared artifact"
                )

            for field in ("required_outputs", "acceptance_checks"):
                value = item.get(field)

                if (
                    not isinstance(value, list)
                    or not value
                    or any(
                        not isinstance(entry, str) or not entry.strip()
                        for entry in value
                    )
                ):
                    errors.append(
                        f"{label}.{field} must be a non-empty list of strings"
                    )

        if not handoffs:
            warnings.append(
                "No handoffs are declared yet; do not infer them from role names."
            )

        return report(errors, warnings, "Handoff validation")

    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())