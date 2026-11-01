# Central engineering report specification

The report is `docs/report/index.html`. Its navigation and presentation should follow the supplied `index.html`: searchable left sidebar; grouped navigation; overview hero; collapsible file/module sections; architecture diagrams; code blocks; function cards; tables; clear callouts; progress/section navigation; responsive layout; dark developer code blocks.

## Required information architecture
1. Overview — system purpose, status, stack, critical concepts, project map.
2. Architecture — context/container/component, key user/system flows, sequence diagrams, state machines, ERD, deployment.
3. Product and domain — use cases, domain terms, business rules, acceptance criteria.
4. Services and modules — purpose, source path, responsibilities, dependencies/imports, public interfaces, key functions, data transformations, errors/failure behavior, tests, related notes.
5. APIs and integrations — contracts, consumers/producers, auth, mapping, rate limits, retries, idempotency, failure/reconciliation.
6. Data — ERD, ownership, migrations, constraints, retention, backup/restore.
7. Security — trust boundaries, authz/authn, threat model, findings and mitigations (sanitized).
8. Quality — test strategy, coverage evidence, test commands/results, known gaps.
9. Operations — local setup, configuration names (never secret values), deployment, monitoring, runbooks, recovery.
10. Decisions and changes — ADRs, dated changes, owner, affected surfaces, impact, verification, open risks.
11. Glossary and Q&A — explain important concepts plainly; add project-specific Q&A only when useful.

## Per-section template
- **Purpose:** what this part does and why it exists.
- **Location:** verified source paths.
- **Inputs/outputs:** contracts and data.
- **Dependencies:** upstream/downstream systems.
- **Behavior:** normal and alternate/failure paths.
- **Security/reliability:** relevant controls.
- **Tests:** actual test files/commands/results.
- **Related:** Obsidian links, Graphify IDs, ADRs.
- **Verified:** date and evidence source.
- **Unknowns:** explicit unresolved questions.

## Efficient update policy
Prefer structured source fragments under `docs/report/data/` (JSON/YAML/Markdown) and a generated HTML view if a generator exists. If the report is maintained directly, patch only affected section and navigation entries. Preserve existing CSS, JS, Mermaid version, IDs, and user styling. Do not regenerate the entire HTML from scratch for a small change.

## Quality gate
Check all nav targets exist; search works; Mermaid diagrams render; code blocks are readable; no secret values/PII; dates and source paths are accurate; mobile layout works; no broken links. Report generated timestamp and last-verified dates.
