#!/usr/bin/env python3
"""Validate lifecycle transitions and governance conditions for one execution."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys

import yaml

from validation_common import ROOT, report


RECORD_FILES = {
    "execution": ("execution.yml", "execution", False, "execution_id"),
    "work_items": ("work-items.yml", "work_items", True, "work_item_id"),
    "role_activations": ("role-activations.yml", "role_activations", True, "activation_id"),
    "dependencies": ("dependencies.yml", "dependencies", True, "dependency_id"),
    "handoff_executions": ("handoff-executions.yml", "handoff_executions", True, "handoff_execution_id"),
    "decisions": ("decisions.yml", "decisions", True, "decision_id"),
    "evidence": ("evidence.yml", "evidence", True, "evidence_id"),
    "blockers": ("blockers.yml", "blockers", True, "blocker_id"),
    "replans": ("replans.yml", "replans", True, "replan_id"),
    "closure": ("closure.yml", "closure", False, "closure_id"),
}

WORK_ITEM_TRANSITIONS = {
    "not_started": {"ready", "cancelled"},
    "ready": {"in_progress", "blocked", "cancelled"},
    "in_progress": {"blocked", "in_review", "completed", "cancelled"},
    "blocked": {"ready", "cancelled"},
    "in_review": {"completed", "changes_requested", "blocked"},
    "changes_requested": {"ready", "blocked", "cancelled"},
    "completed": set(),
    "cancelled": set(),
}

DEPENDENCY_TRANSITIONS = {
    "planned": {"active", "not_applicable", "cancelled"},
    "active": {"satisfied", "blocked", "cancelled"},
    "blocked": {"active", "satisfied", "cancelled"},
    "satisfied": {"active", "cancelled"},
    "not_applicable": {"active", "cancelled"},
    "cancelled": set(),
}

HANDOFF_TRANSITIONS = {
    "planned": {"in_progress", "cancelled"},
    "in_progress": {"submitted", "blocked", "cancelled"},
    "submitted": {"accepted", "partially_accepted", "rejected", "blocked"},
    "partially_accepted": {"in_progress", "blocked"},
    "rejected": {"in_progress", "blocked"},
    "blocked": {"in_progress", "submitted", "cancelled"},
    "accepted": set(),
    "cancelled": set(),
}

DECISION_TRANSITIONS = {
    "proposed": {"under_review", "withdrawn"},
    "under_review": {"approved", "rejected", "withdrawn"},
    "approved": {"superseded"},
    "rejected": set(),
    "superseded": set(),
    "withdrawn": set(),
}

BLOCKER_TRANSITIONS = {
    "open": {"in_progress", "blocked", "resolved", "deferred", "cancelled"},
    "in_progress": {"blocked", "resolved", "deferred", "cancelled"},
    "blocked": {"open", "in_progress", "deferred", "cancelled"},
    "deferred": {"open", "in_progress", "cancelled"},
    "resolved": set(),
    "cancelled": set(),
}

REPLAN_TRANSITIONS = {
    "proposed": {"under_review", "withdrawn"},
    "under_review": {"approved", "rejected", "withdrawn"},
    "approved": {"in_progress", "completed"},
    "in_progress": {"completed"},
    "rejected": set(),
    "completed": set(),
    "withdrawn": set(),
}

CLOSURE_TRANSITIONS = {
    "not_started": {"in_preparation", "cancelled"},
    "in_preparation": {"in_review", "blocked", "cancelled"},
    "in_review": {"in_preparation", "blocked", "closed", "cancelled"},
    "blocked": {"in_preparation", "cancelled"},
    "closed": set(),
    "cancelled": set(),
}

WORKFLOW_STATUSES = {
    "proposed", "planned", "in_progress", "blocked", "in_review",
    "verified", "released", "deferred", "cancelled",
}
WORKFLOW_TRANSITIONS = {
    "proposed": {"planned", "deferred", "cancelled"},
    "planned": {"in_progress", "blocked", "deferred", "cancelled"},
    "in_progress": {"in_review", "blocked", "deferred", "cancelled"},
    "in_review": {"verified", "blocked", "in_progress", "deferred", "cancelled"},
    "verified": {"released"},
    "released": set(),
    "deferred": {"planned"},
    "cancelled": set(),
    "blocked": {"proposed", "planned", "in_progress", "in_review"},
}

ROLE_STATUSES = {"planned", "active", "completed", "deactivated", "not_activated"}
ROLE_CLASSIFICATIONS = {"required", "conditional", "optional", "not_activated"}
ROLE_COMPATIBILITY = {
    "required": {"planned", "active", "completed", "deactivated"},
    "conditional": ROLE_STATUSES,
    "optional": ROLE_STATUSES,
    "not_activated": {"not_activated"},
}
DEPENDENCY_STATUSES = set(DEPENDENCY_TRANSITIONS)
HANDOFF_STATUSES = set(HANDOFF_TRANSITIONS)
DECISION_STATUSES = set(DECISION_TRANSITIONS)
EVIDENCE_STATUSES = {"unverified", "verified", "invalid", "superseded"}
BLOCKER_STATUSES = set(BLOCKER_TRANSITIONS)
REPLAN_STATUSES = set(REPLAN_TRANSITIONS)
CLOSURE_STATUSES = set(CLOSURE_TRANSITIONS)
WORK_ITEM_STATES = set(WORK_ITEM_TRANSITIONS)


def add(errors, code, message):
    errors.append(f"[{code}] {message}")


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def parse_timestamp(value):
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        return None
    return parsed


def read_execution(directory, errors):
    records = {}
    for kind, (filename, wrapper, collection, _) in RECORD_FILES.items():
        path = directory / filename
        if not path.is_file():
            add(errors, "LIFE001", f"Missing required file: {path.relative_to(ROOT)}")
            continue
        try:
            payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            add(errors, "LIFE002", f"Cannot parse {path.relative_to(ROOT)}: {exc}")
            continue
        if not isinstance(payload, dict) or set(payload) != {wrapper}:
            add(errors, "LIFE003", f"{path.relative_to(ROOT)} must contain only '{wrapper}'")
            continue
        value = payload.get(wrapper)
        if collection:
            if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
                add(errors, "LIFE004", f"{path.relative_to(ROOT)}.{wrapper} must be an array of mappings")
                continue
        elif not isinstance(value, dict):
            add(errors, "LIFE005", f"{path.relative_to(ROOT)}.{wrapper} must be a mapping")
            continue
        records[kind] = value
    return records


def history_time(entry, label, errors):
    raw = entry.get("changed_at", entry.get("timestamp", entry.get("occurred_at")))
    parsed = parse_timestamp(raw)
    if parsed is None:
        add(errors, "LIFE006", f"{label} needs a valid timezone-aware history timestamp")
    return parsed


def history_value(entry, key, field):
    values = entry.get(key)
    return values.get(field) if isinstance(values, dict) else None


def validate_history(record, label, current_updated_at, errors):
    history = record.get("history")
    if not isinstance(history, list):
        add(errors, "LIFE007", f"{label}.history must be an array")
        return []
    if not history:
        add(errors, "LIFE007", f"{label}.history must contain the initial record-creation event")
    parsed = []
    for index, entry in enumerate(history):
        entry_label = f"{label}.history[{index}]"
        if not isinstance(entry, dict):
            add(errors, "LIFE008", f"{entry_label} must be a mapping")
            continue
        timestamp = history_time(entry, entry_label, errors)
        if not nonempty(entry.get("reason")):
            add(errors, "LIFE012", f"{entry_label}.reason must be a non-empty explanation")
        if timestamp is not None:
            parsed.append((timestamp, index, entry))
    for previous, current in zip(parsed, parsed[1:]):
        if current[0] < previous[0]:
            add(errors, "LIFE009", f"{label}.history is not chronological at entry {current[1]}")
    created = parse_timestamp(record.get("created_at"))
    if created is None:
        add(errors, "LIFE010", f"{label}.created_at must be a valid UTC timestamp")
    updated = parse_timestamp(current_updated_at)
    if updated is None:
        add(errors, "LIFE010", f"{label}.updated_at must be a valid UTC timestamp")
    elif created is not None and updated < created:
        add(errors, "LIFE011", f"{label}.updated_at precedes created_at")
    elif parsed and updated < parsed[-1][0]:
        add(errors, "LIFE011", f"{label}.updated_at precedes its latest history entry")
    if created is not None and parsed and parsed[0][0] < created:
        add(errors, "LIFE011", f"{label}.history begins before created_at")
    return [entry for _, _, entry in parsed]


def check_transition(label, old, new, allowed, errors, code):
    if old == new:
        add(errors, code, f"{label} records a status transition that does not change state ({old!r})")
        return
    if old not in allowed:
        add(errors, code, f"{label} has unknown previous state {old!r}")
        return
    if new not in allowed:
        add(errors, code, f"{label} has unknown new state {new!r}")
        return
    if new not in allowed[old]:
        add(errors, code, f"{label} has prohibited transition {old!r} -> {new!r}")


def check_status(record, label, field, allowed, errors, code):
    value = record.get(field)
    if value not in allowed:
        add(errors, code, f"{label}.{field} has unsupported value {value!r}")
        return None
    return value


def validate_execution_lifecycle(execution, errors):
    label = f"execution ({execution.get('execution_id', 'unknown')})"
    status = check_status(execution, label, "workflow_status", WORKFLOW_STATUSES, errors, "LIFE020")
    stage = execution.get("workflow_stage")
    valid_stages = {
        "intake", "qualification", "solution_framing", "planning", "execution",
        "integration_and_review", "verification", "release_readiness_and_release", "closure",
    }
    if stage not in valid_stages:
        add(errors, "LIFE021", f"{label}.workflow_stage has unsupported value {stage!r}")
    history = validate_history(execution, label, execution.get("updated_at"), errors)
    transitions = []
    stage_history = []
    last_non_blocked_status = None
    for index, entry in enumerate(history):
        old = history_value(entry, "previous_values", "workflow_status")
        new = history_value(entry, "new_values", "workflow_status")
        if new is not None:
            if old is not None:
                if old == "blocked":
                    if last_non_blocked_status is None or new != last_non_blocked_status:
                        add(errors, "LIFE022", f"{label}.history[{index}] must resume the most recent non-blocked workflow status after blocked")
                else:
                    check_transition(f"{label}.history[{index}].workflow_status", old, new, WORKFLOW_TRANSITIONS, errors, "LIFE022")
                    if transitions and old != transitions[-1]:
                        add(errors, "LIFE022", f"{label}.history[{index}] previous workflow status does not match the preceding recorded status")
                    if new == "blocked":
                        last_non_blocked_status = old
                    elif old == "blocked":
                        last_non_blocked_status = None
            transitions.append(new)
        old_stage = history_value(entry, "previous_values", "workflow_stage")
        new_stage = history_value(entry, "new_values", "workflow_stage")
        if new_stage is not None:
            if old_stage is not None and stage_history and old_stage != stage_history[-1]:
                add(errors, "LIFE024", f"{label}.history[{index}] previous workflow stage does not match the preceding recorded stage")
            stage_history.append(new_stage)
    if transitions and status != transitions[-1]:
        add(errors, "LIFE022", f"{label}.workflow_status does not match its latest recorded history value")
    if stage_history and stage != stage_history[-1]:
        add(errors, "LIFE024", f"{label}.workflow_stage does not match its latest recorded history value")
    final = execution.get("final_disposition")
    if status in {"verified", "released", "deferred", "cancelled"}:
        if not isinstance(final, dict):
            add(errors, "LIFE023", f"{label} terminal workflow status requires final_disposition")
        else:
            if final.get("status") != status:
                add(errors, "LIFE023", f"{label}.final_disposition.status must match workflow_status")
            if not nonempty(final.get("summary")) or not parse_timestamp(final.get("recorded_at")):
                add(errors, "LIFE025", f"{label}.final_disposition requires a summary and UTC recorded_at timestamp")
    elif final is not None:
        add(errors, "LIFE023", f"{label}.final_disposition is present before a terminal workflow disposition")


def validate_work_items(records, decisions, errors):
    decision_index = {item.get("decision_id"): item for item in decisions if nonempty(item.get("decision_id"))}
    for record in records:
        label = f"work item {record.get('work_item_id', 'unknown')}"
        current = check_status(record, label, "state", WORK_ITEM_STATES, errors, "LIFE030")
        history = validate_history(record, label, record.get("updated_at"), errors)
        transitions = []
        for index, entry in enumerate(history):
            old = history_value(entry, "previous_values", "state")
            new = history_value(entry, "new_values", "state")
            if new is not None:
                if old is not None:
                    check_transition(f"{label}.history[{index}].state", old, new, WORK_ITEM_TRANSITIONS, errors, "LIFE031")
                    if transitions and old != transitions[-1]:
                        add(errors, "LIFE031", f"{label}.history[{index}] previous state {old!r} does not match preceding recorded state {transitions[-1]!r}")
                transitions.append(new)
        if transitions and current != transitions[-1]:
            add(errors, "LIFE031", f"{label}.state does not match its latest recorded history value")
        if current == "completed" and not parse_timestamp(record.get("completed_at")):
            add(errors, "LIFE032", f"{label} in completed state requires completed_at")
        if current != "completed" and record.get("completed_at") is not None:
            add(errors, "LIFE032", f"{label}.completed_at is only valid when state is completed")
        planned = record.get("planned_completion_at")
        if planned is not None and parse_timestamp(planned) is None:
            add(errors, "LIFE033", f"{label}.planned_completion_at must be a UTC timestamp when present")
        completed = parse_timestamp(record.get("completed_at"))
        created = parse_timestamp(record.get("created_at"))
        if completed is not None and created is not None and completed < created:
            add(errors, "LIFE033", f"{label}.completed_at precedes created_at")
        updated = parse_timestamp(record.get("updated_at"))
        if completed is not None and updated is not None and completed > updated:
            add(errors, "LIFE033", f"{label}.completed_at is later than updated_at")
        if current == "cancelled":
            related = record.get("related_decision_ids", [])
            authorized = [
                decision_index.get(decision_id)
                for decision_id in related
                if isinstance(related, list) and decision_id in decision_index
            ] if isinstance(related, list) else []
            if not any(item and item.get("decision_status") == "approved" for item in authorized):
                add(errors, "LIFE034", f"{label} cancelled state requires a related approved scope or planning decision")


def validate_role_activations(records, errors):
    for record in records:
        label = f"role activation {record.get('activation_id', 'unknown')}"
        classification = record.get("classification")
        status = check_status(record, label, "activation_status", ROLE_STATUSES, errors, "LIFE040")
        if classification not in ROLE_CLASSIFICATIONS:
            add(errors, "LIFE041", f"{label}.classification has unsupported value {classification!r}")
        elif status not in ROLE_COMPATIBILITY[classification]:
            add(errors, "LIFE041", f"{label} classification {classification!r} is incompatible with status {status!r}")
        if classification == "conditional":
            applies = record.get("activation_trigger_applies")
            if not isinstance(applies, bool):
                add(errors, "LIFE042", f"{label} conditional activation requires boolean activation_trigger_applies")
            elif applies and status == "not_activated":
                add(errors, "LIFE042", f"{label} cannot be not_activated when its conditional trigger applies")
            elif not applies and status != "not_activated":
                add(errors, "LIFE042", f"{label} must be not_activated when its conditional trigger does not apply")
        if status in {"active", "completed", "deactivated"} and not parse_timestamp(record.get("activated_at")):
            add(errors, "LIFE043", f"{label} status {status!r} requires activated_at")
        if status == "completed" and not parse_timestamp(record.get("completed_at")):
            add(errors, "LIFE043", f"{label} completed status requires completed_at")
        if status == "deactivated" and not parse_timestamp(record.get("deactivated_at")):
            add(errors, "LIFE043", f"{label} deactivated status requires deactivated_at")
        created = parse_timestamp(record.get("created_at"))
        activated = parse_timestamp(record.get("activated_at"))
        completed = parse_timestamp(record.get("completed_at"))
        deactivated = parse_timestamp(record.get("deactivated_at"))
        if created and activated and activated < created:
            add(errors, "LIFE043", f"{label}.activated_at precedes created_at")
        if activated and completed and completed < activated:
            add(errors, "LIFE043", f"{label}.completed_at precedes activated_at")
        if activated and deactivated and deactivated < activated:
            add(errors, "LIFE043", f"{label}.deactivated_at precedes activated_at")
        if completed and deactivated and deactivated < completed:
            add(errors, "LIFE043", f"{label}.deactivated_at precedes completed_at")
        history = validate_history(record, label, record.get("updated_at"), errors)
        # Activation history uses previous_values/new_values maps. Governance
        # explicitly permits reactivation but does not define a full transition
        # matrix, so validate chronology and current-state traceability only.
        status_values = []
        for index, entry in enumerate(history):
            old = history_value(entry, "previous_values", "activation_status")
            new = history_value(entry, "new_values", "activation_status")
            if new is not None:
                if old is not None and status_values and old != status_values[-1]:
                    add(errors, "LIFE044", f"{label}.history[{index}] previous activation status {old!r} does not match preceding recorded status {status_values[-1]!r}")
                status_values.append(new)
        if status_values and status != status_values[-1]:
            add(errors, "LIFE044", f"{label}.activation_status does not match its latest recorded history value")


def validate_dependencies(records, errors):
    for record in records:
        label = f"dependency {record.get('dependency_id', 'unknown')}"
        current = check_status(record, label, "status", DEPENDENCY_STATUSES, errors, "LIFE050")
        relationship = record.get("relationship_type")
        if current == "not_applicable" and relationship != "conditional_input":
            add(errors, "LIFE051", f"{label} may use not_applicable only for conditional_input")
        history = validate_history(record, label, record.get("updated_at"), errors)
        transitions = []
        for index, entry in enumerate(history):
            old = history_value(entry, "previous_values", "status")
            new = history_value(entry, "new_values", "status")
            if old is None:
                old = entry.get("previous_status")
            if new is None:
                new = entry.get("new_status")
            if new is not None:
                if old is not None:
                    check_transition(f"{label}.history[{index}].status", old, new, DEPENDENCY_TRANSITIONS, errors, "LIFE052")
                    if transitions and old != transitions[-1]:
                        add(errors, "LIFE052", f"{label}.history[{index}] previous status {old!r} does not match preceding recorded status {transitions[-1]!r}")
                transitions.append(new)
        if transitions and current != transitions[-1]:
            add(errors, "LIFE052", f"{label}.status does not match its latest recorded history value")
        if current == "not_applicable" and relationship == "conditional_input" and not nonempty(record.get("activation_condition")):
            add(errors, "LIFE051", f"{label} not_applicable status requires activation_condition")


def validate_handoffs(records, errors):
    for record in records:
        label = f"handoff {record.get('handoff_execution_id', 'unknown')}"
        current = check_status(record, label, "current_status", HANDOFF_STATUSES, errors, "LIFE060")
        history = validate_history(record, label, record.get("updated_at"), errors)
        transitions = []
        for index, entry in enumerate(history):
            change_type = entry.get("change_type", "")
            if isinstance(change_type, str) and "status" in change_type.lower():
                old, new = entry.get("previous_value"), entry.get("new_value")
                if new is not None:
                    if old is not None:
                        check_transition(f"{label}.history[{index}]", old, new, HANDOFF_TRANSITIONS, errors, "LIFE061")
                        if transitions and old != transitions[-1]:
                            add(errors, "LIFE061", f"{label}.history[{index}] previous status does not match the preceding recorded status")
                    transitions.append(new)
        if transitions and current != transitions[-1]:
            add(errors, "LIFE061", f"{label}.current_status does not match its latest recorded status history")
        submissions = record.get("submissions")
        if not isinstance(submissions, list):
            add(errors, "LIFE062", f"{label}.submissions must be an array")
            submissions = []
        submission_times = []
        for index, submission in enumerate(submissions):
            if not isinstance(submission, dict):
                add(errors, "LIFE062", f"{label}.submissions[{index}] must be a mapping")
                continue
            stamp = parse_timestamp(submission.get("submitted_at"))
            if stamp is None:
                add(errors, "LIFE062", f"{label}.submissions[{index}].submitted_at must be timezone-aware")
            else:
                submission_times.append(stamp)
        if any(later < earlier for earlier, later in zip(submission_times, submission_times[1:])):
            add(errors, "LIFE062", f"{label}.submissions must be chronological")
        if current in {"submitted", "partially_accepted", "accepted", "rejected"}:
            if not nonempty(record.get("current_submission_id")):
                add(errors, "LIFE063", f"{label} status {current!r} requires current_submission_id")
        if current in {"partially_accepted", "accepted", "rejected"} and not nonempty(record.get("current_decision_id")):
            add(errors, "LIFE063", f"{label} status {current!r} requires current_decision_id")


def validate_decisions(records, errors):
    for record in records:
        label = f"decision {record.get('decision_id', 'unknown')}"
        current = check_status(record, label, "decision_status", DECISION_STATUSES, errors, "LIFE070")
        history = validate_history(record, label, record.get("updated_at"), errors)
        transitions = []
        for index, entry in enumerate(history):
            old, new = entry.get("previous_status"), entry.get("new_status")
            if new is not None:
                if old is not None:
                    check_transition(f"{label}.history[{index}]", old, new, DECISION_TRANSITIONS, errors, "LIFE071")
                    if transitions and old != transitions[-1]:
                        add(errors, "LIFE071", f"{label}.history[{index}] previous status does not match the preceding recorded status")
                transitions.append(new)
        if transitions and current != transitions[-1]:
            add(errors, "LIFE071", f"{label}.decision_status does not match its latest recorded history value")
        if current in {"approved", "rejected", "superseded"}:
            if not parse_timestamp(record.get("decided_at")):
                add(errors, "LIFE072", f"{label} status {current!r} requires decided_at")
            if not nonempty(record.get("decided_by_role")):
                add(errors, "LIFE072", f"{label} status {current!r} requires decided_by_role")
        elif current in {"proposed", "under_review", "withdrawn"} and record.get("decided_at") is not None:
            add(errors, "LIFE072", f"{label}.decided_at must be omitted before a decision is approved or rejected")
        if current == "approved" and not nonempty(record.get("selected_option")) and not nonempty(record.get("decision_outcome")):
            add(errors, "LIFE073", f"{label} approved status requires selected_option or decision_outcome")


def validate_evidence(records, errors):
    for record in records:
        label = f"evidence {record.get('evidence_id', 'unknown')}"
        current = check_status(record, label, "verification_status", EVIDENCE_STATUSES, errors, "LIFE080")
        history = validate_history(record, label, record.get("updated_at"), errors)
        values = []
        for entry in history:
            old, new = entry.get("previous_status"), entry.get("new_status")
            if new is not None:
                if old is not None and values and old != values[-1]:
                    add(errors, "LIFE081", f"{label} history previous status {old!r} does not match preceding recorded status {values[-1]!r}")
                values.append(new)
            if old is not None and old not in EVIDENCE_STATUSES:
                add(errors, "LIFE081", f"{label} history contains unknown previous verification status {old!r}")
            if new is not None and new not in EVIDENCE_STATUSES:
                add(errors, "LIFE081", f"{label} history contains unknown new verification status {new!r}")
        if values and current != values[-1]:
            add(errors, "LIFE081", f"{label}.verification_status does not match its latest recorded history value")
        if current in {"verified", "invalid"} and not nonempty(record.get("verification_notes")):
            add(errors, "LIFE082", f"{label} status {current!r} requires verification_notes")
        evidence_id = record.get("evidence_id")
        replacement_id = record.get("supersedes_evidence_id")
        if replacement_id:
            replacement = next(
                (other for other in records if other.get("evidence_id") == replacement_id),
                None,
            )
            if replacement is None:
                add(errors, "LIFE083", f"{label}.supersedes_evidence_id references a missing replacement {replacement_id}")
            elif replacement_id == evidence_id:
                add(errors, "LIFE083", f"{label} cannot supersede itself")
            elif replacement.get("verification_status") != "superseded":
                add(errors, "LIFE083", f"{label}.supersedes_evidence_id references {replacement_id}, but the previous evidence record is not marked superseded")
        if current == "superseded":
            replacements = [
                other for other in records
                if other.get("supersedes_evidence_id") == evidence_id
            ]
            if not replacements:
                add(errors, "LIFE083", f"{label} is superseded but no newer evidence record references it through supersedes_evidence_id")


def validate_blockers(records, decisions, errors):
    decision_index = {r.get("decision_id"): r for r in decisions if nonempty(r.get("decision_id"))}
    for record in records:
        label = f"blocker {record.get('blocker_id', 'unknown')}"
        current = check_status(record, label, "status", BLOCKER_STATUSES, errors, "LIFE090")
        history = validate_history(record, label, record.get("updated_at"), errors)
        transitions = []
        for index, entry in enumerate(history):
            old, new = entry.get("previous_status"), entry.get("new_status")
            if new is not None:
                if old is not None:
                    check_transition(f"{label}.history[{index}]", old, new, BLOCKER_TRANSITIONS, errors, "LIFE091")
                    if transitions and old != transitions[-1]:
                        add(errors, "LIFE091", f"{label}.history[{index}] previous status does not match the preceding recorded status")
                transitions.append(new)
        if transitions and current != transitions[-1]:
            add(errors, "LIFE091", f"{label}.status does not match its latest recorded history value")
        if current == "resolved":
            if not nonempty(record.get("resolution_summary")):
                add(errors, "LIFE092", f"{label} resolved status requires resolution_summary")
            if not parse_timestamp(record.get("resolved_at")):
                add(errors, "LIFE092", f"{label} resolved status requires resolved_at")
        elif record.get("resolved_at") is not None:
            add(errors, "LIFE092", f"{label}.resolved_at is only valid when status is resolved")
        if current == "deferred":
            refs = record.get("related_decision_ids", [])
            authorized = [
                decision_index.get(ref) for ref in refs if ref in decision_index
            ] if isinstance(refs, list) else []
            if not any(d and d.get("decision_status") == "approved" for d in authorized):
                add(errors, "LIFE093", f"{label} deferred status requires a related approved decision")


def validate_replans(records, decisions, errors):
    decision_index = {r.get("decision_id"): r for r in decisions if nonempty(r.get("decision_id"))}
    for record in records:
        label = f"replan {record.get('replan_id', 'unknown')}"
        current = check_status(record, label, "status", REPLAN_STATUSES, errors, "LIFE100")
        history = validate_history(record, label, record.get("updated_at"), errors)
        transitions = []
        for index, entry in enumerate(history):
            old, new = entry.get("previous_status"), entry.get("new_status")
            if new is not None:
                if old is not None:
                    check_transition(f"{label}.history[{index}]", old, new, REPLAN_TRANSITIONS, errors, "LIFE101")
                    if transitions and old != transitions[-1]:
                        add(errors, "LIFE101", f"{label}.history[{index}] previous status does not match the preceding recorded status")
                transitions.append(new)
        if transitions and current != transitions[-1]:
            add(errors, "LIFE101", f"{label}.status does not match its latest recorded history value")
        decision_id = record.get("decision_id")
        decision = decision_index.get(decision_id)
        if current in {"approved", "in_progress", "completed"}:
            if not decision or decision.get("decision_status") != "approved":
                add(errors, "LIFE102", f"{label} status {current!r} requires its approved authorizing decision")
        if current == "completed" and not parse_timestamp(record.get("implemented_at")):
            add(errors, "LIFE103", f"{label} completed status requires implemented_at")
        elif current != "completed" and record.get("implemented_at") is not None:
            add(errors, "LIFE103", f"{label}.implemented_at is only valid when status is completed")


def validate_closure(record, decisions, errors):
    label = f"closure {record.get('closure_id', 'unknown')}"
    current = check_status(record, label, "closure_status", CLOSURE_STATUSES, errors, "LIFE110")
    history = validate_history(record, label, record.get("updated_at"), errors)
    transitions = []
    for index, entry in enumerate(history):
        event_type = entry.get("event_type")
        if event_type == "closure_status_changed":
            old, new = entry.get("previous_value"), entry.get("new_value")
            if new is not None:
                if old is not None:
                    check_transition(f"{label}.history[{index}]", old, new, CLOSURE_TRANSITIONS, errors, "LIFE111")
                    if transitions and old != transitions[-1]:
                        add(errors, "LIFE111", f"{label}.history[{index}] previous status does not match the preceding recorded status")
                transitions.append(new)
    if transitions and current != transitions[-1]:
        add(errors, "LIFE111", f"{label}.closure_status does not match its latest recorded status history")
    decision_index = {r.get("decision_id"): r for r in decisions if nonempty(r.get("decision_id"))}
    decision_id = record.get("closure_decision_id")
    decision = decision_index.get(decision_id)
    if current == "closed":
        if not decision or decision.get("decision_type") != "execution_closure" or decision.get("decision_status") != "approved":
            add(errors, "LIFE112", f"{label} closed status requires an approved execution_closure decision")
        closed_at = parse_timestamp(record.get("closed_at"))
        if closed_at is None:
            add(errors, "LIFE112", f"{label} closed status requires UTC closed_at")
        closure_events = [
            entry for entry in history
            if entry.get("event_type") == "closure_status_changed"
            and entry.get("new_value") == "closed"
        ]
        approval_events = [
            entry for entry in history
            if entry.get("event_type") == "closure_approved"
        ]
        if not closure_events or not approval_events:
            add(errors, "LIFE112", f"{label} closed status requires closure_status_changed and closure_approved history events")
        elif closed_at is not None:
            event_time = parse_timestamp(closure_events[-1].get("occurred_at"))
            if event_time is not None and event_time != closed_at:
                add(errors, "LIFE112", f"{label}.closed_at must match the recorded closure status event timestamp")
        if decision_id and approval_events:
            refs = approval_events[-1].get("related_record_refs", [])
            if not isinstance(refs, list) or decision_id not in refs:
                add(errors, "LIFE112", f"{label} closure_approved history event must reference closure decision {decision_id}")
    elif record.get("closed_at") is not None:
        add(errors, "LIFE112", f"{label}.closed_at is only valid when closure_status is closed")
    if current == "cancelled":
        if not decision or decision.get("decision_status") != "approved":
            add(errors, "LIFE113", f"{label} cancelled status requires an approved cancellation decision")
        cancellation_events = [
            entry for entry in history
            if entry.get("event_type") == "closure_cancelled"
            or (
                entry.get("event_type") == "closure_status_changed"
                and entry.get("new_value") == "cancelled"
            )
        ]
        if not cancellation_events:
            add(errors, "LIFE113", f"{label} cancelled status requires a cancellation history event")
    completion = record.get("completion", {})
    verification = record.get("verification", {})
    exceptions = record.get("exceptions", [])
    approved_exceptions = (
        any(isinstance(item, dict) and item.get("status") == "approved" for item in exceptions)
        if isinstance(exceptions, list) else False
    )
    if isinstance(completion, dict) and completion.get("status") == "complete_with_exceptions" and not approved_exceptions:
        add(errors, "LIFE114", f"{label} complete_with_exceptions requires an approved exception")
    if isinstance(verification, dict) and verification.get("status") == "passed_with_exceptions" and not approved_exceptions:
        add(errors, "LIFE114", f"{label} passed_with_exceptions requires an approved exception")


def validate_execution(directory):
    errors, warnings = [], []
    records = read_execution(directory, errors)
    if len(records) != len(RECORD_FILES):
        return report(errors, warnings, "Execution lifecycle validation")
    execution = records["execution"]
    if directory.name != execution.get("execution_id"):
        add(errors, "LIFE000", "Execution directory name must match execution.execution_id")

    validate_execution_lifecycle(execution, errors)
    validate_work_items(records["work_items"], records["decisions"], errors)
    validate_role_activations(records["role_activations"], errors)
    validate_dependencies(records["dependencies"], errors)
    validate_handoffs(records["handoff_executions"], errors)
    validate_decisions(records["decisions"], errors)
    validate_evidence(records["evidence"], errors)
    validate_blockers(records["blockers"], records["decisions"], errors)
    validate_replans(records["replans"], records["decisions"], errors)
    validate_closure(records["closure"], records["decisions"], errors)
    return report(errors, warnings, "Execution lifecycle validation")


def main():
    parser = argparse.ArgumentParser(
        description="Validate lifecycle transitions and governance conditions for one execution."
    )
    parser.add_argument("execution_directory", help="Repository-relative path such as executions/EXE-<UUID>")
    args = parser.parse_args()
    candidate = (ROOT / args.execution_directory).resolve()
    executions_root = (ROOT / "executions").resolve()
    try:
        candidate.relative_to(executions_root)
    except ValueError:
        print("ERROR: Execution directory must be inside executions/.")
        return 2
    if candidate.parent != executions_root:
        print("ERROR: Execution directory must be a direct child of executions/.")
        return 2
    if not candidate.is_dir():
        print(f"ERROR: Execution directory does not exist: {args.execution_directory}")
        return 2
    try:
        return validate_execution(candidate)
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
