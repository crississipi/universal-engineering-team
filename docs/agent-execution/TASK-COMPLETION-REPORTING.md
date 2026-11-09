# Task completion reporting and role-skill orchestration

## Purpose

The engineering agent produces one canonical completion report for every
top-level user task or prompt that reaches a terminal outcome. Reporting is
completion-triggered, not daily, scheduled, or dependent on a timezone/day
boundary.

This contract defines orchestration behavior and report evidence. It does not
by itself provide a running autonomous agent, grant tool permissions, approve
baseline scenarios, or authorize production actions.

## Required lifecycle

1. **Create an execution identity.** Assign one stable execution ID to the
   top-level task. Record the original prompt or a safe prompt reference,
   objective, and start timestamp. Do not copy secrets or unnecessary personal
   data into the record.
2. **Analyze scope and select roles.** The orchestrator independently selects
   only the canonical roles whose responsibilities are materially required by
   the task. Consult `docs/team/expected-roles.yml`,
   `docs/team/ownership.yml`, applicable governance, and role skill files.
   Role names alone do not establish artifact ownership or a formal handoff.
3. **Load skills before role work.** For every activated role, read the current
   canonical `skills/<role>/SKILL.md` before delegating or performing that
   role's work. Follow its responsibilities, boundaries, required outputs, and
   verification expectations. Record the exact skill path and revision or
   content hash when available. Never claim a skill was used if it was only
   considered or listed.
4. **Assign ownership and coordinate.** Identify one accountable owner for
   each work item. Use only declared handoff contracts. If no formal handoff
   exists, treat collaboration as coordination, not accepted ownership.
   Activate QA, security, accessibility, performance, release, or other
   specialist review when the task's risk and scope warrant it; do not
   automatically activate all roles.
5. **Execute within authority.** Respect user authorization, tool permissions,
   environment restrictions, and role boundaries. Record changes and outputs.
   A plan is not an implementation; a proposed test is not an executed test.
6. **Verify proportionately.** Record each verification check as passed,
   failed, blocked, or not run, with its command/result/evidence reference
   where available. Do not claim tests, reviews, deployments, approvals, or
   external actions that did not happen.
7. **Close the execution.** Assign exactly one terminal status:
   - `completed`: requested work is complete and no known material warning
     remains.
   - `completed_with_warnings`: useful work is complete but limitations,
     warnings, or unverified items remain.
   - `blocked`: work cannot safely or correctly continue without an external
     decision, permission, dependency, or missing input.
   - `failed`: the task was attempted but did not achieve its requested
     outcome.
8. **Emit one canonical report.** Generate a report for every terminal
   execution, including blocked and failed tasks. For multi-role work, emit one
   consolidated top-level report containing each participating role's
   contribution. Role-level subtask records may be linked as evidence but do
   not replace the top-level report.
9. **Persist and expose the result.** Store the structured JSON report and
   human-readable Markdown report under
   `reports/task-completions/<execution_id>/`. Keep execution records
   append-only or versioned; corrections must be traceable rather than
   silently overwriting history.

## Role-selection policy

The orchestrator makes the selection; the user does not need to name roles.

- Match the task's requested outcome, affected artifacts, technical domains,
  risks, and required verification to canonical role responsibilities.
- Read the candidate role skills to confirm fit before activation.
- Select the smallest sufficient set of roles. Add a specialist when a
  material concern falls within that specialist's remit.
- The Delivery Lead may coordinate work, but does not take ownership of
  specialist artifacts merely by coordinating them.
- QA independently evaluates evidence; implementation roles remain
  responsible for correcting their own defects.
- If role relevance is ambiguous, record the ambiguity and choose a bounded
  path or ask one necessary clarification. Do not silently invent ownership.
- Record considered-but-not-activated roles only when that decision materially
  affects scope or risk; the report's required role list is for roles actually
  activated and whose skills were loaded.

## Report contract

Every report records:

- execution ID, task objective/reference, start and completion timestamps;
- terminal status and concise outcome;
- activated canonical role IDs, skill paths/revisions, and contributions;
- deliverables with repository-relative paths and change descriptions;
- verification checks and their actual outcomes;
- decisions, blockers, warnings, and unverified claims;
- next steps, when work remains.

Timestamps are audit metadata only. They do not define a reporting period,
daily roll-up, timezone, or trigger. Store offset-aware timestamps (UTC is
recommended for machine consistency) without requiring a business timezone.

## Ingress/security logging for webhook adapters

This is a separate concern from agent task-completion reports. An adapter
handling untrusted webhook requests should write invalid-signature and
unparseable-payload events to a restricted security/ingress log, not to the
business-event summary.

Allowed fields are generated request ID, receiver timestamp, trusted source
identifier (if known independently of the payload), failure category, safe
reason code, signature status, payload byte length, and safe correlation ID.
Do not record raw bodies, secrets, authorization headers, complete signature
values, or identifiers extracted from an unauthenticated payload. Do not expose
these records in ordinary support-facing business reports.

The provided logger writes JSON Lines and deliberately does not set a
retention duration. Security/Operations must approve retention, access,
rotation, and deletion policy for the deployment environment. Protect the
destination directory and log file with least-privilege access and monitor
write failures; a logger that cannot persist an event must surface that failure
to its caller.

## Event identity policy for the webhook exercise

- Repeated deliveries with the same trusted `event_id` are delivery attempts
  for one provider event. Apply event-level idempotency so the business effect
  is not repeated.
- Different trusted `event_id` values are distinct provider events, even if
  they contain the same `order_id`. They are not duplicate deliveries.
- A second `order.created` event for an existing order must be recorded and
  passed through an explicit domain uniqueness/conflict rule. Do not silently
  discard it or repeat a create-side effect.
- Preserve separate attempt, event, and order identities. The exact business
  response to conflicting distinct events must be defined by Product and
  implemented by Backend/API with QA coverage. The policy above establishes
  identity semantics, not a complete order lifecycle policy.

## Completion guarantees and limitations

The report generator validates and renders a supplied execution record; it
does not observe an agent runtime, discover skills automatically, prove that
a provider actually loaded a skill, authenticate approvals, or establish that
a test result is truthful. The orchestrator must collect evidence from the
runtime and submit accurate values. The validator can check structural
consistency, not the truth of claims.

No baseline execution is authorized by this contract. Existing scenario
approval, cohort, stakeholder, and human pre-run gates remain independent.
