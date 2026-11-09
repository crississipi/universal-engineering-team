#!/usr/bin/env python3
"""Prepare Git-derived baseline cohort revision pins without editing the cohort register.

The selected base commit must be supplied explicitly. For each scenario and
role skill, the script finds the latest commit that changed that path at or
before the base commit. It hashes the parsed task_prompt string from the
scenario file at that scenario revision. The output is a candidate pin
fragment only; it does not approve scenarios or authorize execution.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
ROLES_PATH = ROOT / "docs/team/expected-roles.yml"


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise ValueError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def resolve_commit(value: str) -> str:
    sha = git("rev-parse", "--verify", f"{value}^{{commit}}")
    if len(sha) != 40:
        raise ValueError(f"resolved base commit is not a full SHA: {value}")
    return sha


def latest_path_commit(base: str, path: str) -> str:
    sha = git("log", "-1", "--format=%H", base, "--", path)
    if not sha:
        raise ValueError(f"no commit at or before {base} contains changes to {path}")
    return resolve_commit(sha)


def file_at(commit: str, path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise ValueError(result.stderr.strip() or f"cannot read {path} at {commit}")
    return result.stdout


def load_roles() -> list[str]:
    data = yaml.safe_load(ROLES_PATH.read_text(encoding="utf-8"))
    roles = data.get("roles") if isinstance(data, dict) else None
    if not isinstance(roles, list) or not roles or not all(isinstance(role, str) for role in roles):
        raise ValueError(f"{ROLES_PATH.relative_to(ROOT)} must contain a non-empty roles list")
    if len(roles) != len(set(roles)):
        raise ValueError("canonical role inventory contains duplicate role IDs")
    return roles


def prepare(base_value: str) -> dict:
    base = resolve_commit(base_value)
    pins = []
    for role in load_roles():
        scenario_id = f"SCEN-BASELINE-{role.upper()}"
        scenario_path = f"tests/scenarios/{scenario_id}.yml"
        skill_path = f"skills/{role}/SKILL.md"
        scenario_commit = latest_path_commit(base, scenario_path)
        skill_commit = latest_path_commit(base, skill_path)

        scenario = yaml.safe_load(file_at(scenario_commit, scenario_path))
        if not isinstance(scenario, dict):
            raise ValueError(f"{scenario_path} at {scenario_commit} is not a YAML mapping")
        if scenario.get("id") != scenario_id or scenario.get("role") != role:
            raise ValueError(f"{scenario_path} at {scenario_commit} has mismatched id/role")
        prompt = scenario.get("task_prompt")
        if not isinstance(prompt, str) or not prompt:
            raise ValueError(f"{scenario_path} at {scenario_commit} has no non-empty task_prompt")

        skill = file_at(skill_commit, skill_path)
        if not skill.strip():
            raise ValueError(f"{skill_path} at {skill_commit} is empty")

        pins.append({
            "scenario_id": scenario_id,
            "role": role,
            "scenario_commit": scenario_commit,
            "skill_commit": skill_commit,
            "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        })

    return {
        "repository_base_commit": base,
        "scenario_pins": pins,
        "execution_authorized": False,
        "notes": [
            "Candidate Git-derived pins only; review before copying into cohorts.yml.",
            "Scenario and skill commits are the latest path-changing commits reachable from the selected base commit.",
            "Prompt SHA-256 is over the UTF-8 encoding of the parsed task_prompt string at scenario_commit.",
            "This output does not approve scenarios, resolve stakeholder decisions, or authorize execution.",
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Prepare reproducible Git-derived baseline cohort pins; does not edit cohorts.yml."
    )
    parser.add_argument(
        "--base-commit",
        required=True,
        help="Explicit repository commit to use as the cohort base (SHA or resolvable Git ref).",
    )
    parser.add_argument("--format", choices=("yaml", "json"), default="yaml")
    args = parser.parse_args(argv)

    try:
        result = prepare(args.base_commit)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(yaml.safe_dump(result, sort_keys=False, allow_unicode=True), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
