---
type: change
status: active
owner: Delivery Lead
source:
  - docs/agent-execution/TASK-COMPLETION-REPORTING.md
  - schemas/executions/task-completion-report.schema.json
  - scripts/report-task-completion.py
  - scripts/log-ingress-security-event.py
last_verified: 2026-11-09
tags: [agent-orchestration, role-skills, reporting, security-logging]
---
# Task Completion Reporting

Every top-level task produces one consolidated report when it reaches a terminal outcome. Reporting is event-triggered, not daily or timezone-bound.

## Flow

1. Create an execution identity.
2. Select the smallest sufficient canonical role set.
3. Read each activated role's canonical `SKILL.md`.
4. Execute and coordinate work within ownership and authorization boundaries.
5. Record actual verification evidence.
6. Produce a report for completed, completed-with-warnings, blocked, or failed outcomes.

## Canonical sources

- Canonical orchestration/reporting contract: `docs/agent-execution/TASK-COMPLETION-REPORTING.md`.
- [[../report/index.html|Central Engineering Report]] — navigable system handbook.
- `schemas/executions/task-completion-report.schema.json` — structured report schema.
- `scripts/report-task-completion.py` — report validator and renderer.
- `scripts/log-ingress-security-event.py` — separate sanitized webhook ingress logger.

## Limitations

The report generator validates supplied records. It does not independently observe a provider runtime or prove that a skill was actually loaded. The orchestrator must provide truthful execution evidence. Webhook security-log retention and access controls remain deployment-specific decisions.
