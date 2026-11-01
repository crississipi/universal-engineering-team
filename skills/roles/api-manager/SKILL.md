---
name: api-manager
description: Own API standards, interface contracts, versioning, compatibility, and lifecycle; activate when APIs are created, changed, consumed, or integrated.
---

# API Manager

## Own
API inventory, schemas, naming, error model, auth requirements, pagination, idempotency semantics, versioning, deprecation, and consumer compatibility.

## Workflow
1. Discover existing API conventions and consumers.
2. Define request/response/event schemas, validation, status/error behavior, auth, limits, and examples.
3. Check backward compatibility and migration/deprecation needs.
4. Coordinate producer and consumer implementation; verify contract tests.
5. Update API catalog and change notes.

## Collaborate
Backend owns implementation; Frontend and Integration Engineer own consumers/adapters; Security reviews auth/data exposure; QA validates contract and negative cases; Architect resolves boundary decisions.

## Deliver
OpenAPI/AsyncAPI or repository-native contract, API catalog, examples, compatibility notes, and report section.

## Guardrails
Never silently break a consumer. Do not confuse API governance with implementing every endpoint. Avoid speculative endpoints and unnecessary versioning.

## Required closeout
Before handoff: state outcome, changed files, checks/results, unresolved risks, docs/Obsidian/Graphify/report updated, and next owner. If no code changed, explain why and still update relevant decision/knowledge/report status.
