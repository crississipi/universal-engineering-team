#!/usr/bin/env python3
"""Validate repository-wide baseline evaluation run records."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from validation_common import ROOT, expected_roles


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""

    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                duplicate = key in mapping
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    "found an unhashable mapping key", key_node.start_mark,
                ) from exc
            if duplicate:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    f"found duplicate key {key!r}", key_node.start_mark,
                )
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def normalize_yaml_dates(value):
    """Convert PyYAML timestamp objects to ISO strings for JSON Schema."""
    if isinstance(value, datetime):
        serialized = value.isoformat()
        if value.utcoffset() == timedelta(0):
            serialized = serialized.replace("+00:00", "Z")
        return serialized
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: normalize_yaml_dates(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_yaml_dates(item) for item in value]
    return value


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        return normalize_yaml_dates(yaml.load(stream, Loader=UniqueKeyLoader))


def load_schema(root: Path = ROOT):
    path = root / "schemas/baseline/baseline-run-record.schema.json"
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot load baseline run-record schema: {exc}") from exc
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ValueError("Baseline run-record schema must declare Draft 2020-12")
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def safe_path(raw_path: str, root: Path):
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise ValueError("path must be a non-empty repository-relative string")
    if "\\" in raw_path or ":" in raw_path:
        raise ValueError(f"unsafe repository path: {raw_path}")
    path = PurePosixPath(raw_path)
    if path.is_absolute() or "." in path.parts or ".." in path.parts:
        raise ValueError(f"unsafe repository path: {raw_path}")
    resolved = (root / Path(*path.parts)).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes repository: {raw_path}") from exc
    return resolved


def load_scenario_catalog(root: Path):
    scenarios_dir = root / "tests/scenarios"
    catalog = {}
    errors = []
    expected = set(expected_roles())
    for path in sorted(scenarios_dir.glob("SCEN-BASELINE-*.yml")):
        try:
            scenario = load_yaml(path)
        except (OSError, yaml.YAMLError, ValueError) as exc:
            errors.append(f"[BLV002] Cannot parse {path.relative_to(root)}: {exc}")
            continue
        if not isinstance(scenario, dict):
            errors.append(f"[BLV002] {path.relative_to(root)} must contain a YAML mapping")
            continue
        scenario_id = scenario.get("id")
        role = scenario.get("role")
        if not isinstance(scenario_id, str) or not scenario_id.startswith("SCEN-BASELINE-"):
            errors.append(f"[BLV003] Invalid baseline scenario ID in {path.relative_to(root)}")
            continue
        if scenario_id in catalog:
            errors.append(f"[BLV004] Duplicate baseline scenario ID: {scenario_id}")
            continue
        if role not in expected:
            errors.append(f"[BLV005] {scenario_id} uses non-canonical role: {role!r}")
        if path.name != f"{scenario_id}.yml":
            errors.append(f"[BLV006] Scenario filename does not match ID: {path.relative_to(root)}")
        catalog[scenario_id] = scenario

    roles = [scenario.get("role") for scenario in catalog.values()]
    if len(catalog) != 17:
        errors.append(f"[BLV007] Expected 17 baseline scenario drafts; found {len(catalog)}")
    missing_roles = sorted(expected - set(roles))
    duplicate_roles = sorted({role for role in roles if roles.count(role) > 1})
    if missing_roles:
        errors.append("[BLV008] Missing baseline scenarios for roles: " + ", ".join(missing_roles))
    if duplicate_roles:
        errors.append("[BLV009] Multiple baseline scenarios map to roles: " + ", ".join(duplicate_roles))
    return catalog, errors


def check_evidence_path(raw_path, root, errors, label, *, required=True, allow_unknown=False):
    if allow_unknown and raw_path == "unknown":
        return
    try:
        path = safe_path(raw_path, root)
    except ValueError as exc:
        errors.append(f"[BLV030] {label}: {exc}")
        return
    evidence_root = (root / "evaluations/baseline/evidence").resolve()
    try:
        path.relative_to(evidence_root)
    except ValueError:
        errors.append(f"[BLV031] {label} must be inside evaluations/baseline/evidence/: {raw_path}")
        return
    if required and not path.exists():
        errors.append(f"[BLV032] {label} does not exist: {raw_path}")


def validate_record(path: Path, record, scenarios, root: Path, schema_validator):
    errors = []
    relative = path.relative_to(root).as_posix()
    for error in sorted(
        schema_validator.iter_errors(record),
        key=lambda item: (list(map(str, item.absolute_path)), item.message),
    ):
        location = ".".join(str(part) for part in error.absolute_path) or "<document>"
        errors.append(f"[BLV010] {relative}:{location}: {error.message}")
    if errors:
        return errors

    scenario_id = record["scenario_id"]
    scenario = scenarios.get(scenario_id)
    if scenario is None:
        return [f"[BLV011] {relative} references unknown scenario {scenario_id}"]

    if scenario.get("status") != "approved":
        errors.append(f"[BLV012] {scenario_id} is not approved; baseline run records are not permitted")
    approval = scenario.get("approval")
    if not isinstance(approval, dict) or not approval.get("approved_by") or not approval.get("approved_at"):
        errors.append(f"[BLV013] {scenario_id} lacks explicit approval.approved_by/approved_at")
    if record["role"] != scenario.get("role"):
        errors.append(f"[BLV014] {relative} role does not match {scenario_id}")
    if record["rubric_version"] != scenario.get("rubric_version"):
        errors.append(f"[BLV015] {relative} rubric_version does not match {scenario_id}")
    expected_run_id = f"BASELINE-{scenario_id}-RUN-{record['run_number']:02d}"
    if record["run_id"] != expected_run_id:
        errors.append(f"[BLV016] {relative} run_id must be {expected_run_id}")
    expected_filename = f"{scenario_id}-run-{record['run_number']:02d}.yml"
    if path.name != expected_filename:
        errors.append(f"[BLV017] {relative} filename must be {expected_filename}")

    revisions = record["revisions"]
    expected_scenario_path = f"tests/scenarios/{scenario_id}.yml"
    expected_skill_path = f"skills/{record['role']}/SKILL.md"
    if revisions["scenario_path"] != expected_scenario_path:
        errors.append(f"[BLV018] {relative} scenario_path must be {expected_scenario_path}")
    if revisions["skill_path"] != expected_skill_path:
        errors.append(f"[BLV019] {relative} skill_path must be {expected_skill_path}")

    scenario_criteria = scenario.get("criteria", [])
    criterion_ids = [item.get("id") for item in scenario_criteria if isinstance(item, dict)]
    recorded_ids = [item.get("criterion_id") for item in record["scores"]]
    if len(recorded_ids) != len(set(recorded_ids)):
        errors.append(f"[BLV020] {relative} contains duplicate criterion score entries")
    if set(recorded_ids) != set(criterion_ids):
        errors.append(f"[BLV021] {relative} criterion scores must exactly match the scenario rubric")
    required_requirements = set(scenario.get("required_requirements", []))
    for score in record["scores"]:
        matching = next((item for item in scenario_criteria if item.get("id") == score.get("criterion_id")), None)
        if matching and matching.get("requirement_ref") not in required_requirements:
            errors.append(
                f"[BLV022] {relative} criterion {score.get('criterion_id')} does not trace to scenario.required_requirements"
            )

    prompt_path = record["input"]["prompt_path"]
    check_evidence_path(prompt_path, root, errors, f"{relative} input.prompt_path")
    if prompt_path != "unknown":
        try:
            prompt_file = safe_path(prompt_path, root)
        except ValueError:
            prompt_file = None
        if prompt_file is not None and prompt_file.is_file():
            digest = hashlib.sha256(prompt_file.read_bytes()).hexdigest()
            if digest != record["input"]["prompt_sha256"]:
                errors.append(f"[BLV023] {relative} prompt_sha256 does not match prompt file bytes")
        elif prompt_file is not None:
            errors.append(f"[BLV033] {relative} prompt_path must identify a file")

    evidence = record["evidence"]
    check_evidence_path(evidence["transcript_path"], root, errors, f"{relative} transcript_path", allow_unknown=True)
    check_evidence_path(evidence["git_status_path"], root, errors, f"{relative} git_status_path", allow_unknown=True)
    for index, artifact in enumerate(evidence["output_artifacts"]):
        check_evidence_path(artifact, root, errors, f"{relative} output_artifacts[{index}]")
    for index, command in enumerate(evidence["command_results"]):
        check_evidence_path(
            command["output_path"], root, errors,
            f"{relative} command_results[{index}].output_path", allow_unknown=True,
        )
    return errors


def validate_run_records(runs_dir: Path, root: Path = ROOT):
    errors, warnings = [], []
    try:
        schema_validator = load_schema(root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return {"errors": [f"[BLV001] {exc}"], "warnings": [], "record_count": 0}

    scenarios, scenario_errors = load_scenario_catalog(root)
    errors.extend(scenario_errors)
    if not runs_dir.exists():
        runs = []
    elif not runs_dir.is_dir():
        return {"errors": errors + [f"[BLV024] Runs path is not a directory: {runs_dir}"], "warnings": warnings, "record_count": 0}
    else:
        runs = sorted(runs_dir.glob("*.yml"))

    seen = {}
    cohort_profiles = {}
    scenario_profiles = {}
    for path in runs:
        try:
            record = load_yaml(path)
        except (OSError, yaml.YAMLError, ValueError) as exc:
            errors.append(f"[BLV025] Cannot parse {path.relative_to(root)}: {exc}")
            continue
        if not isinstance(record, dict):
            errors.append(f"[BLV026] {path.relative_to(root)} must contain a YAML mapping")
            continue

        record_errors = validate_record(path, record, scenarios, root, schema_validator)
        errors.extend(record_errors)
        if any(error.startswith("[BLV010]") for error in record_errors):
            continue
        scenario_id = record.get("scenario_id")
        run_number = record.get("run_number")
        if isinstance(scenario_id, str) and isinstance(run_number, int):
            key = (scenario_id, run_number)
            if key in seen:
                errors.append(
                    f"[BLV027] Duplicate run number {run_number} for {scenario_id}: "
                    f"{seen[key].relative_to(root)} and {path.relative_to(root)}"
                )
            else:
                seen[key] = path

        environment = record.get("execution_environment", {})
        revisions = record.get("revisions", {})
        comparability = record.get("comparability", {})
        cohort_id = comparability.get("cohort_id")
        if isinstance(cohort_id, str):
            cohort_profile = {
                "provider": environment.get("provider"),
                "model_display_label": environment.get("model_display_label"),
                "model_identifier": environment.get("model_identifier"),
                "model_version": environment.get("model_version"),
                "mode": environment.get("mode"),
                "configuration": environment.get("configuration"),
                "tool_permissions": environment.get("tool_permissions"),
                "operating_environment": environment.get("operating_environment"),
                "repository_base_commit": revisions.get("repository_base_commit"),
            }
            previous = cohort_profiles.setdefault(cohort_id, cohort_profile)
            if previous != cohort_profile:
                errors.append(f"[BLV028] Cohort {cohort_id} contains inconsistent provider/model/configuration/base-commit metadata")

            scenario_key = (cohort_id, scenario_id)
            scenario_profile = {
                "scenario_commit": revisions.get("scenario_commit"),
                "skill_commit": revisions.get("skill_commit"),
                "prompt_sha256": record.get("input", {}).get("prompt_sha256"),
            }
            previous_scenario = scenario_profiles.setdefault(scenario_key, scenario_profile)
            if previous_scenario != scenario_profile:
                errors.append(f"[BLV029] {scenario_id} has inconsistent scenario/skill/prompt revisions within cohort {cohort_id}")

    for scenario_id, scenario in scenarios.items():
        if scenario.get("status") != "approved":
            continue
        missing = sorted(set(range(1, 11)) - {
            number for (record_scenario, number) in seen if record_scenario == scenario_id
        })
        if missing:
            warnings.append(
                f"{scenario_id} is approved but missing run numbers: "
                + ", ".join(f"{number:02d}" for number in missing)
            )

    return {"errors": errors, "warnings": warnings, "record_count": len(runs)}


def resolve_runs_directory(raw_path: str, root: Path = ROOT):
    candidate = (root / raw_path).resolve()
    expected = (root / "evaluations/baseline/runs").resolve()
    if candidate != expected:
        raise ValueError("Runs directory must be evaluations/baseline/runs/.")
    return candidate


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate baseline run-record schemas, scenario references, evidence, and cohort consistency."
    )
    parser.add_argument(
        "runs_directory",
        nargs="?",
        default="evaluations/baseline/runs",
        help="Repository-relative baseline runs directory (default: evaluations/baseline/runs)",
    )
    args = parser.parse_args(argv)

    try:
        runs_dir = resolve_runs_directory(args.runs_directory)
        result = validate_run_records(runs_dir)
    except (OSError, ValueError) as exc:
        print(f"ERROR: [BLV099] {exc}")
        return 2

    print(f"Baseline run-record validation: {result['record_count']} record(s) inspected")
    for warning in result["warnings"]:
        print(f"WARNING: {warning}")
    for error in result["errors"]:
        print(f"ERROR: {error}")
    if result["errors"]:
        print(f"\nBaseline validation failed: {len(result['errors'])} error(s), {len(result['warnings'])} warning(s).")
        return 1
    print(f"\nBaseline validation passed: {len(result['warnings'])} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
