#!/usr/bin/env python3
"""Generate evidence-backed baseline evaluation reports from validated run records."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import importlib.util
import json
import math
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
VALIDATOR_PATH = SCRIPTS / "validate-baseline.py"


def load_validator():
    """Load the canonical baseline validator without duplicating its rules."""
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location("validate_baseline", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load baseline validator: {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def mean(values):
    return sum(values) / len(values) if values else None


def score_statistics(values):
    numeric = [
        float(value) for value in values
        if isinstance(value, (int, float)) and not isinstance(value, bool)
        and math.isfinite(value)
    ]
    return {
        "count": len(numeric),
        "mean": mean(numeric),
        "minimum": min(numeric) if numeric else None,
        "maximum": max(numeric) if numeric else None,
    }


def weighted_score(record, scenario):
    """Return a weighted score only when every rubric criterion is numerically scored."""
    criteria = scenario.get("criteria", [])
    weights = {
        item.get("id"): item.get("weight")
        for item in criteria
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    scores = {
        item.get("criterion_id"): item.get("score")
        for item in record.get("scores", [])
        if isinstance(item, dict)
    }
    if not criteria or len(weights) != len(criteria) or set(scores) != set(weights):
        return None
    if any(
        not isinstance(scores[key], (int, float))
        or isinstance(scores[key], bool)
        or not math.isfinite(scores[key])
        or not isinstance(weights[key], (int, float))
        or isinstance(weights[key], bool)
        or not math.isfinite(weights[key])
        for key in weights
    ):
        return None
    denominator = sum(weights.values())
    if denominator <= 0:
        return None
    return sum(float(scores[key]) * float(weights[key]) for key in weights) / denominator


def criterion_statistics(records, scenario):
    results = []
    for criterion in scenario.get("criteria", []):
        criterion_id = criterion.get("id")
        values = [
            next(
                (item.get("score") for item in record.get("scores", [])
                 if item.get("criterion_id") == criterion_id),
                None,
            )
            for record in records
        ]
        results.append({
            "criterion_id": criterion_id,
            "description": criterion.get("description"),
            "weight": criterion.get("weight"),
            **score_statistics(values),
        })
    return results


def load_report_data(root=ROOT):
    """Load scenarios and real records after running the canonical validator."""
    validator = load_validator()
    runs_dir = root / "evaluations/baseline/runs"
    validation = validator.validate_run_records(runs_dir, root)
    if validation["errors"]:
        raise ValueError(
            "Baseline records failed validation:\n"
            + "\n".join(validation["errors"])
        )

    scenarios, scenario_errors = validator.load_scenario_catalog(root)
    if scenario_errors:
        raise ValueError("Scenario catalog is invalid:\n" + "\n".join(scenario_errors))

    records = []
    if runs_dir.is_dir():
        for path in sorted(runs_dir.glob("*.yml")):
            record = validator.load_yaml(path)
            if isinstance(record, dict):
                records.append(record)

    return build_report(scenarios, records, validation["warnings"])


def build_report(scenarios, records, validation_warnings=None):
    """Build deterministic report data; never infer approvals, runs, or scores."""
    validation_warnings = list(validation_warnings or [])
    scenario_records = defaultdict(list)
    cohort_records = defaultdict(list)
    for record in records:
        scenario_records[record["scenario_id"]].append(record)
        cohort_records[record["comparability"]["cohort_id"]].append(record)

    scenario_rows = []
    approval_counts = Counter()
    critical_failure_count = 0

    for scenario_id, scenario in sorted(scenarios.items()):
        status = scenario.get("status", "unknown")
        approved = status == "approved"
        approval_counts[status] += 1
        actual = sorted(
            scenario_records.get(scenario_id, []),
            key=lambda item: item["run_number"],
        )
        run_numbers = {record["run_number"] for record in actual}
        missing = sorted(set(range(1, 11)) - run_numbers) if approved else []
        failures = [
            {"run_id": record["run_id"], "failures": list(record.get("critical_failures", []))}
            for record in actual
            if record.get("critical_failures")
        ]
        critical_failure_count += sum(len(item["failures"]) for item in failures)

        cohort_summaries = []
        scenario_cohort_ids = sorted({
            record["comparability"]["cohort_id"] for record in actual
        })
        for cohort_id in scenario_cohort_ids:
            cohort_runs = [
                record for record in actual
                if record["comparability"]["cohort_id"] == cohort_id
            ]
            comparable = [
                record for record in cohort_runs
                if record.get("comparability", {}).get("comparable_within_scenario_cohort") is True
            ]
            weighted = [
                value for record in comparable
                if (value := weighted_score(record, scenario)) is not None
            ]
            cohort_summaries.append({
                "cohort_id": cohort_id,
                "recorded_runs": len(cohort_runs),
                "explicitly_comparable_runs": len(comparable),
                "excluded_unconfirmed_or_non_comparable_runs": len(cohort_runs) - len(comparable),
                "scored_comparable_runs": len(weighted),
                "weighted_score": score_statistics(weighted),
                "criteria": criterion_statistics(comparable, scenario),
            })

        scenario_rows.append({
            "scenario_id": scenario_id,
            "role": scenario.get("role"),
            "title": scenario.get("title"),
            "status": status,
            "approved": approved,
            "recorded_runs": len(actual),
            "scored_runs": sum(
                weighted_score(record, scenario) is not None for record in actual
            ),
            "expected_runs": 10 if approved else None,
            "missing_run_numbers": missing,
            "cohorts": cohort_summaries,
            "runs": [
                {
                    "run_id": record["run_id"],
                    "run_number": record["run_number"],
                    "cohort_id": record["comparability"]["cohort_id"],
                    "weighted_score": weighted_score(record, scenario),
                    "criterion_scores": list(record.get("scores", [])),
                    "comparable": record.get("comparability", {}).get("comparable_within_scenario_cohort"),
                    "critical_failures": list(record.get("critical_failures", [])),
                    "limitations": list(record.get("limitations", [])),
                    "review_decision": record.get("review", {}).get("decision"),
                }
                for record in actual
            ],
            "critical_failures": failures,
            "review_decisions": dict(Counter(
                record.get("review", {}).get("decision") or "not_reviewed"
                for record in actual
            )),
        })

    cohorts = []
    for cohort_id, cohort in sorted(cohort_records.items()):
        eligible = [
            record for record in cohort
            if record.get("comparability", {}).get("comparable_within_scenario_cohort") is True
        ]
        eligible_scores = [
            value for record in eligible
            if (value := weighted_score(record, scenarios[record["scenario_id"]])) is not None
        ]
        role_groups = defaultdict(list)
        for record in eligible:
            role_groups[record["role"]].append(record)
        role_summaries = []
        for role, role_runs in sorted(role_groups.items()):
            role_scores = [
                value for record in role_runs
                if (value := weighted_score(record, scenarios[record["scenario_id"]])) is not None
            ]
            role_summaries.append({
                "role": role,
                "recorded_runs": len(role_runs),
                "scored_runs": len(role_scores),
                "weighted_score": score_statistics(role_scores),
            })
        cohorts.append({
            "cohort_id": cohort_id,
            "recorded_runs": len(cohort),
            "explicitly_comparable_runs": len(eligible),
            "scored_comparable_runs": len(eligible_scores),
            "excluded_unconfirmed_or_non_comparable_runs": len(cohort) - len(eligible),
            "weighted_score": score_statistics(eligible_scores),
            "roles": role_summaries,
        })

    planned_scenarios = len(scenarios)
    planned_runs = planned_scenarios * 10
    recorded_runs = len(records)
    return {
        "report_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "status": {
            "planned_scenarios": planned_scenarios,
            "draft_scenarios": approval_counts.get("draft", 0),
            "approved_scenarios": approval_counts.get("approved", 0),
            "other_scenario_statuses": {
                key: value for key, value in sorted(approval_counts.items())
                if key not in {"draft", "approved"}
            },
            "planned_runs": planned_runs,
            "recorded_runs": recorded_runs,
            "scored_runs": sum(row["scored_runs"] for row in scenario_rows),
            "critical_failure_entries": critical_failure_count,
        },
        "scenarios": scenario_rows,
        "cohorts": cohorts,
        "validation_warnings": validation_warnings,
        "interpretation": [
            "Only committed scenario status and actual validated run records are counted.",
            "Draft scenarios are not treated as approved and are not assigned missing-run counts.",
            "A weighted run score exists only when every criterion has a numeric score.",
            "Scenario score statistics are kept separate by cohort; unlike cohorts are never averaged together.",
            "Cross-role cohort statistics include only runs explicitly marked comparable_within_scenario_cohort: true.",
            "Critical failures and human review decisions are reported separately from numeric scores.",
            "This report does not approve scenarios, authenticate reviewers, or establish model quality.",
        ],
    }


def format_number(value, digits=2):
    return "—" if value is None else f"{value:.{digits}f}"


def render_markdown(report):
    status = report["status"]
    lines = [
        "# Baseline evaluation report",
        "",
        f"> Generated: {report['generated_at_utc']} (UTC). This report is derived only from validated repository records.",
        "",
        "## Cohort and approval status",
        "",
        "| Measure | Count |",
        "|---|---:|",
        f"| Planned scenarios | {status['planned_scenarios']} |",
        f"| Draft scenarios | {status['draft_scenarios']} |",
        f"| Approved scenarios | {status['approved_scenarios']} |",
        f"| Planned runs (10 per planned scenario) | {status['planned_runs']} |",
        f"| Actual run records | {status['recorded_runs']} |",
        f"| Runs with complete numeric weighted scores | {status['scored_runs']} |",
        f"| Critical-failure entries | {status['critical_failure_entries']} |",
        "",
        "Planned runs are a target, not evidence that execution occurred. Scores are never averaged across different cohorts.",
        "",
        "## Scenario results",
        "",
        "| Scenario | Role | Status | Records | Scored | Missing approved run numbers |",
        "|---|---|---|---:|---:|---|",
    ]
    for row in report["scenarios"]:
        missing = ", ".join(f"{number:02d}" for number in row["missing_run_numbers"]) or "—"
        lines.append(
            f"| {row['scenario_id']} | {row['role']} | {row['status']} | "
            f"{row['recorded_runs']} | {row['scored_runs']} | {missing} |"
        )

    lines.extend(["", "## Individual run scores", ""])
    any_runs = False
    for row in report["scenarios"]:
        if not row["runs"]:
            continue
        any_runs = True
        lines.extend([
            f"### {row['scenario_id']} ({row['role']})",
            "",
            "| Run | Cohort | Weighted score | Comparable | Critical failures | Limitations | Human review |",
            "|---:|---|---:|---|---|---|---|",
        ])
        for run in row["runs"]:
            score = format_number(run["weighted_score"])
            comparable = "yes" if run["comparable"] is True else ("no" if run["comparable"] is False else "unconfirmed")
            failures_text = "; ".join(run["critical_failures"]) or "—"
            limitations_text = "; ".join(run["limitations"]) or "—"
            review = run["review_decision"] or "not reviewed"
            lines.append(
                f"| {run['run_number']:02d} | {run['cohort_id']} | {score} | "
                f"{comparable} | {failures_text} | {limitations_text} | {review} |"
            )
        lines.append("")
    if not any_runs:
        lines.extend(["No individual run scores exist because no run records are present.", ""])

    lines.extend(["## Scenario scores by cohort", ""])
    any_scenario_cohort = False
    for row in report["scenarios"]:
        for cohort in row["cohorts"]:
            any_scenario_cohort = True
            stats = cohort["weighted_score"]
            lines.extend([
                f"### {row['scenario_id']} / {cohort['cohort_id']}",
                "",
                f"- Recorded runs: {cohort['recorded_runs']}",
                f"- Explicitly comparable runs: {cohort['explicitly_comparable_runs']}",
                f"- Excluded because comparability is false or unconfirmed: {cohort['excluded_unconfirmed_or_non_comparable_runs']}",
                f"- Scored comparable runs: {cohort['scored_comparable_runs']}",
                f"- Weighted-score mean: {format_number(stats['mean'])}",
                f"- Weighted-score range: {format_number(stats['minimum'])}–{format_number(stats['maximum'])}",
                "",
                "| Criterion | Weight | Numeric scores | Mean | Range |",
                "|---|---:|---:|---:|---:|",
            ])
            for criterion in cohort["criteria"]:
                range_text = "—"
                if criterion["count"]:
                    range_text = f"{format_number(criterion['minimum'])}–{format_number(criterion['maximum'])}"
                lines.append(
                    f"| {criterion['criterion_id']} | {criterion['weight']} | {criterion['count']} | "
                    f"{format_number(criterion['mean'])} | {range_text} |"
                )
            lines.append("")
    if not any_scenario_cohort:
        lines.extend(["No scenario run records exist; no score statistics are available.", ""])

    lines.extend(["## Comparable cross-role cohort summaries", ""])
    if not report["cohorts"]:
        lines.extend(["No cohort records exist. No cross-role score summary is available.", ""])
    for cohort in report["cohorts"]:
        stats = cohort["weighted_score"]
        lines.extend([
            f"### {cohort['cohort_id']}",
            "",
            f"- Recorded runs: {cohort['recorded_runs']}",
            f"- Explicitly comparable runs: {cohort['explicitly_comparable_runs']}",
            f"- Scored comparable runs: {cohort['scored_comparable_runs']}",
            f"- Excluded because comparability is false or unconfirmed: {cohort['excluded_unconfirmed_or_non_comparable_runs']}",
            f"- Mean comparable weighted score: {format_number(stats['mean'])}",
            "",
        ])
        if cohort["roles"]:
            lines.extend([
                "| Role | Comparable records | Scored runs | Weighted mean |",
                "|---|---:|---:|---:|",
            ])
            for role in cohort["roles"]:
                lines.append(
                    f"| {role['role']} | {role['recorded_runs']} | {role['scored_runs']} | "
                    f"{format_number(role['weighted_score']['mean'])} |"
                )
            lines.append("")
        else:
            lines.extend(["No runs in this cohort are explicitly marked comparable.", ""])

    lines.extend(["## Critical failures and human review", ""])
    any_failures = False
    for row in report["scenarios"]:
        for item in row["critical_failures"]:
            any_failures = True
            lines.append(f"- **{row['scenario_id']} / {item['run_id']}**: " + "; ".join(item["failures"]))
    if not any_failures:
        lines.append("No critical-failure entries are present in the validated run records.")
    lines.append("")
    lines.append("Human review decisions are listed per scenario in the JSON report; an absent decision is not treated as a pass.")
    lines.append("")

    lines.extend(["## Validation warnings", ""])
    if report["validation_warnings"]:
        lines.extend(f"- {warning}" for warning in report["validation_warnings"])
    else:
        lines.append("None.")
    lines.extend(["", "## Interpretation and limitations", ""])
    lines.extend(f"- {item}" for item in report["interpretation"])
    lines.append("")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate baseline evaluation summaries from validated, actual run records."
    )
    parser.add_argument(
        "--format", choices=("markdown", "json"), default="markdown",
        help="Report format (default: markdown).",
    )
    args = parser.parse_args(argv)
    try:
        report = load_report_data()
    except (OSError, ValueError, yaml.YAMLError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
