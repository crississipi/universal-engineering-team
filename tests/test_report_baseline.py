"""Tests for baseline report aggregation and rendering."""

import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

spec = importlib.util.spec_from_file_location(
    "report_baseline", SCRIPTS / "report-baseline.py"
)
reporter = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = reporter
spec.loader.exec_module(reporter)


def scenario(scenario_id="SCEN-BASELINE-TEST", role="product-analyst", status="draft"):
    return {
        "id": scenario_id,
        "role": role,
        "title": "Test scenario",
        "status": status,
        "criteria": [
            {"id": "C1", "description": "Criterion one", "weight": 60},
            {"id": "C2", "description": "Criterion two", "weight": 40},
        ],
    }


def record(run_number=1, *, scenario_id="SCEN-BASELINE-TEST", role="product-analyst",
           scores=None, comparable=True, failures=None, decision=None, cohort="cohort-a"):
    return {
        "run_id": f"BASELINE-{scenario_id}-RUN-{run_number:02d}",
        "scenario_id": scenario_id,
        "role": role,
        "run_number": run_number,
        "scores": scores if scores is not None else [
            {"criterion_id": "C1", "score": 80, "rationale": "Evidence"},
            {"criterion_id": "C2", "score": 100, "rationale": "Evidence"},
        ],
        "critical_failures": failures or [],
        "comparability": {
            "cohort_id": cohort,
            "comparable_within_scenario_cohort": comparable,
            "deviations": [],
        },
        "review": {"decision": decision},
    }


class BaselineReportTests(unittest.TestCase):
    def test_empty_draft_cohort_reports_zero_actual_runs_and_no_scores(self):
        result = reporter.build_report({
            "SCEN-BASELINE-TEST": scenario()
        }, [])
        self.assertEqual(result["status"]["planned_scenarios"], 1)
        self.assertEqual(result["status"]["planned_runs"], 10)
        self.assertEqual(result["status"]["draft_scenarios"], 1)
        self.assertEqual(result["status"]["approved_scenarios"], 0)
        self.assertEqual(result["status"]["recorded_runs"], 0)
        self.assertEqual(result["status"]["scored_runs"], 0)
        self.assertIsNone(result["status"]["weighted_score"]["mean"])
        self.assertIsNone(result["scenarios"][0]["expected_runs"])
        self.assertEqual(result["scenarios"][0]["missing_run_numbers"], [])
        self.assertEqual(result["cohorts"], [])

    def test_weighted_score_uses_rubric_weights(self):
        item = scenario()
        run = record(scores=[
            {"criterion_id": "C1", "score": 50, "rationale": "Evidence"},
            {"criterion_id": "C2", "score": 100, "rationale": "Evidence"},
        ])
        self.assertEqual(reporter.weighted_score(run, item), 70.0)

    def test_weighted_score_is_unavailable_when_any_criterion_is_unscored(self):
        item = scenario()
        run = record(scores=[
            {"criterion_id": "C1", "score": 50, "rationale": "Evidence"},
            {"criterion_id": "C2", "score": None, "rationale": None},
        ])
        self.assertIsNone(reporter.weighted_score(run, item))

    def test_weighted_score_rejects_boolean_score(self):
        item = scenario()
        run = record(scores=[
            {"criterion_id": "C1", "score": True, "rationale": "Evidence"},
            {"criterion_id": "C2", "score": 100, "rationale": "Evidence"},
        ])
        self.assertIsNone(reporter.weighted_score(run, item))

    def test_weighted_score_rejects_non_finite_score(self):
        item = scenario()
        run = record(scores=[
            {"criterion_id": "C1", "score": float("nan"), "rationale": "Evidence"},
            {"criterion_id": "C2", "score": 100, "rationale": "Evidence"},
        ])
        self.assertIsNone(reporter.weighted_score(run, item))

    def test_approved_scenario_reports_missing_run_numbers(self):
        result = reporter.build_report({
            "SCEN-BASELINE-TEST": scenario(status="approved")
        }, [record(1)])
        row = result["scenarios"][0]
        self.assertEqual(row["expected_runs"], 10)
        self.assertEqual(row["missing_run_numbers"], list(range(2, 11)))

    def test_draft_scenario_does_not_report_missing_runs(self):
        result = reporter.build_report({
            "SCEN-BASELINE-TEST": scenario(status="draft")
        }, [])
        self.assertEqual(result["scenarios"][0]["missing_run_numbers"], [])

    def test_cohort_rollup_excludes_false_and_unconfirmed_comparability(self):
        runs = [
            record(1, comparable=True),
            record(2, comparable=False),
            record(3, comparable=None),
        ]
        result = reporter.build_report({"SCEN-BASELINE-TEST": scenario()}, runs)
        cohort = result["cohorts"][0]
        self.assertEqual(cohort["recorded_runs"], 3)
        self.assertEqual(cohort["explicitly_comparable_runs"], 1)
        self.assertEqual(cohort["excluded_unconfirmed_or_non_comparable_runs"], 2)
        self.assertEqual(cohort["scored_comparable_runs"], 1)
        self.assertEqual(cohort["weighted_score"]["mean"], 88.0)

    def test_cohort_role_summaries_keep_roles_separate(self):
        second = scenario("SCEN-BASELINE-TEST-2", "backend-developer")
        runs = [
            record(1),
            record(1, scenario_id="SCEN-BASELINE-TEST-2", role="backend-developer"),
        ]
        result = reporter.build_report({
            "SCEN-BASELINE-TEST": scenario(),
            "SCEN-BASELINE-TEST-2": second,
        }, runs)
        self.assertEqual(
            [item["role"] for item in result["cohorts"][0]["roles"]],
            ["backend-developer", "product-analyst"],
        )
        self.assertEqual(len(result["cohorts"][0]["roles"]), 2)

    def test_critical_failures_and_review_decisions_are_separate_from_score(self):
        run = record(failures=["Unauthorized production action"], decision="blocked")
        result = reporter.build_report({"SCEN-BASELINE-TEST": scenario()}, [run])
        row = result["scenarios"][0]
        self.assertEqual(result["status"]["critical_failure_entries"], 1)
        self.assertEqual(row["critical_failures"][0]["failures"], ["Unauthorized production action"])
        self.assertEqual(row["review_decisions"], {"blocked": 1})
        self.assertEqual(row["scored_runs"], 1)

    def test_markdown_states_no_cohort_data_without_inventing_scores(self):
        result = reporter.build_report({"SCEN-BASELINE-TEST": scenario()}, [])
        markdown = reporter.render_markdown(result)
        self.assertIn("No cohort records exist", markdown)
        self.assertIn("Actual run records", markdown)
        self.assertIn("| 0 |", markdown)
        self.assertNotIn("0.00", markdown)

    def test_report_preserves_individual_run_score_and_review(self):
        run = record(4, decision="needs_changes", failures=["Missing test evidence"])
        result = reporter.build_report({"SCEN-BASELINE-TEST": scenario()}, [run])
        details = result["scenarios"][0]["runs"][0]
        self.assertEqual(details["run_number"], 4)
        self.assertEqual(details["weighted_score"], 88.0)
        self.assertEqual(details["review_decision"], "needs_changes")
        self.assertEqual(details["critical_failures"], ["Missing test evidence"])
        markdown = reporter.render_markdown(result)
        self.assertIn("Individual run scores", markdown)
        self.assertIn("needs_changes", markdown)


if __name__ == "__main__":
    unittest.main()
