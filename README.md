# Universal Engineering Team

A provider-portable, project-agnostic engineering team for AI coding agents.

This repository gives an AI coding assistant a consistent way to approach software development as a coordinated engineering organization rather than as one general-purpose assistant trying to do everything. It contains specialist role skills, shared operating instructions, ownership boundaries, engineering workflows, and documentation practices that can be reused across different repositories and technology stacks.

The library is designed for **GitHub Copilot, Claude Code, OpenAI Codex, Cursor, Gemini CLI, Antigravity, and other coding agents that support the Agent Skills `SKILL.md` convention**. Provider support and discovery paths can change, so use each provider's current documentation when configuring an agent not covered below.

> **Important:** Storing these files in one folder does not automatically make them available to every AI provider. Each provider must be configured to discover the skills, either through its supported global skill directory or through project-level skill directories.

---

## 1. What are these skills?

An agent skill is a focused set of instructions that teaches an AI coding agent how to perform a particular kind of work. A skill is usually a folder containing a `SKILL.md` file with a name, a description, and practical instructions.

Unlike a large prompt that tries to explain every engineering discipline at once, skills are designed to be loaded when relevant. The agent can inspect the skill descriptions, select the specialist guidance needed for the current task, and use that guidance alongside the actual source code, tests, project documentation, and available tools.

A skill is **not** a separate AI model, an autonomous employee, or a guarantee that the agent will execute every instruction perfectly. It is reusable operating guidance. The AI provider still supplies the model, tools, permissions, context window, and execution environment.

### How the library works

The library uses three instruction layers:

| Layer | File or location | Purpose |
|---|---|---|
| Shared engineering rules | `AGENTS.md` | Defines the team's common standards, workflow, role routing, collaboration, and definition of done. |
| Specialist expertise | `skills/roles/<role>/SKILL.md` | Provides focused responsibilities, decision boundaries, workflows, and deliverables for a particular engineering role. |
| Project-specific context | The target repository's own instructions and documentation | Describes the actual product, stack, architecture, commands, constraints, environments, and conventions. |

The agent should read the shared instructions, inspect the project, and activate only the specialist skills relevant to the task. Project facts must come from the project itself—not from assumptions embedded in a reusable skill.

### Typical task flow

1. **Understand the request** — identify the outcome, constraints, acceptance criteria, and risks.
2. **Discover the project** — inspect its instructions, codebase, architecture, dependencies, tests, and documentation.
3. **Select specialists** — choose the roles whose responsibilities match the work. A small change should not activate the entire team.
4. **Plan ownership and interfaces** — establish one accountable owner for each deliverable and define dependencies or contracts before parallel work.
5. **Implement incrementally** — make focused changes while following the project's conventions.
6. **Verify** — run appropriate tests and checks, and report actual results rather than assumed success.
7. **Document** — update relevant technical documentation, Graphify relationships, Obsidian notes, and the centralized HTML report where those facilities are used by the project.
8. **Review and close** — check integration, risks, outstanding work, and the definition of done.

For multi-role work, the **Delivery Lead is a coordinating responsibility** described in the shared constitution; it coordinates ownership, sequencing, handoffs, and closure. The Solution Architect leads cross-system technical design. These responsibilities are deliberately distinct.

---

## 2. What is included?

This package contains 16 specialist roles:

| Role | Primary use |
|---|---|
| Product Analyst | Requirements, user needs, scope, prioritization, and acceptance criteria. |
| Solution Architect | System design, architecture boundaries, technical decisions, and cross-system trade-offs. |
| API Manager | API contracts, standards, versioning, compatibility, and lifecycle. |
| Backend Developer | Server-side logic, services, jobs, and business workflows. |
| Frontend Developer | Web/mobile/client interfaces, UI state, and API consumption. |
| UX/UI Designer | User journeys, interaction patterns, visual hierarchy, and design-system guidance. |
| Database Manager | Data models, schema evolution, migrations, integrity, and query design. |
| Integration Engineer | External systems, adapters, events, webhooks, queues, and reconciliation. |
| Data Engineer | Data ingestion, transformation, movement, and analytical workflows. |
| QA Manager | Risk-based test strategy, coverage, defect triage, and quality evidence. |
| Penetration Tester / AppSec | Application, API, infrastructure, and integration security risks. |
| DevOps / SRE | Build, deployment, infrastructure, observability, reliability, and recovery. |
| Performance Engineer | Latency, throughput, resource use, and scalability. |
| Accessibility Specialist | Inclusive access and accessibility of interfaces and workflows. |
| Technical Writer / Knowledge Engineer | Technical documentation, Obsidian, Graphify, and the HTML engineering report. |
| Release Manager | Release readiness, approvals, rollout, rollback, and post-release verification. |

See [ROLE-INDEX.md](ROLE-INDEX.md) for role activation guidance and links to each complete skill.

---

## 3. Choose an installation scope

There are two common ways to install the skills.

### Option A — Global installation (recommended for personal use)

Install skills in your home-directory skill location. They can then be discovered across supported projects on that machine, without copying them into every repository.

This is a **per-computer** installation. It does not automatically make the skills available on another computer, in a remote development container, or in a provider's cloud agent.

### Option B — Project-level installation

Install skills inside a specific project repository. This is useful when:
- A team wants to version-control the same skill set with its project.
- Remote/cloud agents need access to the skills through the checked-out repository.
- Different projects need different versions or subsets of the engineering roles.

Do not install both globally and locally without a reason. If both copies exist, check the provider's precedence rules and keep them synchronized.

---

## 4. Install the skills on Windows

The following instructions use PowerShell and assume Git is installed.

### Step 1 — Get the repository

Clone the repository that contains this library:

```powershell
git clone https://github.com/YOUR-USERNAME/universal-engineering-team.git
cd universal-engineering-team
```

Replace the URL with the actual GitHub repository URL. If you downloaded a ZIP instead, extract it and open PowerShell in the extracted folder.

### Step 2 — Choose provider destinations

Common user-level skill locations include:

| Coding agent | User-level skill directory |
|---|---|
| GitHub Copilot | `$HOME\.copilot\skills` |
| Claude Code | `$HOME\.claude\skills` |
| OpenAI Codex | `$HOME\.agents\skills` or the provider's currently documented user skill directory |
| Cursor | `$HOME\.cursor\skills` or `$HOME\.agents\skills` |
| Gemini CLI | `$HOME\.gemini\skills` or `$HOME\.agents\skills`, depending on the supported version |
| Antigravity | Use its currently documented global skills directory; some versions use a Gemini/Antigravity-specific directory |

Provider support and paths may change. Confirm the current path in the official documentation for your installed version before relying on a global installation. In particular, distinguish an IDE's local skills from skills synchronized to cloud agents.

### Step 3 — Install globally with PowerShell

The script below copies each role folder (not just the `SKILL.md` file) into the selected user-level skill directory. It uses the shared `.agents/skills` directory as a convenient common destination for agents that support it, and also installs to the separate Claude Code and Copilot locations.

Run it from the root of this repository:

```powershell
$source = Join-Path (Get-Location) "skills\roles"

# Shared user-level location supported by several coding agents.
$shared = Join-Path $HOME ".agents\skills"

# Provider-specific locations.
$copilot = Join-Path $HOME ".copilot\skills"
$claude  = Join-Path $HOME ".claude\skills"

$destinations = @($shared, $copilot, $claude)

foreach ($destination in $destinations) {
    New-Item -ItemType Directory -Force -Path $destination | Out-Null

    Get-ChildItem -Path $source -Directory | ForEach-Object {
        $target = Join-Path $destination $_.Name

        # Replace the installed copy with the version in this repository.
        if (Test-Path $target) {
            Remove-Item -Path $target -Recurse -Force
        }

        Copy-Item -Path $_.FullName -Destination $target -Recurse
    }

    Write-Host "Installed skills to $destination"
}
```

**What this does:** installs all 16 role folders into the selected locations. It does not modify your projects, provider settings, or `AGENTS.md`. Review the destination paths before running the script, especially if you already maintain custom skills with the same folder names.

For a provider with a different global directory, add that verified directory to `$destinations`. Do not assume the shared directory is supported by every provider.

### Step 4 — Install or reference the shared constitution

The skills contain specialist instructions, but the root `AGENTS.md` defines how the roles collaborate. For each project, copy this file into the project root:

```powershell
Copy-Item ".\AGENTS.md" "C:\path\to\your-project\AGENTS.md"
```

If your provider supports a personal/global instruction file, you may also reference or adapt the constitution there. Do not assume that placing `AGENTS.md` in a global folder makes every provider load it automatically.

For project-specific instructions, keep the project's actual stack, build commands, test commands, architecture, and constraints in that project's own documentation. Avoid putting project-specific facts into the reusable global skills.

---

## 5. Install on macOS or Linux

From the repository root:

```bash
SOURCE="./skills/roles"

# Shared user-level location for agents that support the Agent Skills directory.
SHARED="$HOME/.agents/skills"

mkdir -p "$SHARED"

for role in "$SOURCE"/*; do
  [ -d "$role" ] || continue
  name="$(basename "$role")"
  rm -rf "$SHARED/$name"
  cp -R "$role" "$SHARED/$name"
done
```

For provider-specific directories, repeat the copy operation using the global path documented by that provider. For example, Claude Code commonly uses `~/.claude/skills`, and GitHub Copilot supports `~/.copilot/skills`.

Copy the root `AGENTS.md` into each project that should use the shared engineering constitution.

---

## 6. Project-level installation

For a project-specific installation, copy the skill folders into a supported project skill directory. Examples include:

```text
your-project/
├── AGENTS.md
├── .agents/
│   └── skills/
│       ├── solution-architect/
│       │   └── SKILL.md
│       ├── backend-developer/
│       │   └── SKILL.md
│       └── qa-manager/
│           └── SKILL.md
└── src/
```

Some providers use their own project-specific directory, such as `.github/skills/`, `.claude/skills/`, or `.cursor/skills/`. Check the provider's current documentation and use the appropriate location.

You do not need to install all 16 roles into every project. Install the full set if the project genuinely benefits from the whole team, or install only the roles relevant to that repository.

---

## 7. Verify that the skills are discovered

After installation:

1. Restart the coding agent or reload its skills if the provider supports a reload command.
2. Ask the agent: **"List the engineering skills you can discover and tell me where each one was loaded from."**
3. Ask a small test task, such as: **"Review this API change. Identify which engineering roles should be involved and explain why before making changes."**
4. Confirm that it selects relevant roles instead of loading every skill for every task.
5. Confirm that it reads the project's `AGENTS.md` and inspects the actual repository before making assumptions.

Useful provider-specific checks may include:
- GitHub Copilot CLI: use its `/skills list`, `/skills info`, or `copilot skill list` commands where available.
- Claude Code: use `/skills` to inspect available skills.
- Antigravity: use its skills listing or customization interface if available.
- Other agents: consult the provider's current skill-discovery and reload commands.

A skill file being present on disk does not prove that a provider has loaded it. Verify discovery from inside the agent.

---

## 8. How to use the skills during system development

Once installed and discovered, describe the task normally. The agent should use the skill descriptions to decide which specialists are relevant.

Examples:

| Development task | Likely roles |
|---|---|
| Add a form to an existing web page | Frontend Developer, UX/UI Designer, QA Manager; Accessibility Specialist when relevant. |
| Add a new REST API endpoint | API Manager, Backend Developer, QA Manager; Database Manager if persistence changes. |
| Integrate a payment or CRM provider | Solution Architect, API Manager, Integration Engineer, Backend Developer, Security, QA Manager. |
| Design a multi-service application | Product Analyst, Solution Architect, API Manager, Database Manager, DevOps/SRE, relevant implementation roles. |
| Investigate a slow query or endpoint | Performance Engineer, Database Manager or Backend Developer, QA Manager; DevOps/SRE if runtime telemetry is needed. |
| Prepare a production release | Release Manager, DevOps/SRE, QA Manager, Security, relevant service owners. |
| Update system documentation | Technical Writer / Knowledge Engineer, with facts verified by the relevant technical owners. |

You can also explicitly request a specialist, for example:

```text
Use the Solution Architect and Backend Developer skills to assess this change.
Inspect the existing architecture first, propose a safe implementation plan,
then implement and verify the agreed approach.
```

Explicitly naming a role is optional when the provider supports automatic skill selection. If the agent does not activate the expected skill, mention it directly or check that the provider has discovered and enabled it.

---

## 9. Keep the skills updated

Treat the Git repository as the **single source of truth**.

Recommended update process:

1. Make changes in the canonical skills repository.
2. Review the changes and commit them.
3. Pull the latest repository version on each computer.
4. Re-run the installation script to refresh installed copies.
5. Reload or restart each coding agent.
6. Verify that the updated skill is discoverable.

For example:

```powershell
git pull
```

Then rerun the PowerShell installation script from Section 4.

Do not independently edit multiple installed copies. That creates version drift and makes it difficult to know which instructions an agent is using.

For organization-wide or cloud-agent use, publish the repository through an approved internal source and configure each provider or agent environment to check out or synchronize the skills. A personal local installation does not automatically provision skills to teammates or remote agents.

---

## 10. Documentation and knowledge workflow

The engineering team expects documentation to remain aligned with the implementation. The package includes guidance for:

- **Graphify** — model relationships between services, modules, APIs, data, decisions, and workflows.
- **Obsidian** — maintain connected engineering knowledge, decisions, concepts, and operational notes.
- **Central HTML report** — provide a navigable, searchable walkthrough of the system, architecture, modules, interfaces, and changes.

Read the relevant guides before using these tools:

- [Graphify guidance](docs/knowledge/GRAPHIFY.md)
- [Obsidian guidance](docs/knowledge/OBSIDIAN.md)
- [HTML report specification](docs/report/REPORT_SPEC.md)
- [Team workflow](docs/team/workflow.md)
- [Role ownership](docs/team/ownership.md)

These are project documentation practices, not automatic integrations. The agent must inspect the actual Graphify and Obsidian setup, use the installed tool's supported format, and update only the affected report sections. If a tool is not installed or configured, the agent should report that limitation rather than claim it updated the tool.

---

## 11. Important design principles

- **Project-agnostic:** skills discover the actual project's stack and conventions before prescribing implementation details.
- **Progressive disclosure:** load only relevant specialist skills to conserve context and reduce instruction conflicts.
- **Clear ownership:** each deliverable has one accountable owner; specialists do not silently overwrite each other's decisions.
- **Explicit handoffs:** cross-role work includes interfaces, assumptions, evidence, risks, and next actions.
- **Anti-stuck behavior:** diagnose failures, consider materially different approaches, run a safe experiment, and escalate with a recommendation instead of repeating ineffective attempts.
- **Security and permission boundaries:** skills do not grant access or authorize destructive, production, or privileged actions.
- **Evidence-based completion:** agents report the checks actually run and disclose failures, skipped checks, and unresolved risks.
- **Documentation is part of delivery:** applicable technical documentation, Graphify, Obsidian, and the HTML report are updated as part of the definition of done.

---

## 12. Troubleshooting

### The agent does not see a skill
- Confirm that the folder contains a file named exactly `SKILL.md`.
- Confirm the YAML frontmatter contains a valid `name` and `description`.
- Confirm the skill folder is in a directory the provider actually scans.
- Restart or reload the agent.
- Check whether the provider requires Agent Skills to be enabled in settings.
- Ask the agent to report its discovered skill names and locations.

### The agent sees the skill but does not use it
- Make the skill description clearly state the task types that should activate it.
- Ask the agent to use the named skill explicitly.
- Avoid vague or overlapping descriptions across roles.
- Check that the task genuinely falls within the skill's responsibility.

### Different providers behave differently
The Agent Skills format improves portability, but it does not make provider behavior identical. Providers may differ in discovery paths, frontmatter support, context loading, tool access, permissions, and cloud synchronization. Keep the skill content standard and provider-independent, then follow each provider's setup requirements.

### Global skills are missing in a remote or cloud session
Global directories on your computer are not necessarily synchronized to remote environments. Install the skills at project level, add them to an approved dotfiles/bootstrap process, or configure the provider's organization/cloud environment to retrieve the canonical repository.

---

## 13. Repository map

```text
universal-engineering-team/
├── AGENTS.md                         # Shared engineering constitution
├── README.md                         # Introduction and setup guide
├── ROLE-INDEX.md                     # Role directory and activation guidance
├── ALL-ROLE-SKILLS.md                # Consolidated role reference
├── skills/
│   └── roles/
│       ├── product-analyst/
│       ├── solution-architect/
│       ├── api-manager/
│       ├── backend-developer/
│       ├── frontend-developer/
│       ├── ux-ui-designer/
│       ├── database-manager/
│       ├── integration-engineer/
│       ├── data-engineer/
│       ├── qa-manager/
│       ├── penetration-tester/
│       ├── devops-sre/
│       ├── performance-engineer/
│       ├── accessibility-specialist/
│       ├── technical-writer-knowledge-engineer/
│       └── release-manager/
└── docs/
    ├── team/
    ├── knowledge/
    ├── obsidian/
    └── report/
```

---

## 14. Final note

This library provides a reusable engineering operating model—not a substitute for project discovery, engineering judgment, human approval, testing, or provider configuration.

For best results, install the skills in a supported location, make the shared constitution available to the project, verify that the agent discovers the skills, and keep project-specific facts in the project itself.
