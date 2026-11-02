#!/usr/bin/env python3
"""Validate cross-record references and consistency for one execution directory."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import sys

import yaml

from validation_common import ROOT, expected_roles, load_yaml, report


RECORD_FILES = {
    "execution": ("execution.yml", "execution", False, "execution_id"),
    "work_items": ("work-items.yml", "work_items", True, "work_item_id"),
    "role_activations": (
        "role-activations.yml", "role_activations", True, "activation_id"
    ),
    "dependencies": ("dependencies.yml", "dependencies", True, "dependency_id"),
    "handoff_executions": (
        "handoff-executions.yml", "handoff_executions", True,
        "handoff_execution_id"
    ),
    "decisions": ("decisions.yml", "decisions", True, "decision_id"),
    "evidence": ("evidence.yml", "evidence", True, "evidence_id"),
    "blockers": ("blockers.yml", "blockers", True, "blocker_id"),
    "replans": ("replans.yml", "replans", True, "replan_id"),
    "closure": ("closure.yml", "closure", False, "closure_id"),
}

ID_TO_KIND = {
    "WI": "work_items",
    "ACT": "role_activations",
    "DEP": "dependencies",
    "HEX": "handoff_executions",
    "DEC": "decisions",
    "EVD": "evidence",
    "BLK": "blockers",
    "RPL": "replans",
    "CLS": "closure",
}

ROOT_INDEX_FIELDS = {
    "work_item_ids": "work_items",
    "activation_ids": "role_activations",
    "dependency_ids": "dependencies",
    "handoff_execution_ids": "handoff_executions",
    "decision_ids": "decisions",
    "evidence_ids": "evidence",
    "blocker_ids": "blockers",
    "replan_ids": "replans",
}

CROSS_REFERENCE_FIELDS = {
    "related_decision_ids": "decisions",
    "evidence_refs": "evidence",
    "related_blocker_ids": "blockers",
    "related_handoff_execution_ids": "handoff_executions",
    "affected_dependency_ids": "dependencies",
    "affected_work_item_ids": "work_items",
    "affected_role_activation_ids": "role_activations",
    "affected_handoff_execution_ids": "handoff_executions",
    "affected_blocker_ids": "blockers",
}

ROLE_FIELDS = {
    "coordinator_role", "changed_by_role", "role_id", "assigned_role",
    "from_role", "to_role", "submitted_by_role", "proposed_by_role",
    "decided_by_role", "produced_by_role", "verified_by_role",
    "reported_by_role", "responsible_role", "coordinated_by_role",
    "closure_authorized_by_role", "actor_role", "checked_by_role",
}

def add(errors, code, message):
    errors.append(f"[{code}] {message}")


def is_non_empty(value):
    return isinstance(value, str) and bool(value.strip())


def as_list(value, label, errors, required=False):
    if value is None and not required:
        return []
    if not isinstance(value, list):
        add(errors, "REF001", f"{label} must be a list")
        return []
    return value


def string_set(value, label, errors):
    values = as_list(value, label, errors, required=True)
    result = set()
    for index, item in enumerate(values):
        if not is_non_empty(item):
            add(errors, "REF066", f"{label}[{index}] must be a non-empty string")
            continue
        if item in result:
            add(errors, "REF067", f"{label} contains duplicate {item}")
        result.add(item)
    return result


def load_execution_document(path, wrapper, collection, errors):
    if not path.is_file():
        add(errors, "REF002", f"Required execution record file is missing: {path.relative_to(ROOT)}")
        return None

    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        add(errors, "REF003", f"Could not parse {path.relative_to(ROOT)}: {exc}")
        return None

    if not isinstance(value, dict) or set(value) != {wrapper}:
        add(errors, "REF004", f"{path.relative_to(ROOT)} must contain only the top-level '{wrapper}' key")
        return None

    payload = value.get(wrapper)
    if collection:
        if not isinstance(payload, list):
            add(errors, "REF005", f"{path.relative_to(ROOT)}.{wrapper} must be an array")
            return None
        if any(not isinstance(item, dict) for item in payload):
            add(errors, "REF006", f"{path.relative_to(ROOT)}.{wrapper} must contain only mappings")
            return None
        return payload

    if not isinstance(payload, dict):
        add(errors, "REF007", f"{path.relative_to(ROOT)}.{wrapper} must be a mapping")
        return None
    return payload


def index_records(kind, records, id_field, errors):
    indexed = {}
    for index, record in enumerate(records):
        record_id = record.get(id_field)
        label = f"{kind}[{index}]"
        if not is_non_empty(record_id):
            add(errors, "REF008", f"{label}.{id_field} must be a non-empty string")
            continue
        if record_id in indexed:
            add(errors, "REF009", f"Duplicate {id_field}: {record_id}")
            continue
        indexed[record_id] = record
    return indexed


def resolve(record_id, kind, indexes, label, errors, optional=False):
    if record_id is None and optional:
        return None
    if not is_non_empty(record_id):
        add(errors, "REF010", f"{label} must be a non-empty identifier")
        return None
    target = indexes.get(kind, {}).get(record_id)
    if target is None:
        add(errors, "REF011", f"{label} references missing {kind} record {record_id}")
    return target


def resolve_id_by_prefix(record_id, indexes, artifacts, label, errors):
    if not is_non_empty(record_id):
        add(errors, "REF012", f"{label} must contain a non-empty canonical reference")
        return
    if record_id.startswith("ART-"):
        if record_id not in artifacts:
            add(errors, "REF013", f"{label} references unknown artifact package {record_id}")
        return
    prefix = record_id.split("-", 1)[0]
    kind = ID_TO_KIND.get(prefix)
    if kind is None:
        add(errors, "REF014", f"{label} uses an unsupported canonical reference {record_id}")
        return
    resolve(record_id, kind, indexes, label, errors)


def validate_role_fields(value, roles, label, errors):
    if isinstance(value, dict):
        for key, child in value.items():
            child_label = f"{label}.{key}"
            if key in ROLE_FIELDS and child is not None:
                if not isinstance(child, str) or child not in roles:
                    add(errors, "REF015", f"{child_label} is not a canonical role slug")
            validate_role_fields(child, roles, child_label, errors)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            validate_role_fields(child, roles, f"{label}[{index}]", errors)


def validate_execution_identity(execution, directory, records, errors):
    execution_id = execution.get("execution_id")
    if not is_non_empty(execution_id):
        add(errors, "REF016", "execution.execution_id must be a non-empty string")
        return None
    if directory.name != execution_id:
        add(errors, "REF017", f"Execution directory '{directory.name}' does not match execution_id '{execution_id}'")
    for kind, entries in records.items():
        if kind in {"execution", "closure"}:
            continue
        for index, record in enumerate(entries):
            actual = record.get("execution_id")
            if actual != execution_id:
                add(errors, "REF018", f"{kind}[{index}].execution_id must match root execution {execution_id}")
    closure = records.get("closure")
    if isinstance(closure, dict) and closure.get("execution_id") != execution_id:
        add(errors, "REF018", f"closure.execution_id must match root execution {execution_id}")
    return execution_id


def validate_root_index(execution, indexes, errors):
    refs = execution.get("record_refs")
    if not isinstance(refs, dict):
        add(errors, "REF019", "execution.record_refs must be a mapping")
        return
    for field, kind in ROOT_INDEX_FIELDS.items():
        values = as_list(refs.get(field), f"execution.record_refs.{field}", errors, required=True)
        seen = set()
        for index, value in enumerate(values):
            label = f"execution.record_refs.{field}[{index}]"
            if is_non_empty(value):
                if value in seen:
                    add(errors, "REF020", f"{label} duplicates {value}")
                seen.add(value)
            resolve(value, kind, indexes, label, errors)
    closure_id = refs.get("closure_id")
    if closure_id is not None:
        resolve(closure_id, "closure", indexes, "execution.record_refs.closure_id", errors)
        if indexes.get("closure") and is_non_empty(closure_id) and closure_id not in indexes["closure"]:
            add(errors, "REF060", f"execution.record_refs.closure_id does not match the canonical closure record")


def validate_activation_work_items(indexes, errors):
    work_items = indexes["work_items"]
    activations = indexes["role_activations"]

    active_roles = {}
    for activation_id, activation in activations.items():
        role = activation.get("role_id")
        if activation.get("activation_status") == "active" and isinstance(role, str) and role:
            if role in active_roles:
                add(errors, "REF021", f"Role {role} has multiple active activation records: {active_roles[role]} and {activation_id}")
            else:
                active_roles[role] = activation_id

        listed = as_list(activation.get("work_item_ids"), f"role activation {activation_id}.work_item_ids", errors)
        for work_item_id in listed:
            work_item = resolve(work_item_id, "work_items", indexes, f"role activation {activation_id}.work_item_ids", errors)
            if work_item and work_item.get("activation_id") != activation_id:
                add(errors, "REF022", f"Role activation {activation_id} lists {work_item_id}, but the work item points to a different activation")

    for work_item_id, work_item in work_items.items():
        activation_id = work_item.get("activation_id")
        activation = resolve(activation_id, "role_activations", indexes, f"work item {work_item_id}.activation_id", errors)
        if activation:
            if activation.get("role_id") != work_item.get("assigned_role"):
                add(errors, "REF023", f"Work item {work_item_id}.assigned_role does not match activation {activation_id}.role_id")
            state = work_item.get("state")
            activation_status = activation.get("activation_status")
            if state in {"in_progress", "in_review", "changes_requested"} and activation_status != "active":
                add(errors, "REF024", f"Work item {work_item_id} in state {state!r} requires active role activation {activation_id}")
            if state in {"not_started", "ready"} and activation_status not in {"planned", "active"}:
                add(errors, "REF024", f"Work item {work_item_id} in state {state!r} has incompatible activation status {activation_status!r}")
            if state == "completed" and activation_status not in {"active", "completed"}:
                add(errors, "REF024", f"Completed work item {work_item_id} has incompatible activation status {activation_status!r}")
            if state == "cancelled" and activation_status not in {"planned", "active", "completed", "deactivated", "not_activated"}:
                add(errors, "REF024", f"Cancelled work item {work_item_id} has incompatible activation status {activation_status!r}")


def validate_dependency_graph(indexes, errors):
    work_items = indexes["work_items"]
    dependencies = indexes["dependencies"]
    adjacency = defaultdict(list)

    for dependency_id, dependency in dependencies.items():
        predecessor_id = dependency.get("predecessor_work_item_id")
        successor_id = dependency.get("successor_work_item_id")
        predecessor = resolve(predecessor_id, "work_items", indexes, f"dependency {dependency_id}.predecessor_work_item_id", errors)
        successor = resolve(successor_id, "work_items", indexes, f"dependency {dependency_id}.successor_work_item_id", errors)

        if predecessor_id == successor_id and predecessor_id:
            add(errors, "REF026", f"Dependency {dependency_id} cannot reference the same predecessor and successor")
        if predecessor and successor:
            adjacency[predecessor_id].append(successor_id)
    
        for field, kind in (
            ("satisfaction_evidence_refs", "evidence"),
            ("related_decision_ids", "decisions"),
            ("related_blocker_ids", "blockers"),
            ("handoff_execution_refs", "handoff_executions"),
        ):
            for index, ref in enumerate(as_list(dependency.get(field), f"dependency {dependency_id}.{field}", errors)):
                resolve(ref, kind, indexes, f"dependency {dependency_id}.{field}[{index}]", errors)

    # Every dependency edge participates in the governed acyclic dependency graph.
    visiting = set()
    visited = set()

    def visit(node, stack):
        if node in visiting:
            cycle = " -> ".join(stack + [node])
            add(errors, "REF028", f"Dependency graph contains a cycle: {cycle}")
            return
        if node in visited:
            return
        visiting.add(node)
        for successor in adjacency.get(node, []):
            visit(successor, stack + [node])
        visiting.remove(node)
        visited.add(node)

    for work_item_id in work_items:
        visit(work_item_id, [])


def validate_handoffs(indexes, artifacts, contracts, errors, warnings):
    handoffs = indexes["handoff_executions"]
    dependencies = indexes["dependencies"]
    if handoffs and not contracts:
        warnings.append("Handoff execution records exist, but docs/team/ownership.yml declares no reusable handoff contracts; contract-level consistency could not be checked.")

    seen_submission_ids = set()
    for handoff_id, handoff in handoffs.items():
        contract_id = handoff.get("handoff_contract_id")
        if not is_non_empty(contract_id):
            add(errors, "REF068", f"Handoff execution {handoff_id}.handoff_contract_id must be a non-empty contract identifier")
        contract = contracts.get(contract_id) if isinstance(contract_id, str) else None
        if contract_id and contracts and contract is None:
            add(errors, "REF029", f"Handoff execution {handoff_id} references unknown handoff contract {contract_id}")
        if contract:
            if contract.get("status") != "active":
                add(errors, "REF030", f"Handoff execution {handoff_id} references contract {contract_id} whose status is not active")
            for field in ("from_role", "to_role", "artifact_id", "consumer_artifact_id"):
                if field in contract and handoff.get(field) != contract.get(field):
                    add(errors, "REF030", f"Handoff execution {handoff_id}.{field} does not match reusable contract {contract_id}")

        producer = resolve(handoff.get("producer_work_item_id"), "work_items", indexes, f"handoff {handoff_id}.producer_work_item_id", errors)
        consumer = resolve(handoff.get("consumer_work_item_id"), "work_items", indexes, f"handoff {handoff_id}.consumer_work_item_id", errors)
        if producer and producer.get("assigned_role") != handoff.get("from_role"):
            add(errors, "REF031", f"Handoff {handoff_id} producer work item is not assigned to from_role")
        if consumer and consumer.get("assigned_role") != handoff.get("to_role"):
            add(errors, "REF032", f"Handoff {handoff_id} consumer work item is not assigned to to_role")

        artifact_id = handoff.get("artifact_id")
        if artifact_id is not None and (not is_non_empty(artifact_id) or artifact_id not in artifacts):
            add(errors, "REF033", f"Handoff {handoff_id} references unknown producer artifact {artifact_id}")
        consumer_artifact = handoff.get("consumer_artifact_id")
        if consumer_artifact is not None and (not is_non_empty(consumer_artifact) or consumer_artifact not in artifacts):
            add(errors, "REF034", f"Handoff {handoff_id} references unknown consumer artifact {consumer_artifact}")

        submissions = as_list(handoff.get("submissions"), f"handoff {handoff_id}.submissions", errors, required=True)
        submission_index = {}
        for index, submission in enumerate(submissions):
            if not isinstance(submission, dict):
                continue
            submission_id = submission.get("submission_id")
            if not is_non_empty(submission_id):
                add(errors, "REF035", f"handoff {handoff_id}.submissions[{index}].submission_id must be non-empty")
                continue
            if submission_id in submission_index:
                add(errors, "REF036", f"Handoff {handoff_id} has duplicate submission_id {submission_id}")
            if submission_id in seen_submission_ids:
                add(errors, "REF036", f"Submission ID {submission_id} is duplicated across handoff executions")
            seen_submission_ids.add(submission_id)
            submission_index[submission_id] = submission

            decision_id = submission.get("decision_id")
            if decision_id:
                decision = resolve(decision_id, "decisions", indexes, f"handoff {handoff_id} submission {submission_id}.decision_id", errors)
                if decision and decision.get("decision_type") != "handoff_acceptance":
                    add(errors, "REF037", f"Handoff submission {submission_id} decision must have decision_type 'handoff_acceptance'")

            for field in ("output_refs", "context_refs"):
                for ref_index, reference in enumerate(as_list(submission.get(field), f"handoff {handoff_id} submission {submission_id}.{field}", errors)):
                    validate_typed_reference(reference, indexes, artifacts, f"handoff {handoff_id} submission {submission_id}.{field}[{ref_index}]", errors)

        current_submission_id = handoff.get("current_submission_id")
        if current_submission_id is not None:
            if not is_non_empty(current_submission_id) or current_submission_id not in submission_index:
                add(errors, "REF038", f"Handoff {handoff_id}.current_submission_id does not resolve to one of its submissions")
            else:
                valid_submission_ids = [
                    item.get("submission_id") for item in submissions
                    if isinstance(item, dict) and is_non_empty(item.get("submission_id"))
                ]
                if valid_submission_ids and current_submission_id != valid_submission_ids[-1]:
                    add(errors, "REF039", f"Handoff {handoff_id}.current_submission_id must identify the latest submission")

        current_decision_id = handoff.get("current_decision_id")
        if current_decision_id:
            decision = resolve(current_decision_id, "decisions", indexes, f"handoff {handoff_id}.current_decision_id", errors)
            if decision and decision.get("decision_type") != "handoff_acceptance":
                add(errors, "REF040", f"Handoff {handoff_id}.current_decision_id must reference a handoff_acceptance decision")
            if submissions and is_non_empty(current_submission_id) and current_submission_id in submission_index:
                submission_decision = submission_index[current_submission_id].get("decision_id")
                if submission_decision and submission_decision != current_decision_id:
                    add(errors, "REF041", f"Handoff {handoff_id}.current_decision_id does not match the current submission decision")
            if decision:
                expected_outcome = handoff.get("current_status")
                if isinstance(expected_outcome, str) and expected_outcome in {"accepted", "partially_accepted", "rejected", "blocked"} and decision.get("decision_outcome") != expected_outcome:
                    add(errors, "REF057", f"Handoff {handoff_id}.current_status does not match current decision outcome")

        for dependency_id in as_list(handoff.get("dependency_ids"), f"handoff {handoff_id}.dependency_ids", errors):
            resolve(dependency_id, "dependencies", indexes, f"handoff {handoff_id}.dependency_ids", errors)


def validate_typed_reference(reference, indexes, artifacts, label, errors):
    if not isinstance(reference, dict):
        add(errors, "REF043", f"{label} must be a mapping")
        return
    ref_type = reference.get("reference_type")
    ref_id = reference.get("reference_id")
    if ref_type == "artifact":
        if not is_non_empty(ref_id) or ref_id not in artifacts:
            add(errors, "REF044", f"{label} references unknown artifact {ref_id}")
    elif ref_type == "work_item":
        resolve(ref_id, "work_items", indexes, label, errors)
    elif ref_type == "role_activation":
        resolve(ref_id, "role_activations", indexes, label, errors)
    elif ref_type == "dependency":
        resolve(ref_id, "dependencies", indexes, label, errors)
    elif ref_type == "handoff_execution":
        resolve(ref_id, "handoff_executions", indexes, label, errors)
    elif ref_type == "decision":
        resolve(ref_id, "decisions", indexes, label, errors)
    elif ref_type == "evidence":
        resolve(ref_id, "evidence", indexes, label, errors)
    elif ref_type == "blocker":
        resolve(ref_id, "blockers", indexes, label, errors)
    elif ref_type == "replan":
        resolve(ref_id, "replans", indexes, label, errors)
    elif ref_type == "external":
        # The external identifier is the canonical reference; a URI is supplementary.
        if not is_non_empty(ref_id):
            add(errors, "REF045", f"{label} external reference requires its external reference_id")
    else:
        add(errors, "REF046", f"{label}.reference_type is unsupported: {ref_type!r}")


def validate_common_record_references(indexes, artifacts, errors):
    for kind, records in indexes.items():
        for record_id, record in records.items():
            label = f"{kind} record {record_id}"
            for field, target_kind in CROSS_REFERENCE_FIELDS.items():
                if field not in record:
                    continue
                for index, ref in enumerate(as_list(record.get(field), f"{label}.{field}", errors)):
                    resolve(ref, target_kind, indexes, f"{label}.{field}[{index}]", errors)

            for field in ("related_record_refs", "affected_record_refs"):
                if field in record:
                    for index, ref in enumerate(as_list(record.get(field), f"{label}.{field}", errors)):
                        resolve_id_by_prefix(ref, indexes, artifacts, f"{label}.{field}[{index}]", errors)

            for field in ("artifact_id",):
                artifact_id = record.get(field)
                if artifact_id and artifact_id not in artifacts:
                    add(errors, "REF047", f"{label}.{field} references unknown artifact {artifact_id}")

            for field in ("dependency_ids",):
                if field in record:
                    for index, dependency_id in enumerate(as_list(record.get(field), f"{label}.{field}", errors)):
                        dependency = resolve(dependency_id, "dependencies", indexes, f"{label}.{field}[{index}]", errors)
                        if kind == "work_items" and dependency and record_id not in {
                            dependency.get("predecessor_work_item_id"),
                            dependency.get("successor_work_item_id"),
                        }:
                            add(errors, "REF056", f"{label}.{field}[{index}] references a dependency that does not involve this work item")

            if kind == "work_items":
                for field in ("input_refs", "output_refs"):
                    for index, reference in enumerate(as_list(record.get(field), f"{label}.{field}", errors)):
                        validate_typed_reference(reference, indexes, artifacts, f"{label}.{field}[{index}]", errors)

            if kind == "closure":
                for field in ("closure_checks", "exceptions"):
                    for nested_index, nested in enumerate(as_list(record.get(field), f"{label}.{field}", errors)):
                        if not isinstance(nested, dict):
                            continue
                        nested_label = f"{label}.{field}[{nested_index}]"
                        for ref_field in ("related_record_refs", "affected_record_refs"):
                            for ref_index, ref in enumerate(as_list(nested.get(ref_field), f"{nested_label}.{ref_field}", errors)):
                                resolve_id_by_prefix(ref, indexes, artifacts, f"{nested_label}.{ref_field}[{ref_index}]", errors)
                        for ref_field in ("evidence_refs",):
                            for ref_index, ref in enumerate(as_list(nested.get(ref_field), f"{nested_label}.{ref_field}", errors)):
                                resolve(ref, "evidence", indexes, f"{nested_label}.{ref_field}[{ref_index}]", errors)

            for field in ("supersedes_decision_id",):
                if record.get(field):
                    resolve(record[field], "decisions", indexes, f"{label}.{field}", errors)
            if record.get("supersedes_evidence_id"):
                resolve(record["supersedes_evidence_id"], "evidence", indexes, f"{label}.supersedes_evidence_id", errors)

    # Supersession chains must not contain cycles.
    for kind, field in (("decisions", "supersedes_decision_id"), ("evidence", "supersedes_evidence_id")):
        graph = {
            record_id: record.get(field)
            for record_id, record in indexes[kind].items()
            if is_non_empty(record.get(field))
        }
        for start in graph:
            seen = set()
            current = start
            while current in graph:
                if current in seen:
                    add(errors, "REF048", f"{kind} supersession relationship contains a cycle from {start}")
                    break
                seen.add(current)
                current = graph[current]


def validate_replans(indexes, artifacts, errors):
    for replan_id, replan in indexes["replans"].items():
        status = replan.get("status")
        decision_id = replan.get("decision_id")
        if isinstance(status, str) and status in {"approved", "in_progress", "completed"} and not decision_id:
            add(errors, "REF049", f"Replan {replan_id} in status {status!r} must reference its authorizing decision")
        if decision_id:
            decision = resolve(decision_id, "decisions", indexes, f"replan {replan_id}.decision_id", errors)
            if decision and isinstance(status, str) and status in {"approved", "in_progress", "completed"} and decision.get("decision_status") != "approved":
                add(errors, "REF049", f"Replan {replan_id} in status {status!r} must reference an approved decision")
        for index, artifact_id in enumerate(as_list(replan.get("affected_artifact_ids"), f"replan {replan_id}.affected_artifact_ids", errors)):
            if not is_non_empty(artifact_id) or artifact_id not in artifacts:
                add(errors, "REF050", f"Replan {replan_id}.affected_artifact_ids[{index}] references unknown artifact {artifact_id}")
        for index, change in enumerate(as_list(replan.get("changes"), f"replan {replan_id}.changes", errors, required=True)):
            if not isinstance(change, dict):
                continue
            target = change.get("target_record_ref")
            resolve_id_by_prefix(target, indexes, artifacts, f"replan {replan_id}.changes[{index}].target_record_ref", errors)


def validate_closure(indexes, artifacts, errors):
    closure = indexes.get("closure", {})
    if not closure:
        return
    closure_record = next(iter(closure.values()))
    closure_id = next(iter(closure))
    refs = closure_record.get("required_record_refs")
    if not isinstance(refs, dict):
        add(errors, "REF051", f"closure {closure_id}.required_record_refs must be a mapping")
        refs = {}

    fields = {
        "role_activation_ids": "role_activations",
        "work_item_ids": "work_items",
        "dependency_ids": "dependencies",
        "handoff_execution_ids": "handoff_executions",
        "decision_ids": "decisions",
        "evidence_ids": "evidence",
        "blocker_ids": "blockers",
        "replan_ids": "replans",
    }
    for field, kind in fields.items():
        seen = set()
        for index, ref in enumerate(as_list(refs.get(field), f"closure {closure_id}.required_record_refs.{field}", errors, required=True)):
            if is_non_empty(ref):
                if ref in seen:
                    add(errors, "REF058", f"closure {closure_id}.required_record_refs.{field} contains duplicate {ref}")
                seen.add(ref)
            resolve(ref, kind, indexes, f"closure {closure_id}.required_record_refs.{field}[{index}]", errors)
    # Release references are intentionally external to the ten canonical YAML record types.
    as_list(refs.get("release_record_refs"), f"closure {closure_id}.required_record_refs.release_record_refs", errors, required=True)

    decision_id = closure_record.get("closure_decision_id")
    if decision_id:
        decision = resolve(decision_id, "decisions", indexes, f"closure {closure_id}.closure_decision_id", errors)
        if decision:
            if decision.get("decision_type") != "execution_closure":
                add(errors, "REF052", f"Closure decision {decision_id} must have decision_type 'execution_closure'")
            if closure_record.get("closure_status") == "closed" and decision.get("decision_status") != "approved":
                add(errors, "REF053", f"Closed execution requires approved closure decision {decision_id}")

    completion = closure_record.get("completion", {})
    verification = closure_record.get("verification", {})
    if not isinstance(completion, dict):
        add(errors, "REF064", f"closure {closure_id}.completion must be a mapping")
        completion = {}
    if not isinstance(verification, dict):
        add(errors, "REF065", f"closure {closure_id}.verification must be a mapping")
        verification = {}
    completion_lists = {
        field: string_set(completion.get(field), f"closure {closure_id}.completion.{field}", errors)
        for field in ("completed_work_item_ids", "cancelled_work_item_ids", "outstanding_work_item_ids")
    }
    verification_lists = {
        field: string_set(verification.get(field), f"closure {closure_id}.verification.{field}", errors)
        for field in ("verified_work_item_ids", "failed_work_item_ids", "not_verified_work_item_ids")
    }
    for label, groups in (("completion", completion_lists), ("verification", verification_lists)):
        seen_ids = set()
        for group_name, group_ids in groups.items():
            overlap = seen_ids.intersection(group_ids)
            for overlap_id in sorted(overlap):
                add(errors, "REF061", f"Closure {closure_id} work item {overlap_id} appears in multiple {label} classifications")
            seen_ids.update(group_ids)
    in_scope_work_items = string_set(refs.get("work_item_ids"), f"closure {closure_id}.required_record_refs.work_item_ids", errors)
    accounted_work_items = set().union(*completion_lists.values())
    missing_completion_items = in_scope_work_items - accounted_work_items
    for work_item_id in sorted(missing_completion_items):
        add(errors, "REF070", f"In-scope work item {work_item_id} is not accounted for in the closure completion lists")

    for group_name, group_ids in completion_lists.items():
        for work_item_id in group_ids:
            item = resolve(work_item_id, "work_items", indexes, f"closure {closure_id}.{group_name}", errors)
            if item:
                expected_state = {
                    "completed_work_item_ids": "completed",
                    "cancelled_work_item_ids": "cancelled",
                }.get(group_name)
                if expected_state and item.get("state") != expected_state:
                    add(errors, "REF062", f"Closure {closure_id}.{group_name} includes {work_item_id} whose state is {item.get('state')!r}, expected {expected_state!r}")
                if group_name == "outstanding_work_item_ids" and item.get("state") in {"completed", "cancelled"}:
                    add(errors, "REF063", f"Closure {closure_id}.outstanding_work_item_ids includes terminal work item {work_item_id}")
                if group_name == "outstanding_work_item_ids" and item.get("state") not in {"not_started", "ready", "in_progress", "blocked", "in_review", "changes_requested"}:
                    add(errors, "REF071", f"Closure {closure_id}.outstanding_work_item_ids contains {work_item_id} with an unsupported non-terminal state")

    if completion.get("status") == "complete" and completion_lists["outstanding_work_item_ids"]:
        add(errors, "REF072", f"Closure {closure_id} cannot claim completion status 'complete' while outstanding work items remain")
    for work_item_id in verification_lists["verified_work_item_ids"] | verification_lists["failed_work_item_ids"] | verification_lists["not_verified_work_item_ids"]:
        resolve(work_item_id, "work_items", indexes, f"closure {closure_id}.verification work-item classification", errors)
    for section, field, kind in (
        (completion, "completed_work_item_ids", "work_items"),
        (completion, "cancelled_work_item_ids", "work_items"),
        (completion, "outstanding_work_item_ids", "work_items"),
        (verification, "verified_work_item_ids", "work_items"),
        (verification, "failed_work_item_ids", "work_items"),
        (verification, "not_verified_work_item_ids", "work_items"),
        (verification, "evidence_refs", "evidence"),
    ):
        for index, ref in enumerate(as_list(section.get(field), f"closure {closure_id}.{field}", errors, required=True)):
            resolve(ref, kind, indexes, f"closure {closure_id}.{field}[{index}]", errors)

    for index, ref in enumerate(as_list(completion.get("completion_evidence_refs"), f"closure {closure_id}.completion.completion_evidence_refs", errors)):
        resolve(ref, "evidence", indexes, f"closure {closure_id}.completion.completion_evidence_refs[{index}]", errors)

    for classification, ids in {**completion_lists, **verification_lists}.items():
        for work_item_id in ids:
            if work_item_id not in in_scope_work_items:
                add(errors, "REF069", f"Closure {closure_id}.{classification} includes {work_item_id}, which is absent from required_record_refs.work_item_ids")

    exceptions = as_list(closure_record.get("exceptions"), f"closure {closure_id}.exceptions", errors, required=True)
    approved_exceptions = 0
    for exception_index, exception in enumerate(exceptions):
        if not isinstance(exception, dict):
            continue
        decision_ref = exception.get("accepted_by_decision_id")
        if decision_ref:
            decision = resolve(decision_ref, "decisions", indexes, f"closure exception[{exception_index}].accepted_by_decision_id", errors)
            if decision and decision.get("decision_status") != "approved":
                add(errors, "REF054", f"Closure exception {exception.get('exception_id')} must reference an approved decision")
        if exception.get("status") == "approved" and decision_ref:
            approved_exceptions += 1

    if completion.get("status") == "complete_with_exceptions" and approved_exceptions == 0:
        add(errors, "REF073", f"Closure {closure_id} claims complete_with_exceptions without an approved exception")
    if verification.get("status") == "passed" and (
        verification_lists["failed_work_item_ids"] or verification_lists["not_verified_work_item_ids"]
    ):
        add(errors, "REF074", f"Closure {closure_id} cannot claim verification status 'passed' while failed or not-verified work items remain")
    if verification.get("status") == "passed_with_exceptions" and approved_exceptions == 0:
        add(errors, "REF075", f"Closure {closure_id} claims passed_with_exceptions without an approved exception")


def validate_execution(directory):
    errors, warnings = [], []
    roles = set(expected_roles())

    records = {}
    for kind, (filename, wrapper, collection, _) in RECORD_FILES.items():
        payload = load_execution_document(directory / filename, wrapper, collection, errors)
        if payload is not None:
            records[kind] = payload

    if len(records) != len(RECORD_FILES):
        return report(errors, warnings, "Execution reference validation")

    execution = records["execution"]
    execution_id = validate_execution_identity(execution, directory, records, errors)

    indexes = {}
    for kind, (_, _, collection, id_field) in RECORD_FILES.items():
        payload = records[kind]
        entries = payload if collection else [payload]
        indexes[kind] = index_records(kind, entries, id_field, errors)

    try:
        ownership = load_yaml(ROOT / "docs/team/ownership.yml")
        artifacts = {
            item.get("id"): item
            for item in ownership.get("artifacts", [])
            if isinstance(item, dict) and is_non_empty(item.get("id"))
        }
        contracts = {
            item.get("id"): item
            for item in ownership.get("handoffs", [])
            if isinstance(item, dict) and is_non_empty(item.get("id"))
        }
    except (ValueError, AttributeError) as exc:
        add(errors, "REF055", f"Could not load artifact and handoff registries: {exc}")
        artifacts, contracts = {}, {}

    for kind, payload in records.items():
        validate_role_fields(payload, roles, kind, errors)

    validate_root_index(execution, indexes, errors)
    validate_activation_work_items(indexes, errors)
    validate_dependency_graph(indexes, errors)
    validate_handoffs(indexes, artifacts, contracts, errors, warnings)
    validate_common_record_references(indexes, artifacts, errors)
    validate_replans(indexes, artifacts, errors)
    validate_closure(indexes, artifacts, errors)

    if execution_id:
        print(f"Execution: {execution_id}")
    return report(errors, warnings, "Execution reference validation")


def main():
    parser = argparse.ArgumentParser(
        description="Validate cross-record references for one execution directory."
    )
    parser.add_argument(
        "execution_directory",
        help="Repository-relative path such as executions/EXE-<UUID>",
    )
    args = parser.parse_args()

    candidate = (ROOT / args.execution_directory).resolve()
    executions_root = (ROOT / "executions").resolve()
    try:
        candidate.relative_to(executions_root)
    except ValueError:
        print("ERROR: Execution directory must be inside the repository executions/ directory.")
        return 2

    if candidate.parent != executions_root:
        print("ERROR: Execution directory must be a direct child of executions/.")
        return 2

    if not candidate.is_dir():
        print(f"ERROR: Execution directory does not exist: {args.execution_directory}")
        return 2

    try:
        return validate_execution(candidate)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
