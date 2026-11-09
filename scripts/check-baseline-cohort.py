#!/usr/bin/env python3
"""Validate baseline cohort revision pins and execution-environment metadata.

This is a structural/readiness check only. It never approves scenarios or
authorizes baseline execution.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validation_common import expected_roles  # noqa: E402

SCHEMA_PATH = ROOT / "schemas/baseline/baseline-cohort.schema.json"
COHORT_PATH = ROOT / "docs/evaluation/baseline/cohorts.yml"


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""

    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep)
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
            mapping[key] = self.construct_object(value_node, deep)
        return mapping


def load_yaml_text(raw: str):
    return yaml.load(raw, Loader=UniqueKeyLoader)


def git_text(*args):
    """Return git output or raise a useful error; no shell is involved."""
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode != 0:
        raise ValueError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


def git_commit_exists(commit):
    try:
        git_text("cat-file", "-e", f"{commit}^{{commit}}")
        return True
    except ValueError:
        return False


def commit_contains(base_commit, pinned_commit):
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", pinned_commit, base_commit],
        cwd=ROOT, text=True, encoding="utf-8",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    return result.returncode == 0


def git_file(commit, path):
    return git_text("show", f"{commit}:{path}")


def load_schema():
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load cohort schema: {exc}") from exc
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ValueError("cohort schema must declare Draft 2020-12")
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def validate_cohort(path: Path = COHORT_PATH):
    errors, blockers = [], []
    try:
        raw = path.read_text(encoding="utf-8")
        cohort = load_yaml_text(raw)
    except (OSError, yaml.YAMLError) as exc:
        return [f"cannot read cohort register: {exc}"], blockers

    if not isinstance(cohort, dict):
        return ["cohort register must be a YAML mapping"], blockers

    try:
        validator = load_schema()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)], blockers

    for issue in sorted(validator.iter_errors(cohort), key=lambda item: list(map(str, item.absolute_path))):
        location = ".".join(str(part) for part in issue.absolute_path) or "<document>"
        errors.append(f"{location}: {issue.message}")
    if errors:
        return errors, blockers

    base_commit = cohort["repository_base_commit"]
    if base_commit is None:
        blockers.append("repository_base_commit is not pinned")
    elif not git_commit_exists(base_commit):
        errors.append(f"repository_base_commit does not exist in this checkout: {base_commit}")

    environment = cohort["execution_environment"]
    for field in (
        "provider", "model_display_label", "model_identifier", "model_version",
        "mode", "tool_permissions", "operating_environment",
    ):
        value = environment[field]
        if value is None or (isinstance(value, str) and value.strip().lower() == "unknown"):
            blockers.append(f"execution_environment.{field} is not recorded")

    configuration = environment["configuration"]
    for field in ("temperature", "reasoning_effort", "other_material_settings"):
        value = configuration[field]
        if value is None or (isinstance(value, str) and value.strip().lower() == "unknown"):
            blockers.append(f"execution_environment.configuration.{field} is not recorded")

    roles = expected_roles()
    expected_by_id = {f"SCEN-BASELINE-{role.upper()}": role for role in roles}
    pins = cohort["scenario_pins"]
    seen = set()
    for index, pin in enumerate(pins):
        scenario_id = pin["scenario_id"]
        role = pin["role"]
        label = f"scenario_pins[{index}] ({scenario_id})"
        if scenario_id in seen:
            errors.append(f"duplicate cohort scenario pin: {scenario_id}")
            continue
        seen.add(scenario_id)
        expected_role = expected_by_id.get(scenario_id)
        if expected_role is None:
            errors.append(f"{label}: scenario ID is not in the canonical baseline catalog")
            continue
        if role != expected_role:
            errors.append(f"{label}: role must be {expected_role}")

        scenario_path = f"tests/scenarios/{scenario_id}.yml"
        skill_path = f"skills/{role}/SKILL.md"
        scenario_commit = pin["scenario_commit"]
        skill_commit = pin["skill_commit"]

        if scenario_commit is None:
            blockers.append(f"{label}: scenario_commit is not pinned")
        else:
            try:
                pinned_scenario = load_yaml_text(git_file(scenario_commit, scenario_path))
                if not isinstance(pinned_scenario, dict):
                    errors.append(f"{label}: pinned scenario file is not a YAML mapping")
                else:
                    if pinned_scenario.get("id") != scenario_id or pinned_scenario.get("role") != role:
                        errors.append(f"{label}: pinned scenario identity/role does not match the register")
                    prompt = pinned_scenario.get("task_prompt")
                    if not isinstance(prompt, str) or not prompt:
                        errors.append(f"{label}: pinned scenario has no non-empty task_prompt")
                    else:
                        actual_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
                        expected_hash = pin["prompt_sha256"]
                        if expected_hash is None:
                            blockers.append(f"{label}: prompt_sha256 is not pinned")
                        elif actual_hash != expected_hash:
                            errors.append(f"{label}: prompt_sha256 does not match pinned scenario task_prompt bytes")
            except (ValueError, yaml.YAMLError) as exc:
                errors.append(f"{label}: cannot read scenario at pinned commit: {exc}")

        if skill_commit is None:
            blockers.append(f"{label}: skill_commit is not pinned")
        else:
            try:
                skill_text = git_file(skill_commit, skill_path)
                if not skill_text.strip():
                    errors.append(f"{label}: pinned role skill file is empty")
            except ValueError as exc:
                errors.append(f"{label}: cannot read role skill at pinned commit: {exc}")

        if base_commit is not None and git_commit_exists(base_commit):
            for field, commit in (("scenario_commit", scenario_commit), ("skill_commit", skill_commit)):
                if commit is not None and git_commit_exists(commit) and not commit_contains(base_commit, commit):
                    errors.append(f"{label}: {field} is not an ancestor of repository_base_commit")

    missing = sorted(set(expected_by_id) - seen)
    if missing:
        errors.append("cohort register is missing canonical scenario pins: " + ", ".join(missing))
    return errors, blockers


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check baseline cohort revision pins and execution-environment readiness."
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--cohort", default=str(COHORT_PATH), help="Path to the cohort YAML register.")
    args = parser.parse_args(argv)

    errors, blockers = validate_cohort(Path(args.cohort))
    result = {
        "status": "ERROR" if errors else ("BLOCKED" if blockers else "COHORT-PINS-CLEAR"),
        "errors": errors,
        "blockers": blockers,
        "execution_authorized": False,
        "note": "This check does not approve scenarios, resolve stakeholder decisions, or authorize execution.",
    }
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("Baseline cohort readiness check")
        print(f"Status: {result['status']}")
        for error in errors:
            print(f"ERROR: {error}")
        for blocker in blockers:
            print(f"BLOCKER: {blocker}")
        print(result["note"])
    return 2 if errors else (1 if blockers else 0)


if __name__ == "__main__":
    raise SystemExit(main())
