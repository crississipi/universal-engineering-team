#!/usr/bin/env python3
"""Synchronize canonical role skills into VS Code Copilot's project skill directory."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys

import yaml

from validation_common import ROOT

DESTINATION = ROOT / ".github" / "skills"
MARKER_NAME = ".generated-by-universal-engineering-team"


def snapshot(directory: Path) -> dict[str, bytes]:
    return {
        path.relative_to(directory).as_posix(): path.read_bytes()
        for path in directory.rglob("*")
        if path.is_file()
    }


def synchronize(root: Path = ROOT, write: bool = False) -> list[str]:
    source_root = root / "skills"
    destination_root = root / ".github" / "skills"
    marker = destination_root / MARKER_NAME
    roles_file = root / "docs" / "team" / "expected-roles.yml"

    if not source_root.is_dir():
        raise ValueError(f"Canonical skills directory is missing: {source_root}")
    roles_data = yaml.safe_load(roles_file.read_text(encoding="utf-8"))
    roles = roles_data.get("roles") if isinstance(roles_data, dict) else None
    if not isinstance(roles, list) or not roles or any(not isinstance(role, str) for role in roles):
        raise ValueError(f"Expected a non-empty roles list in {roles_file}")
    if len(roles) != len(set(roles)):
        raise ValueError("Canonical expected-roles.yml contains duplicate roles.")

    if destination_root.exists() and not marker.is_file():
        raise ValueError(
            f"{destination_root} exists without the generator marker; refusing to overwrite it."
        )
    if write:
        destination_root.mkdir(parents=True, exist_ok=True)
        marker.write_text(
            "Generated from canonical skills/. Do not edit these copies directly.\n",
            encoding="utf-8",
        )

    findings = []
    for role in roles:
        source = source_root / role
        destination = destination_root / role
        if not source.is_dir() or not (source / "SKILL.md").is_file():
            raise ValueError(f"Canonical role skill is missing: {source / 'SKILL.md'}")
        if write:
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(source, destination)
        elif not destination.is_dir():
            findings.append(f"Missing Copilot skill mirror: {role}")
            continue

        if snapshot(source) != snapshot(destination):
            findings.append(f"Copilot skill mirror is out of sync: {role}")

    expected = set(roles)
    actual = {
        item.name for item in destination_root.iterdir()
        if item.is_dir()
    } if destination_root.exists() else set()
    for extra in sorted(actual - expected):
        findings.append(f"Unexpected directory in generated Copilot skills: {extra}")

    return findings


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        findings = synchronize(write=args.write)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}")
        return 2
    if findings:
        print("\n".join(f"ERROR: {item}" for item in findings))
        return 1
    print(
        "Copilot skill mirrors synchronized from canonical skills/."
        if args.write else
        "Copilot skill mirrors match all canonical role skills."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
