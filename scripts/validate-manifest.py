#!/usr/bin/env python3
"""Validate the derived collaboration manifest's structure and declarations."""

from pathlib import Path
import argparse
import json
import sys

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError:
    print("ERROR: A validation dependency is missing. Run: python -m pip install -r requirements-dev.txt")
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
BACKTICK = chr(96)


def read_yaml(path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ValueError(f"Cannot load {path}: {exc}") from exc


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot load {path}: {exc}") from exc


def parse_matrix_relationships(content):
    """Parse canonical package edges from the Markdown matrix table."""
    relationships = {}
    errors = []
    for line_number, line in enumerate(content.splitlines(), start=1):
        if not line.startswith("| " + BACKTICK + "ART-"):
            continue
        columns = [column.strip() for column in line.split("|")[1:-1]]
        if len(columns) != 5:
            errors.append(
                f"producer-consumer-matrix.md:{line_number}: expected five relationship columns"
            )
            continue
        producer, consumer, output, relationship_type, condition = columns
        producer = producer.strip(BACKTICK)
        consumer = consumer.strip(BACKTICK)
        relationship_type = relationship_type.strip(BACKTICK)
        edge = (producer, consumer)
        if edge in relationships:
            errors.append(
                f"producer-consumer-matrix.md:{line_number}: duplicate relationship edge {producer} -> {consumer}"
            )
            continue
        relationships[edge] = {
            "id": f"REL-{producer}--{consumer}",
            "producer_artifact_id": producer,
            "consumer_artifact_id": consumer,
            "relationship_type": relationship_type,
            "output": output,
            "condition": condition,
        }
    return relationships, errors


def relationship_requires_input(relationship_type, *, activated=False):
    """Feedback never blocks; conditional inputs block only when activated."""
    if relationship_type == "required_input":
        return True
    if relationship_type == "conditional_input":
        return bool(activated)
    return False


def validate_manifest(manifest, schema, role_data, ownership, matrix_content,
                      *, root=ROOT, check_skill_paths=True):
    errors = []
    if not isinstance(manifest, dict):
        return ["skills/manifest.yml must contain a YAML mapping"]
    if not isinstance(role_data, dict) or not isinstance(role_data.get("roles"), list):
        return ["docs/team/expected-roles.yml must contain a roles list"]
    if not isinstance(ownership, dict):
        return ["docs/team/ownership.yml must contain a YAML mapping"]

    try:
        Draft202012Validator.check_schema(schema)
        schema_validator = Draft202012Validator(schema)
        for error in sorted(
            schema_validator.iter_errors(manifest),
            key=lambda item: list(map(str, item.absolute_path)),
        ):
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"skills/manifest.yml:{location}: {error.message}")
    except Exception as exc:
        errors.append(f"schemas/manifest.schema.json is invalid: {exc}")
        return errors

    canonical_roles = role_data["roles"]
    if any(not isinstance(role, str) or not role.strip() for role in canonical_roles):
        errors.append("expected-roles.yml: roles must contain non-empty strings")
        canonical_roles = []
    if len(canonical_roles) != len(set(canonical_roles)):
        errors.append("expected-roles.yml: duplicate role IDs")
    role_ids = set(canonical_roles)
    if ownership.get("roles", []) != canonical_roles:
        errors.append("ownership.yml: role inventory differs from expected-roles.yml")

    seen_roles = set()
    for index, role in enumerate(manifest.get("roles", [])):
        if not isinstance(role, dict):
            continue
        role_id = role.get("id")
        skill = role.get("skill")
        if role_id in seen_roles:
            errors.append(f"roles[{index}]: duplicate role declaration {role_id!r}")
        seen_roles.add(role_id)
        if role_id not in role_ids:
            errors.append(f"roles[{index}]: unknown role reference {role_id!r}")
        expected_skill = f"skills/{role_id}/SKILL.md"
        if skill != expected_skill:
            errors.append(f"roles[{index}]: skill path must match role ID ({expected_skill!r})")
        elif check_skill_paths and not (root / skill).is_file():
            errors.append(f"roles[{index}]: skill file does not exist: {skill}")

    source_artifacts = ownership.get("artifacts", [])
    if not isinstance(source_artifacts, list):
        errors.append("ownership.yml: artifacts must be a list")
        source_artifacts = []
    source_artifact_by_id = {}
    for index, artifact in enumerate(source_artifacts):
        if not isinstance(artifact, dict):
            errors.append(f"ownership.yml: artifacts[{index}] must be a mapping")
            continue
        artifact_id = artifact.get("id")
        if artifact_id in source_artifact_by_id:
            errors.append(f"ownership.yml: duplicate artifact ID {artifact_id!r}")
        source_artifact_by_id[artifact_id] = artifact
        for field in ("owner", "primary_producer"):
            role_id = artifact.get(field)
            if role_id not in role_ids:
                errors.append(
                    f"ownership.yml: artifact {artifact_id!r} has unknown {field} role {role_id!r}"
                )
        contributors = artifact.get("contributors", [])
        if not isinstance(contributors, list):
            errors.append(f"ownership.yml: artifact {artifact_id!r} contributors must be a list")
        else:
            if any(not isinstance(role, str) for role in contributors):
                errors.append(f"ownership.yml: artifact {artifact_id!r} contributors must be role IDs")
            elif len(contributors) != len(set(contributors)):
                errors.append(f"ownership.yml: artifact {artifact_id!r} has duplicate contributors")
            for role_id in contributors:
                if role_id not in role_ids:
                    errors.append(
                        f"ownership.yml: artifact {artifact_id!r} has unknown contributor role {role_id!r}"
                    )

    manifest_artifact_ids = set()
    for index, artifact in enumerate(manifest.get("artifacts", [])):
        if not isinstance(artifact, dict):
            continue
        artifact_id = artifact.get("id")
        if artifact_id in manifest_artifact_ids:
            errors.append(f"artifacts[{index}]: duplicate artifact ID {artifact_id!r}")
        manifest_artifact_ids.add(artifact_id)
        if artifact_id not in source_artifact_by_id:
            errors.append(f"artifacts[{index}]: unknown artifact reference {artifact_id!r}")
        for field in ("owner", "primary_producer"):
            if artifact.get(field) not in role_ids:
                errors.append(
                    f"artifacts[{index}]: unknown {field} role {artifact.get(field)!r}"
                )
        for role_id in artifact.get("contributors", []):
            if role_id not in role_ids:
                errors.append(f"artifacts[{index}]: unknown contributor role {role_id!r}")

    source_relationships, matrix_errors = parse_matrix_relationships(matrix_content)
    errors.extend(matrix_errors)
    relationship_by_edge = {}
    relationship_ids = set()
    for index, relationship in enumerate(manifest.get("relationships", [])):
        if not isinstance(relationship, dict):
            continue
        producer = relationship.get("producer_artifact_id")
        consumer = relationship.get("consumer_artifact_id")
        edge = (producer, consumer)
        relationship_id = relationship.get("id")
        if relationship_id in relationship_ids:
            errors.append(f"relationships[{index}]: duplicate relationship ID {relationship_id!r}")
        relationship_ids.add(relationship_id)
        if edge in relationship_by_edge:
            errors.append(
                f"relationships[{index}]: conflicting duplicate declaration for {producer!r} -> {consumer!r}"
            )
        relationship_by_edge[edge] = relationship
        for artifact_id in edge:
            if artifact_id not in source_artifact_by_id:
                errors.append(f"relationships[{index}]: unknown artifact reference {artifact_id!r}")
        if producer == consumer:
            errors.append(f"relationships[{index}]: producer and consumer artifacts must differ")
        if relationship_id != f"REL-{producer}--{consumer}":
            errors.append(f"relationships[{index}]: ID does not match its producer-consumer edge")
        if relationship.get("relationship_type") not in {
            "required_input", "conditional_input", "feedback"
        }:
            errors.append(
                f"relationships[{index}]: unsupported relationship type {relationship.get('relationship_type')!r}"
            )
        condition = relationship.get("condition")
        if not isinstance(condition, str) or not condition.strip():
            errors.append(f"relationships[{index}]: condition must not be blank")
        source_edge = source_relationships.get(edge)
        if source_edge is None:
            errors.append(
                f"relationships[{index}]: missing mirror edge in producer-consumer-matrix.md"
            )
        elif relationship != source_edge:
            errors.append(
                f"relationships[{index}]: declaration conflicts with producer-consumer-matrix.md"
            )

    for producer, consumer in source_relationships:
        if (producer, consumer) not in relationship_by_edge:
            errors.append(
                f"skills/manifest.yml: missing relationship mirror for {producer} -> {consumer}"
            )

    handoffs = manifest.get("handoffs", [])
    source_handoffs = ownership.get("handoffs", [])
    if not isinstance(source_handoffs, list):
        errors.append("ownership.yml: handoffs must be a list")
        source_handoffs = []
    if handoffs != source_handoffs:
        errors.append("skills/manifest.yml: formal handoffs differ from ownership.yml")

    handoff_ids = set()
    handoff_edges = set()
    for index, handoff in enumerate(handoffs):
        if not isinstance(handoff, dict):
            continue
        handoff_id = handoff.get("id")
        if handoff_id in handoff_ids:
            errors.append(f"handoffs[{index}]: duplicate handoff ID {handoff_id!r}")
        handoff_ids.add(handoff_id)
        producer_id = handoff.get("artifact_id")
        consumer_id = handoff.get("consumer_artifact_id")
        edge = (producer_id, consumer_id)
        if edge in handoff_edges:
            errors.append(
                f"handoffs[{index}]: conflicting duplicate handoff for {producer_id!r} -> {consumer_id!r}"
            )
        handoff_edges.add(edge)
        producer_artifact = source_artifact_by_id.get(producer_id)
        consumer_artifact = source_artifact_by_id.get(consumer_id)
        if producer_artifact is None:
            errors.append(f"handoffs[{index}]: unknown producer artifact {producer_id!r}")
        if consumer_artifact is None:
            errors.append(f"handoffs[{index}]: unknown consumer artifact {consumer_id!r}")
        from_role = handoff.get("from_role")
        to_role = handoff.get("to_role")
        if from_role not in role_ids:
            errors.append(f"handoffs[{index}]: unknown producer role {from_role!r}")
        if to_role not in role_ids:
            errors.append(f"handoffs[{index}]: unknown consumer role {to_role!r}")
        if producer_artifact is not None:
            if from_role != producer_artifact.get("owner"):
                errors.append(
                    f"handoffs[{index}]: from_role must own producer artifact {producer_id!r}"
                )
            if from_role != producer_artifact.get("primary_producer"):
                errors.append(
                    f"handoffs[{index}]: from_role must be the primary producer of {producer_id!r}"
                )
        if consumer_artifact is not None and to_role != consumer_artifact.get("owner"):
            errors.append(
                f"handoffs[{index}]: to_role must own consumer artifact {consumer_id!r}"
            )
        relationship = relationship_by_edge.get(edge)
        if relationship is None:
            errors.append(
                f"handoffs[{index}]: missing producer-consumer relationship mirror for {producer_id!r} -> {consumer_id!r}"
            )
        elif handoff.get("relationship_type") != relationship.get("relationship_type"):
            errors.append(
                f"handoffs[{index}]: relationship_type conflicts with the producer-consumer matrix"
            )
        if handoff.get("relationship_type") == "conditional_input":
            activation = handoff.get("activation_condition")
            if not isinstance(activation, str) or not activation.strip():
                errors.append(
                    f"handoffs[{index}]: conditional handoff requires a non-empty activation_condition"
                )

    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        manifest = read_yaml(root / "skills/manifest.yml")
        schema = read_json(root / "schemas/manifest.schema.json")
        role_data = read_yaml(root / "docs/team/expected-roles.yml")
        ownership = read_yaml(root / "docs/team/ownership.yml")
        matrix = (root / "docs/team/producer-consumer-matrix.md").read_text(encoding="utf-8")
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: Cannot read producer-consumer matrix: {exc}")
        return 1

    errors = validate_manifest(
        manifest, schema, role_data, ownership, matrix, root=root
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"\nManifest validation failed: {len(errors)} error(s).")
        return 1
    print(
        "Manifest validation passed: schema, role/artifact references, "
        "relationship mirrors, handoff ownership, and declaration uniqueness."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
