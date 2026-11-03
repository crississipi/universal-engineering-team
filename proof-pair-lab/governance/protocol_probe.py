"""Small reference model for documented collaboration protocol semantics.

This module is a conformance probe, not a production orchestration engine.
It deliberately models only decisions that can be derived from the current
governance documents. It does not create execution records or authorize work.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class DependencyDecision:
    status: str
    blocks_successor: bool
    reason: str


def evaluate_dependency(
    relationship_type: str,
    *,
    prerequisite_satisfied: bool = False,
    activation_applies: bool | None = None,
    feedback_is_explicit_acceptance_criterion: bool = False,
) -> DependencyDecision:
    """Evaluate whether a relationship blocks its successor's dependent gate."""
    if relationship_type == "required_input":
        if prerequisite_satisfied:
            return DependencyDecision("satisfied", False, "Required input is satisfied.")
        return DependencyDecision("active", True, "Required input remains unresolved.")

    if relationship_type == "conditional_input":
        if activation_applies is None:
            raise ValueError("Conditional input requires an explicit activation decision.")
        if not activation_applies:
            return DependencyDecision(
                "not_applicable", False, "Activation condition does not apply."
            )
        if prerequisite_satisfied:
            return DependencyDecision("satisfied", False, "Activated input is satisfied.")
        return DependencyDecision(
            "active", True, "Activation condition applies and its input is unresolved."
        )

    if relationship_type == "feedback":
        if feedback_is_explicit_acceptance_criterion:
            if prerequisite_satisfied:
                return DependencyDecision(
                    "satisfied", False, "Required feedback criterion is satisfied."
                )
            return DependencyDecision(
                "active", True, "Task acceptance criteria explicitly require this feedback."
            )
        return DependencyDecision(
            "planned",
            False,
            "Feedback does not block by default; assess findings separately.",
        )

    raise ValueError(f"Unsupported relationship type: {relationship_type}")


def correction_attempt_count(attempts: Iterable[tuple[str, bool]]) -> int:
    """Count distinct unsuccessful approaches for one unresolved increment.

    Each tuple is (approach_key, successful). Re-running an approach does not
    add an attempt. Callers must use the same input collection for one
    unresolved increment; separate increments must be counted separately.
    """
    unsuccessful_approaches: set[str] = set()
    for approach_key, successful in attempts:
        key = approach_key.strip()
        if not key:
            raise ValueError("Every correction attempt requires an approach key.")
        if not successful:
            unsuccessful_approaches.add(key)
    return len(unsuccessful_approaches)


def should_escalate_after_corrections(
    attempts: Iterable[tuple[str, bool]],
) -> bool:
    """Escalate after three materially different unsuccessful approaches."""
    return correction_attempt_count(attempts) >= 3


IMMEDIATE_ESCALATION_TRIGGERS = frozenset(
    {
        "security",
        "privacy",
        "safety",
        "data_integrity",
        "production_stability",
        "permission",
        "authorization",
    }
)


def requires_immediate_escalation(
    *,
    severity: str,
    risk_triggers: Iterable[str] = (),
) -> bool:
    """Return true for critical blockers or explicitly urgent risk categories."""
    normalized = {trigger.strip().lower() for trigger in risk_triggers}
    return severity.strip().lower() == "critical" or bool(
        normalized & IMMEDIATE_ESCALATION_TRIGGERS
    )
