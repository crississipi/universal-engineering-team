
#!/usr/bin/env python3
"""Validate formal handoff contracts against ownership and relationship rules."""

from pathlib import Path
import re
import sys

from validation_common import ROOT, expected_roles, load_yaml, report

MANIFEST = ROOT / "docs/team/ownership.yml"
MATRIX = ROOT / "docs/team/producer-consumer-matrix.md"

RELATIONSHIP_TYPES = {
    "required_input",
    "conditional_input",
    "feedback",
}

CONTRACT_STATUSES = {
    "proposed",
    "active",
    "deprecated",
}

# The schema defines HOF-<PRODUCER>-<CONSUMER>-<SEQUENCE>.
# Role abbreviations are not centrally mapped, so validate the identifier
# structure without guessing whether an abbreviation matches a role slug.
HANDOFF_ID_RE = re.compile(
    r"^HOF-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3,}$"
)

# Contract versions must be strings such as "1.0" or "1.0.1".
VERSION_RE = re.compile(r"^[0-9]+(?:\.[0-9]+)*$")

ARTIFACT_ID_RE = re.compile(r"^ART-[A-Z0-9]+(?:-[A-Z0-9]+)*$")


def non_empty_string(value):
    return isinstance(value, str) and bool(value.strip())


def validate_string_list(value, field, label, errors, allow_empty=False):
    """Validate a list containing only non-empty strings."""
    if not isinstance(value, list):
        errors.append(f"{label}.{field} must be a list of strings")
        return

    if not allow_empty and not value:
        errors.append(f"{label}.{field} must not be empty")
        return

    for index, entry in enumerate(value):
        if not non_empty_string(entry):
            errors.append(
                f"{label}.{field}[{index}] must be a non-empty string"
            )


def parse_relationship_matrix(path, errors):
    """Read package relationships from the Markdown matrix table."""
    if not path.is_file():
        errors.append(
            "Missing producer-consumer matrix: "
            "docs/team/producer-consumer-matrix.md"
        )
        return {}

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"Could not read producer-consumer matrix: {exc}")
        return {}

    header = None
    relationships = {}

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()

        if not stripped.startswith("|"):
            continue

        cells = [
            cell.strip().strip("`")
            for cell in stripped.strip("|").split("|")
        ]

        normalized = [cell.lower() for cell in cells]

        # Locate the table header by its declared column names.
        if header is None:
            if (
                "producer package" in normalized
                and "consumer package" in normalized
                and "relationship" in normalized
            ):
                header = {
                    name: normalized.index(name)
                    for name in (
                        "producer package",
                        "consumer package",
                        "relationship",
                    )
                }
            continue

        # Ignore Markdown separator rows.
        if all(
            cell and set(cell) <= {"-", ":"}
            for cell in cells
        ):
            continue

        required_width = max(header.values()) + 1

        if len(cells) < required_width:
            errors.append(
                f"Matrix line {line_number} has fewer columns than its header"
            )
            continue

        producer = cells[header["producer package"]]
        consumer = cells[header["consumer package"]]
        relationship = cells[header["relationship"]]

        if not ARTIFACT_ID_RE.fullmatch(producer):
            errors.append(
                f"Matrix line {line_number} has an invalid producer "
                f"package ID: {producer!r}"
            )
            continue

        if not ARTIFACT_ID_RE.fullmatch(consumer):
            errors.append(
                f"Matrix line {line_number} has an invalid consumer "
                f"package ID: {consumer!r}"
            )
            continue

        if (
                not isinstance(relationship, str)
                or relationship not in RELATIONSHIP_TYPES
            ):
            errors.append(
                f"Matrix line {line_number} has an invalid relationship "
                f"type: {relationship!r}"
            )
            continue

        pair = (producer, consumer)

        if pair in relationships:
            errors.append(
                f"Duplicate producer-consumer matrix relationship: "
                f"{producer} -> {consumer}"
            )
            continue

        relationships[pair] = relationship

    if header is None:
        errors.append(
            "Producer-consumer matrix is missing its expected table header"
        )

    return relationships


def validate_handoff(item, index, roles, artifacts, matrix, seen_ids, errors):
    """Validate one reusable handoff contract."""
    label = f"handoffs[{index}]"

    if not isinstance(item, dict):
        errors.append(f"{label} must be a mapping")
        return

    handoff_id = item.get("id")

    if not non_empty_string(handoff_id):
        errors.append(f"{label}.id must be a non-empty string")
    else:
        if not HANDOFF_ID_RE.fullmatch(handoff_id):
            errors.append(
                f"{label}.id must follow "
                "HOF-<PRODUCER>-<CONSUMER>-<SEQUENCE> format"
            )

        if handoff_id in seen_ids:
            errors.append(f"Duplicate handoff ID: {handoff_id}")
        else:
            seen_ids.add(handoff_id)

    version = item.get("contract_version")

    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        errors.append(
            f"{label}.contract_version must be a quoted numeric "
            "version string such as '1.0'"
        )

    source = item.get("from_role")
    target = item.get("to_role")

    if not isinstance(source, str) or source not in roles:
        errors.append(f"{label}.from_role is invalid")

    if not isinstance(target, str) or target not in roles:
        errors.append(f"{label}.to_role is invalid")

    if (
        isinstance(source, str)
        and isinstance(target, str)
        and source == target
    ):
        errors.append(f"{label} cannot hand off to the same role")

    producer_id = item.get("artifact_id")
    consumer_id = item.get("consumer_artifact_id")

    producer = artifacts.get(producer_id) if isinstance(producer_id, str) else None
    consumer = artifacts.get(consumer_id) if isinstance(consumer_id, str) else None

    if producer is None:
        errors.append(
            f"{label}.artifact_id must reference a declared producer package"
        )
    elif isinstance(source, str) and source in roles:
        if producer.get("owner") != source:
            errors.append(
                f"{label}.artifact_id owner must match from_role "
                f"({source})"
            )

        if producer.get("primary_producer") != source:
            errors.append(
                f"{label}.artifact_id primary_producer must match "
                f"from_role ({source})"
            )

    if consumer is None:
        errors.append(
            f"{label}.consumer_artifact_id must reference a declared "
            "consumer package"
        )
    elif isinstance(target, str) and target in roles:
        if consumer.get("owner") != target:
            errors.append(
                f"{label}.consumer_artifact_id owner must match "
                f"to_role ({target})"
            )

    if (
        isinstance(producer_id, str)
        and isinstance(consumer_id, str)
        and producer_id == consumer_id
    ):
        errors.append(
            f"{label} must reference different producer and consumer packages"
        )

    relationship = item.get("relationship_type")

    if (
            not isinstance(relationship, str)
            or relationship not in RELATIONSHIP_TYPES
        ):
        errors.append(
            f"{label}.relationship_type must be one of: "
            + ", ".join(sorted(RELATIONSHIP_TYPES))
        )
    elif (
        isinstance(producer_id, str)
        and isinstance(consumer_id, str)
        and producer is not None
        and consumer is not None
    ):
        pair = (producer_id, consumer_id)
        matrix_relationship = matrix.get(pair)

        if matrix_relationship is None:
            errors.append(
                f"{label} relationship {producer_id} -> {consumer_id} "
                "does not exist in producer-consumer-matrix.md"
            )
        elif matrix_relationship != relationship:
            errors.append(
                f"{label}.relationship_type is {relationship!r}, but the "
                f"matrix declares {matrix_relationship!r} for "
                f"{producer_id} -> {consumer_id}"
            )

    if not non_empty_string(item.get("purpose")):
        errors.append(f"{label}.purpose must be a non-empty string")

    validate_string_list(
        item.get("required_outputs"),
        "required_outputs",
        label,
        errors,
    )

    validate_string_list(
        item.get("required_context"),
        "required_context",
        label,
        errors,
        allow_empty=True,
    )

    validate_string_list(
        item.get("acceptance_checks"),
        "acceptance_checks",
        label,
        errors,
    )

    activation_condition = item.get("activation_condition")

    if relationship == "conditional_input":
        if not non_empty_string(activation_condition):
            errors.append(
                f"{label}.activation_condition is required for "
                "conditional_input"
            )
    elif activation_condition is not None and not non_empty_string(
        activation_condition
    ):
        errors.append(
            f"{label}.activation_condition must be a non-empty string "
            "when provided"
        )

    status = item.get("status")

    if (
            not isinstance(status, str)
            or status not in CONTRACT_STATUSES
        ):
        errors.append(
            f"{label}.status must be one of: "
            + ", ".join(sorted(CONTRACT_STATUSES))
        )


def main():
    errors = []
    warnings = []

    try:
        data = load_yaml(MANIFEST)

        if not isinstance(data, dict):
            raise ValueError("ownership.yml must contain a YAML mapping")

        roles = set(expected_roles())

        if data.get("roles") != expected_roles():
            errors.append(
                "ownership.yml roles must match expected-roles.yml in order"
            )

        raw_artifacts = data.get("artifacts")
        handoffs = data.get("handoffs")

        if not isinstance(raw_artifacts, list):
            errors.append("ownership.yml artifacts must be a list")
            raw_artifacts = []

        if not isinstance(handoffs, list):
            errors.append("ownership.yml handoffs must be a list")
            handoffs = []

        artifacts = {}

        for index, artifact in enumerate(raw_artifacts):
            label = f"artifacts[{index}]"

            if not isinstance(artifact, dict):
                errors.append(f"{label} must be a mapping")
                continue

            artifact_id = artifact.get("id")

            if not non_empty_string(artifact_id):
                errors.append(f"{label}.id must be a non-empty string")
                continue

            if artifact_id in artifacts:
                errors.append(f"Duplicate artifact ID: {artifact_id}")
                continue

            artifacts[artifact_id] = artifact

        matrix = parse_relationship_matrix(MATRIX, errors)

        seen_ids = set()

        for index, item in enumerate(handoffs):
            validate_handoff(
                item=item,
                index=index,
                roles=roles,
                artifacts=artifacts,
                matrix=matrix,
                seen_ids=seen_ids,
                errors=errors,
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
