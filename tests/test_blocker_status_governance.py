"""Keep blocker lifecycle documentation and JSON Schema in sync."""

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "docs/team/blocker-records.md"
OVERVIEW = ROOT / "docs/team/blockers-replanning-and-state-transitions.md"
SCHEMA = ROOT / "schemas/executions/blockers.schema.json"

EXPECTED_STATUSES = {
    "open",
    "in_progress",
    "blocked",
    "escalated",
    "deferred",
    "resolved",
    "closed",
    "cancelled",
}

EXPECTED_TRANSITIONS = {
    "open": {"in_progress", "blocked", "escalated", "resolved", "deferred", "cancelled"},
    "in_progress": {"blocked", "escalated", "resolved", "deferred", "cancelled"},
    "blocked": {"open", "in_progress", "escalated", "resolved", "deferred", "cancelled"},
    "escalated": {"in_progress", "blocked", "resolved", "deferred", "cancelled"},
    "deferred": {"open", "in_progress", "blocked", "escalated", "resolved", "cancelled"},
    "resolved": {"closed"},
    "closed": set(),
    "cancelled": set(),
}


def section(text, heading, next_heading):
    start = text.index(heading)
    end = text.index(next_heading, start)
    return text[start:end]


def table_statuses(text):
    return set(re.findall(r"^\| `([a-z_]+)` \|", text, re.MULTILINE))


def parse_transitions(text):
    result = {}
    for current, destinations in re.findall(
        r"^\| `([a-z_]+)` \| (.*?) \|$",
        text,
        re.MULTILINE,
    ):
        if current not in EXPECTED_STATUSES:
            continue
        if destinations == "Terminal":
            result[current] = set()
        else:
            result[current] = set(re.findall(r"`([a-z_]+)`", destinations))
    return result


class BlockerStatusGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records_text = RECORDS.read_text(encoding="utf-8")
        cls.overview_text = OVERVIEW.read_text(encoding="utf-8")
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        cls.item = cls.schema["$defs"]["document"]["properties"]["blockers"]["items"]

    def test_record_specification_declares_canonical_statuses(self):
        status_section = section(
            self.records_text,
            "## 7. Blocker Status",
            "## 8. Responsibility and Escalation",
        )
        self.assertEqual(table_statuses(status_section), EXPECTED_STATUSES)

    def test_transition_table_matches_governed_transitions(self):
        status_section = section(
            self.records_text,
            "### 7.1 Status Transitions",
            "### 7.2 Resolution and Closure Requirements",
        )
        self.assertEqual(parse_transitions(status_section), EXPECTED_TRANSITIONS)

    def test_schema_status_and_history_enums_match_specification(self):
        self.assertEqual(set(self.item["properties"]["status"]["enum"]), EXPECTED_STATUSES)
        history = self.item["properties"]["history"]["items"]["properties"]
        self.assertEqual(set(history["previous_status"]["enum"]), EXPECTED_STATUSES)
        self.assertEqual(set(history["new_status"]["enum"]), EXPECTED_STATUSES)

    def test_lifecycle_overview_points_to_all_canonical_statuses(self):
        overview = section(
            self.overview_text,
            "### 4.5 Blocker statuses",
            "### 4.6 Blocker ownership",
        )
        for status in EXPECTED_STATUSES:
            self.assertIn(f"`{status}`", overview)

    def test_closed_status_requires_verification_and_closure_timestamp(self):
        closed_rule = next(
            rule for rule in self.item["allOf"]
            if rule.get("if", {}).get("properties", {}).get("status", {}).get("const") == "closed"
        )
        self.assertEqual(
            set(closed_rule["then"]["required"]),
            {"resolution_summary", "resolution_evidence_refs", "resolved_at", "closed_at"},
        )
        self.assertEqual(
            self.item["properties"]["resolution_evidence_refs"]["items"],
            {"$ref": "./definitions/identifiers.schema.json#/$defs/evdId"},
        )
        self.assertEqual(
            closed_rule["then"]["properties"]["resolution_evidence_refs"]["minItems"],
            1,
        )
        self.assertIn("closed_at", self.item["properties"])

    def test_resolved_status_requires_resolution_but_not_closure(self):
        resolved_rule = next(
            rule for rule in self.item["allOf"]
            if rule.get("if", {}).get("properties", {}).get("status", {}).get("const") == "resolved"
        )
        self.assertEqual(
            set(resolved_rule["then"]["required"]),
            {"resolution_summary", "resolved_at"},
        )
        self.assertNotIn("closed_at", resolved_rule["then"]["required"])


if __name__ == "__main__":
    unittest.main()
