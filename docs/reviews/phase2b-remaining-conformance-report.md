# Phase 2B — Remaining Governance Conformance Scenarios

## Status

**Reference-probe implementation:** Added on this branch.  
**Repository-local execution:** Passed on the user's checked-out branch.  
**Production-agent enforcement:** Not verified; the repository contains governance documents and schemas, not a live orchestration engine.

This report deliberately separates executable reference-model results from claims about production agent behavior. No live Copilot, Claude Code, Codex, or other agent run is claimed.

## Scope and source rules

The probe in `proof-pair-lab/governance/` covers the remaining four proof areas from
`docs/reviews/proof-pair-report.md`:

- Conditional dependency activation.
- Feedback-only relationships and closure behavior.
- Three materially different unsuccessful correction attempts.
- Immediate escalation for critical and urgent risk conditions.

The reference model is derived from:

- `docs/team/dependency-execution-rules.md`
- `docs/team/dependency-execution-records.md`
- `docs/team/execution-protocol.md`
- `docs/team/blockers-replanning-and-state-transitions.md`
- `docs/team/handoff-escalation-rules.md`

## Scenario coverage

| Proof area | Probe cases | Expected decision |
|---|---|---|
| Conditional dependency inactive | Activation condition false | `not_applicable`; successor is not blocked by this dependency |
| Conditional dependency active | Activation true, prerequisite unresolved | `active`; dependent gate is blocked |
| Conditional dependency satisfied | Activation true, prerequisite satisfied | `satisfied`; this dependency no longer blocks |
| Conditional activation unknown | No activation decision supplied | Reject incomplete decision; do not guess |
| Feedback only | No task acceptance criterion makes feedback mandatory | Feedback alone does not block |
| Required feedback criterion | Task acceptance criterion explicitly requires feedback and it is unresolved | Track as an explicit blocking acceptance condition |
| Required feedback satisfied | Explicit criterion is satisfied | Does not block |
| Repeated same correction approach | Same unsuccessful approach submitted multiple times | Count once; no three-attempt escalation |
| Three distinct unsuccessful approaches | Three different unsuccessful approaches to one unresolved increment | Escalate |
| Successful attempt | One approach succeeds | Does not count as an unsuccessful correction |
| Separate increments | Attempts belong to different unresolved increments | Count independently |
| Critical severity | Critical blocker | Immediate escalation |
| Urgent risk triggers | Security, privacy, safety, data integrity, production stability, permission, or authorization | Immediate escalation |
| Ordinary blocker | Medium severity with no urgent risk trigger | No automatic immediate escalation |

## Interpretation and limitations

1. The probe evaluates dependency decisions; it does not persist canonical
   `dependencies.yml`, `work-items.yml`, or `blockers.yml` records.
2. A feedback finding that reveals a safety, security, correctness, or required
   acceptance issue must be assessed under the applicable blocker and escalation
   rules. The feedback relationship itself is not automatically a prerequisite.
3. Correction attempts are supplied as approach keys. The probe can prove that
   repeated keys count once and three distinct unsuccessful keys trigger the
   threshold. It cannot independently judge whether two real engineering
   approaches are materially different. That requires reviewer judgment and
   evidence in the actual correction record.
4. Immediate escalation is tested as a decision. It does not claim the
   escalation notification, authority routing, stop-work action, or record
   persistence occurred in a live system.
5. No formal handoff contracts are declared in
   `docs/team/ownership.yml`; formal handoff submission and consumer acceptance
   remain untested.

## Governance inconsistency discovered

Historical finding (resolved in PR #10): the blocker lifecycle vocabulary was
inconsistent across canonical materials at the time this report was written.
The current canonical records, lifecycle guidance, and JSON Schema now share
the same eight statuses. This report preserves the original discovery and
probe limitation as historical evidence; it is not a statement of the current
canonical status vocabulary.

- PR #10, merged as `41f29d4ad5f6452024279e99c6697af0c65c3a4b`, aligned
  `docs/team/blocker-records.md`, lifecycle guidance, and
  `schemas/executions/blockers.schema.json`.
- The current shared status set is `open`, `in_progress`, `blocked`,
  `escalated`, `deferred`, `resolved`, `closed`, and `cancelled`.

The historical reference probe did not persist an `escalated` status. The
canonical vocabulary is now aligned, but live status persistence, escalation
notification/routing, stop-work enforcement, and authority routing remain
unverified.

## Local validation instructions

From `proof-pair-lab/`:

```powershell
python -m unittest discover -s governance -p "test_*.py" -v
```

The user ran the command from `proof-pair-lab/` and reported:

- Governance conformance scenarios: **15 passed**.
- Backend proof-lab tests: **12 passed**.
- Independent QA proof-lab tests: **10 passed**.
- Total: **37 passed, 0 failures, 0 errors**.
- `git diff --check` was included in the command sequence and produced no reported diagnostics.

The Python version was not included in the supplied output and is therefore
not recorded here.

## Acceptance assessment

The reference model covers the logical outcomes for the four outstanding
scenarios. The Phase 2B gate should not be marked fully accepted until:

- The local reference-model test execution is complete: 37 tests passed across
  governance, Backend, and QA suites.
- The blocker status vocabulary has been aligned by PR #10; live persistence
  and escalation routing still require separate evidence.
- Any desired live-agent behavior is tested separately with traceable prompts,
  outputs, and execution records.
- Formal handoff behavior remains deferred until an approved formal handoff
  contract exists.
