#!/usr/bin/env python3
"""Check baseline pre-run governance without creating approvals or run evidence."""

from pathlib import Path
import argparse
import json
import re
import sys

import yaml

from validation_common import ROOT, expected_roles

SCENARIO_DIR = ROOT / "tests/scenarios"
DECISION_REGISTER = ROOT / "docs/evaluation/baseline/stakeholder-decisions.yml"
EXPECTED_DECISIONS = {
    "DAILY-SUMMARY-METRIC-SEMANTICS",
    "REPORTING-TIMEZONE-DAY-BOUNDARY",
    "INGRESS-TELEMETRY-TREATMENT",
    "SAME-ORDER-DISTINCT-EVENT-POLICY",
    "DELAY-THRESHOLD-OR-RETRY-INTERVAL",
}
DATE_TIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})$")


def _read_yaml(path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc


def validate_decision_register(path=None):
    errors, blockers = [], []
    path = path or DECISION_REGISTER
    try:
        data = _read_yaml(path)
    except ValueError as exc:
        return [str(exc)], blockers

    if not isinstance(data, dict) or data.get("schema_version") != 1:
        return ["decision register must be a mapping with schema_version: 1"], blockers
    decisions = data.get("decisions")
    if not isinstance(decisions, list):
        return ["decision register decisions must be a list"], blockers

    seen = set()
    for index, item in enumerate(decisions):
        label = f"decisions[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be a mapping")
            continue
        decision_id = item.get("id")
        if not isinstance(decision_id, str) or not decision_id.strip():
            errors.append(f"{label}.id must be a non-empty string")
            continue
        if decision_id in seen:
            errors.append(f"duplicate stakeholder decision ID: {decision_id}")
        seen.add(decision_id)

        status = item.get("status")
        if status not in {"open", "confirmed", "non_scored"}:
            errors.append(f"{decision_id}: status must be open, confirmed, or non_scored")
            continue
        for field in ("question", "owner", "affected_roles"):
            value = item.get(field)
            if field == "affected_roles":
                if not isinstance(value, list) or not value or any(not isinstance(v, str) or not v.strip() for v in value):
                    errors.append(f"{decision_id}: affected_roles must be a non-empty string list")
            elif not isinstance(value, str) or not value.strip():
                errors.append(f"{decision_id}: {field} must be non-empty")

        if status == "open":
            blockers.append(f"{decision_id} is unresolved")
            for field in ("decision", "rationale", "authorized_by", "authorized_at", "evidence_ref", "non_scored_scope"):
                if item.get(field) is not None:
                    errors.append(f"{decision_id}: open decisions must not contain {field}")
        else:
            for field in ("decision", "rationale", "authorized_by", "authorized_at", "evidence_ref"):
                value = item.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{decision_id}: {field} is required for {status}")
            timestamp = item.get("authorized_at")
            if isinstance(timestamp, str) and not DATE_TIME_RE.fullmatch(timestamp):
                errors.append(f"{decision_id}: authorized_at must be an ISO-8601 timestamp with timezone")
            if status == "non_scored":
                scope = item.get("non_scored_scope")
                if not isinstance(scope, str) or not scope.strip():
                    errors.append(f"{decision_id}: non_scored_scope is required for non_scored disposition")
            elif item.get("non_scored_scope") is not None:
                errors.append(f"{decision_id}: confirmed decisions must not contain non_scored_scope")

    missing = sorted(EXPECTED_DECISIONS - seen)
    unexpected = sorted(seen - EXPECTED_DECISIONS)
    if missing:
        errors.append("decision register is missing required decisions: " + ", ".join(missing))
    if unexpected:
        errors.append("decision register contains unrecognized decisions: " + ", ".join(unexpected))
    return errors, blockers


def validate_scenario_approvals(scenario_dir=None):
    errors, blockers = [], []
    scenario_dir = scenario_dir or SCENARIO_DIR
    expected = set(expected_roles())
    found_roles = set()
    paths = sorted(scenario_dir.glob("SCEN-BASELINE-*.yml"))
    if len(paths) != len(expected):
        errors.append(f"expected {len(expected)} baseline scenarios; found {len(paths)}")

    for path in paths:
        try:
            scenario = _read_yaml(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not isinstance(scenario, dict):
            errors.append(f"{path}: scenario must be a YAML mapping")
            continue
        scenario_id = scenario.get("id", path.stem)
        role = scenario.get("role")
        if role not in expected:
            errors.append(f"{scenario_id}: role is not canonical")
        elif role in found_roles:
            errors.append(f"{scenario_id}: duplicate baseline scenario role {role}")
        else:
            found_roles.add(role)

        if scenario.get("status") != "approved":
            blockers.append(f"{scenario_id} is not approved")
            continue
        approval = scenario.get("approval")
        if not isinstance(approval, dict):
            errors.append(f"{scenario_id}: approved scenario requires approval metadata")
            continue
        for field in ("approved_by", "approved_at"):
            value = approval.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{scenario_id}: approval.{field} must be non-empty")
        approved_at = approval.get("approved_at")
        if isinstance(approved_at, str) and not DATE_TIME_RE.fullmatch(approved_at):
            errors.append(f"{scenario_id}: approval.approved_at must be ISO-8601 with timezone")

    missing_roles = sorted(expected - found_roles)
    if missing_roles:
        errors.append("missing baseline scenarios for roles: " + ", ".join(missing_roles))
    return errors, blockers


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check stakeholder dispositions and human scenario approvals before baseline execution."
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    decision_errors, decision_blockers = validate_decision_register()
    approval_errors, approval_blockers = validate_scenario_approvals()
    errors = decision_errors + approval_errors
    blockers = decision_blockers + approval_blockers
    result = {
        "status": "ERROR" if errors else ("BLOCKED" if blockers else "GOVERNANCE-CLEAR"),
        "errors": errors,
        "blockers": blockers,
        "scenario_approvals_required": len(expected_roles()),
        "stakeholder_decisions_required": len(EXPECTED_DECISIONS),
        "execution_authorized": False,
    }
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("Baseline pre-run governance check")
        print(f"Status: {result['status']}")
        print(f"Scenario approvals required: {result['scenario_approvals_required']}")
        print(f"Stakeholder decisions required: {result['stakeholder_decisions_required']}")
        for error in errors:
            print(f"ERROR: {error}")
        for blocker in blockers:
            print(f"BLOCKER: {blocker}")
        print("This check does not authorize execution or validate cohort revision pins.")
    if errors:
        return 2
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())
