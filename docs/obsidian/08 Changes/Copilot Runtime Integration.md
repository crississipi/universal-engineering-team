---
type: change
status: active
owner: Technical Writer / Knowledge Engineer
last_verified: 2026-11-09
tags: [copilot, skills, hooks, task-reporting]
---
# Copilot Runtime Integration

- VS Code Copilot discovers project skills from `.github/skills/<role>/SKILL.md`.
- Canonical skill content remains under `skills/<role>/`; generated copies are synchronized with `scripts/sync-copilot-skills.py`.
- `.github/hooks/task-completion-reporting.json` captures prompt starts and checks terminal turns through `agentStop`.
- The hook asks the agent to create a pending structured report, then validates and publishes it with the canonical generator.
- Hook state and pending drafts are local-only under `.copilot-runtime/` and are gitignored.
- The VS Code Hooks feature is Preview. Test the actual Copilot runtime before relying on it.
- Validation does not prove that the model truly loaded a skill or that its reported work and tests occurred.
- If the hook reaches its bounded retry limit, it warns and allows the turn to end without a report; that failure must be disclosed and repaired.

See `docs/agent-execution/COPILOT-RUNTIME-INTEGRATION.md` and `docs/agent-execution/TASK-COMPLETION-REPORTING.md`.
