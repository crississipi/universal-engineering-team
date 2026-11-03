---
name: <canonical-role-id>
description: <concise role capability description within repository policy>
---

# <Role Name>

## 1. Identity and boundaries

State the role's purpose, accountable domain, decision authority, and explicit non-ownership boundaries. Refer to canonical ownership and responsibility documents; do not redefine them.

## 2. Activation

Describe when this role is required, conditional, optional, or not activated. Reference `docs/team/role-activation-rules.md`; state concrete triggers without requiring every role on every task.

## 3. Input contract

List the minimum inputs needed to begin, their authoritative sources, how to handle missing or conflicting inputs, and which work can proceed safely while inputs are pending.

## 4. Execution contract

Describe the role-specific workflow, methods, quality bar, and domain guardrails. Keep instructions specific to this role. Shared workflow and verification rules belong in `docs/team/execution-protocol.md`.

## 5. Collaboration contract

Reference the role's structured declarations in `skills/manifest.yml`. Explain how to use required, conditional, and feedback relationships without converting every relationship into a blocking dependency or formal handoff.

## 6. Output and handoff contract

List concrete role-owned outputs and the evidence/context needed to consume them. Formal handoffs must reference an approved contract in `docs/team/ownership.yml`; do not create a contract by implication.

## 7. Accountability and closeout

State what this role must verify, which decisions it owns, what it must escalate, and the closeout information it must provide. Report actual checks and results; never claim unperformed verification or approval.
