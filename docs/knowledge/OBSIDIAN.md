# Obsidian vault contract

Use the existing vault location if present. Do not create a second vault without approval. If none exists, keep project notes under `docs/obsidian/` so they can be opened as a vault.

## Suggested structure
- `00 Home/Project MOC.md`
- `01 Architecture/System Overview.md`
- `01 Architecture/Services/<service>.md`
- `02 Flows/<flow>.md`
- `03 Data/<entity-or-store>.md`
- `04 APIs/<api-or-event>.md`
- `05 Decisions/ADR-<id>-<title>.md`
- `06 Operations/<runbook>.md`
- `07 Quality/<test-strategy-or-risk>.md`
- `08 Changes/<date>-<task-id>.md`

## Note format
Use frontmatter:
```yaml
---
type: architecture | service | flow | data | api | decision | runbook | test | change
status: active
owner: role-or-team
source:
  - path/to/source
last_verified: YYYY-MM-DD
tags: [system, relevant-domain]
---
```
Keep each note focused. Add `[[wikilinks]]` to related services, flows, APIs, data, ADRs, tests, and Graphify map. The Home MOC links all active notes. Use stable note names; rename only when meaning changes.

## Collaboration rules
- Update existing notes in place; do not create duplicates for the same concept.
- Put decisions in ADR notes, not buried in chat or report prose.
- Mark stale notes as deprecated and link replacements.
- Avoid copying long code blocks; link to source paths and explain behavior.
- Every change note links to its report section, graph entities, tests, and decisions.
