# Universal Engineering Team — Agent Skills

A portable, stack-agnostic engineering team for coding agents. The package contains **16 specialist roles plus 1 Delivery Lead coordination role (17 roles total)**, a shared engineering constitution, role ownership guidance, task routing, validation scripts, and mandatory documentation practices.

## Included roles

Product Analyst; Solution Architect; API Manager; Backend Developer; Frontend Developer; UX/UI Designer; Database Manager; Integration Engineer; Data Engineer; QA Manager; Penetration Tester / AppSec; DevOps / SRE; Performance Engineer; Accessibility Specialist; Technical Writer / Knowledge Engineer; Release Manager; Delivery Lead.

## Package layout

```text
.
├── AGENTS.md
├── ROLE-INDEX.md
├── SKILLS-RESOLVER.md
├── ALL-ROLE-SKILLS.md
├── skills/
│   └── <role>/SKILL.md
├── docs/
│   ├── team/
│   ├── knowledge/
│   ├── obsidian/
│   └── report/
├── scripts/
└── .github/workflows/
```

## Team governance

Start with `docs/team/workflow.md` for the team's workflow and governance navigation.

Key references:

- `docs/team/ownership.md` — artifact ownership and responsibility boundaries.
- `docs/team/artifact-catalog.md` — the 17 accountable artifact packages.
- `docs/team/producer-consumer-matrix.md` — package-level dependencies.
- `docs/team/workflow-lifecycle.md` — workflow stages and overall workflow statuses.
- `docs/team/blockers-replanning-and-state-transitions.md` — blocker and work-item execution rules.

## Skill evaluation

- `docs/team/evaluation-methodology.md` — pilot, baseline, and regression evaluation methodology.
- `docs/evaluation/pilot/README.md` — completed pilot execution and review record.
- `docs/evaluation/baseline/README.md` — repository-wide 17-role baseline plan, coverage register, readiness gates, and evidence protocol.

The pilot is complete (9/9 executions; 3/3 scenario reviews recorded). The
repository-wide baseline is a separate planned cohort of 170 executions and
has not started. Do not count pilot runs toward baseline totals.

## How agents should use the library

1. Read the project's applicable instruction file and inspect the repository before proposing changes.
2. Use `SKILLS-RESOLVER.md` to identify likely roles; confirm each role against the task and ownership boundaries.
3. Read only the selected role `SKILL.md` files. Each has standard Agent Skills `name` and `description` metadata plus its full role-specific instructions.
4. For cross-role work, appoint one coordinating lead, assign one owner per file/decision, define interfaces, and use concise evidence-based handoffs.
5. Verify the implementation and report actual commands/results. Never claim an unrun check passed.
6. Update applicable source documentation, Obsidian notes, Graphify relationships, and the central HTML report. Documentation is a completion requirement, not an optional follow-up.

Do not load every role for every task. The resolver's examples are guidance, not hard-coded workflow restrictions.

## Installation

The skill format is portable, but discovery paths and project-instruction behavior vary by provider and version. Use the provider's current documentation to identify its supported global or project-level skill directory.

- Copy the **entire** `skills/<role>/` folder into the provider's discovered skills directory, preserving the `SKILL.md` filename.
- Copy or adapt `AGENTS.md` into the project's supported instruction mechanism. Do not assume every provider automatically reads `AGENTS.md`.
- Keep `ROLE-INDEX.md` and `SKILLS-RESOLVER.md` available as routing references. If a provider does not automatically load them, the coordinating agent should consult them when selecting roles.
- Maintain one canonical repository and synchronize provider-specific copies from it. Global local installation does not automatically sync to cloud agents or other machines.

### Windows PowerShell example

Replace the destination with the actual skills directory documented by your agent provider:

```powershell
$source = Join-Path (Get-Location) "skills"
$destination = Join-Path $HOME ".copilot\skills"

New-Item -ItemType Directory -Force -Path $destination | Out-Null
Copy-Item -Path (Join-Path $source "*") -Destination $destination -Recurse -Force
```

This example is illustrative; it does not assert that `.copilot\skills` is the correct directory for every VS Code/GitHub Copilot version or every agent provider.

## Validation

Install development dependencies from the repository root:

```powershell
python -m pip install -r requirements-dev.txt
```

PowerShell wrapper:

```powershell
./scripts/validate-skills.ps1
```

The validator checks skill frontmatter, duplicate names, role-index targets, and local Markdown links. Token counts are estimates unless the optional `tiktoken` package is installed; they are monitoring data, not a quality score. A shorter skill is not automatically a better skill.

GitHub Actions runs the same validation on pushes and pull requests.

## Graphify and Obsidian

- Follow `docs/knowledge/GRAPHIFY.md`; inspect the installed Graphify version and use its native conventions when available.
- Follow `docs/knowledge/OBSIDIAN.md`; reuse the project's existing vault and stable note links.
- Portable graph artifacts are under `docs/knowledge/graph/`. Treat them as a fallback, not as a claim that every Graphify installation uses the same schema.
- Starter Obsidian notes are under `docs/obsidian/`; merge with existing project knowledge rather than overwriting it.

## Central HTML report

`docs/report/REPORT_SPEC.md` defines the report. Create or update `docs/report/index.html` as a searchable, navigable system handbook. Include verified architecture, flows, module/file responsibilities, key functions/contracts, operations, quality evidence, decisions, and change history. Patch affected sections; do not overwrite a populated report or invent undocumented behavior.

## Safety and quality principles

- One accountable owner per deliverable or decision at a time.
- Specialist skills define responsibility, not permission to exceed scope.
- Do not perform destructive production actions, expose secrets, or conduct intrusive security testing without explicit authorization.
- Prefer the smallest safe change; preserve existing project conventions.
- When blocked, diagnose the failing layer, compare materially different options, run a safe discriminating experiment, and escalate with evidence. Do not loop on failed attempts.
- A task is not complete until acceptance criteria, verification, risks, and applicable documentation/knowledge/report updates are accounted for.

## Updating the library

1. Edit the canonical role skill or shared instruction.
2. Run validation scripts and review the diff for accidental loss of technical requirements.
3. Update `ALL-ROLE-SKILLS.md`, `ROLE-INDEX.md`, and `SKILLS-RESOLVER.md` when role content or routing changes.
4. Test discovery and invocation in each target provider/version before claiming cross-provider compatibility.
5. Synchronize installed copies only after validation.

## Important compatibility note

This repository uses the common Agent Skills frontmatter convention (`name`, `description`). Providers may differ in skill discovery, automatic activation, project instruction loading, and context handling. The package aims for provider-neutral instructions; it cannot guarantee identical behavior across every agent without testing the exact provider and version.
