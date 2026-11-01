# Graphify maintenance contract

Graphify installations and plugins can use different schemas. **Inspect the repository and installed Graphify instructions first.** Follow the existing native format and commands; do not invent a plugin command or overwrite its graph.

## Portable fallback (when no native Graphify format exists)
Maintain:
- `docs/knowledge/graph/nodes.jsonl` — one JSON object per line: `{"id":"stable-kebab-id","type":"service|module|api|database|event|person-role|decision|document|test|deployment","label":"Human name","path":"repo/relative/path","summary":"Verified one-line purpose","status":"active|planned|deprecated","verified":"YYYY-MM-DD"}`
- `docs/knowledge/graph/edges.csv` — header `source,target,relation,evidence`; relation examples: `calls`, `publishes`, `consumes`, `persists_to`, `authenticates_with`, `owned_by`, `tested_by`, `documented_by`, `deployed_to`, `depends_on`.
- `docs/knowledge/graph/system-map.mmd` — Mermaid view of important relationships.

## Update rules
1. Stable IDs; update existing nodes instead of duplicating them.
2. Every edge must have evidence: source path, contract, test, or ADR.
3. Remove/mark stale relationships when code changes; never leave a known false edge.
4. Keep graph scope useful: components, interfaces, data stores, events, decisions, tests, docs, deployments. Do not graph every function by default.
5. Link graph entities to Obsidian notes and report sections where practical.
6. Graphify is a relationship index, not the canonical specification. Code/contracts/ADRs remain authoritative.
7. Validate JSONL/CSV syntax and ensure every edge endpoint exists.
