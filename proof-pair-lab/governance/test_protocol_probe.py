"""Executable conformance scenarios for the shared execution protocol."""

import unittest

from governance.protocol_probe import (
    correction_attempt_count,
    evaluate_dependency,
    requires_immediate_escalation,
    should_escalate_after_corrections,
)


class ConditionalDependencyScenarios(unittest.TestCase):
    def test_inactive_conditional_input_does_not_block(self):
        decision = evaluate_dependency(
            "conditional_input", activation_applies=False
        )
        self.assertEqual(decision.status, "not_applicable")
        self.assertFalse(decision.blocks_successor)

    def test_active_unsatisfied_conditional_input_blocks_dependent_gate(self):
        decision = evaluate_dependency(
            "conditional_input",
            activation_applies=True,
            prerequisite_satisfied=False,
        )
        self.assertEqual(decision.status, "active")
        self.assertTrue(decision.blocks_successor)

    def test_active_satisfied_conditional_input_does_not_block(self):
        decision = evaluate_dependency(
            "conditional_input",
            activation_applies=True,
            prerequisite_satisfied=True,
        )
        self.assertEqual(decision.status, "satisfied")
        self.assertFalse(decision.blocks_successor)

    def test_conditional_input_requires_explicit_activation_decision(self):
        with self.assertRaises(ValueError):
            evaluate_dependency("conditional_input")


class FeedbackScenarios(unittest.TestCase):
    def test_feedback_alone_does_not_block(self):
        decision = evaluate_dependency("feedback")
        self.assertFalse(decision.blocks_successor)
        self.assertEqual(decision.status, "planned")

    def test_feedback_can_block_when_task_acceptance_explicitly_requires_it(self):
        decision = evaluate_dependency(
            "feedback",
            feedback_is_explicit_acceptance_criterion=True,
            prerequisite_satisfied=False,
        )
        self.assertTrue(decision.blocks_successor)
        self.assertEqual(decision.status, "active")

    def test_satisfied_required_feedback_criterion_does_not_block(self):
        decision = evaluate_dependency(
            "feedback",
            feedback_is_explicit_acceptance_criterion=True,
            prerequisite_satisfied=True,
        )
        self.assertFalse(decision.blocks_successor)
        self.assertEqual(decision.status, "satisfied")


class CorrectionAttemptScenarios(unittest.TestCase):
    def test_repeated_command_or_same_approach_counts_once(self):
        attempts = [
            ("change-timeout", False),
            ("change-timeout", False),
            ("change-timeout", False),
        ]
        self.assertEqual(correction_attempt_count(attempts), 1)
        self.assertFalse(should_escalate_after_corrections(attempts))

    def test_three_distinct_unsuccessful_approaches_trigger_escalation(self):
        attempts = [
            ("increase-timeout", False),
            ("add-retry-with-backoff", False),
            ("replace-blocking-call-with-queue", False),
        ]
        self.assertEqual(correction_attempt_count(attempts), 3)
        self.assertTrue(should_escalate_after_corrections(attempts))

    def test_successful_attempt_is_not_an_unsuccessful_correction(self):
        attempts = [
            ("approach-a", False),
            ("approach-b", False),
            ("approach-c", True),
        ]
        self.assertEqual(correction_attempt_count(attempts), 2)
        self.assertFalse(should_escalate_after_corrections(attempts))

    def test_attempts_are_counted_for_the_same_increment_only(self):
        first_increment = [("approach-a", False), ("approach-b", False)]
        second_increment = [("approach-c", False)]
        self.assertFalse(should_escalate_after_corrections(first_increment))
        self.assertFalse(should_escalate_after_corrections(second_increment))


class ImmediateEscalationScenarios(unittest.TestCase):
    def test_critical_severity_escalates_immediately(self):
        self.assertTrue(requires_immediate_escalation(severity="critical"))

    def test_permission_and_authorization_triggers_escalate_immediately(self):
        self.assertTrue(
            requires_immediate_escalation(
                severity="medium", risk_triggers=["permission"]
            )
        )
        self.assertTrue(
            requires_immediate_escalation(
                severity="low", risk_triggers=["authorization"]
            )
        )

    def test_urgent_security_privacy_safety_and_integrity_triggers_escalate(self):
        for trigger in (
            "security",
            "privacy",
            "safety",
            "data_integrity",
            "production_stability",
        ):
            with self.subTest(trigger=trigger):
                self.assertTrue(
                    requires_immediate_escalation(
                        severity="high", risk_triggers=[trigger]
                    )
                )

    def test_ordinary_medium_blocker_does_not_escalate_immediately(self):
        self.assertFalse(requires_immediate_escalation(severity="medium"))


if __name__ == "__main__":
    unittest.main()
