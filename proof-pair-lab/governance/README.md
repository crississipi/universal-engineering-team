# Governance Conformance Probe

This directory contains a small, dependency-free reference model for selected
rules in the Universal Engineering Team execution protocol.

It exercises four proof areas:

1. Conditional inputs block only when their activation condition applies and
   the required input remains unresolved.
2. Feedback does not block by default. It can become a blocking acceptance
   condition only when the task's acceptance criteria explicitly require it.
3. Correction attempts count distinct unsuccessful approaches against one
   unresolved increment; repeating the same approach does not increase the
   count. Three distinct unsuccessful approaches trigger escalation.
4. Critical blockers and urgent security, privacy, safety, data-integrity,
   production-stability, permission, or authorization triggers require
   immediate escalation.

## Run

From the `proof-pair-lab/` directory:

```powershell
python -m unittest discover -s governance -p "test_*.py" -v
```

## Important scope boundary

These tests validate the reference decision model in
`governance/protocol_probe.py` against documented rules. They do not execute
Copilot, Claude Code, Codex, a production orchestrator, or canonical
execution-record persistence. They do not prove that a live agent correctly
classifies a real-world change as materially different; the caller supplies
an approach key for each correction attempt. They are conformance examples,
not an enforcement engine or formal handoff acceptance.

The current repository declares no formal handoff contracts in
`docs/team/ownership.yml`. Formal handoff submission and acceptance therefore
remain outside this probe.

The current blocker governance also has a status-vocabulary inconsistency:
`blockers-replanning-and-state-transitions.md` describes `escalated` and
`closed`, while `blocker-records.md` and `schemas/executions/blockers.schema.json`
use a different status set. The immediate-escalation probe tests the decision
to escalate, not persistence of an escalation status. Do not treat that
persistence behavior as verified until the canonical vocabulary is reconciled.
