# VS Code GitHub Copilot runtime integration

## Scope and prerequisites

This integration targets the VS Code **Copilot** session target and its shared Copilot hook runtime. VS Code's Agent Hooks UI is currently Preview. Hooks are executable repository code and must be reviewed and tested in a trusted workspace before relying on them.

Official references:

- [VS Code agent hooks](https://code.visualstudio.com/docs/agent-customization/hooks)
- [VS Code Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [GitHub Copilot hooks reference](https://docs.github.com/en/copilot/reference/hooks-reference)

## Native skill discovery

Copilot discovers project skills from `.github/skills/<skill-name>/SKILL.md`. Canonical role skills remain under `skills/<role>/`; do not edit generated copies directly.

Run:

```powershell
python scripts/sync-copilot-skills.py --write
python scripts/sync-copilot-skills.py --check
```

The synchronizer mirrors complete role directories, including referenced resources. Run `--check` after canonical skill edits. Copilot may automatically load a skill when its description matches the task, but discovery does not guarantee activation. The coordinating agent must still select the smallest sufficient role set and read the canonical skill content before claiming activation.

## Completion hook lifecycle

`.github/hooks/task-completion-reporting.json` registers:

- `userPromptSubmitted`: records an execution ID and offset-aware start timestamp for the submitted prompt. Prompt text is not persisted by this hook.
- `agentStop`: checks for the model-authored structured report input. If missing or invalid, it asks the agent to create or correct it and continues the turn. After validation, the hook invokes `scripts/report-task-completion.py` and publishes the JSON and Markdown report.

The model writes its report input to:

```
.copilot-runtime/task-completion-pending/<execution_id>.json
```

The hook supplies the exact execution ID and start timestamp in its continuation instruction. Runtime state is kept under `.copilot-runtime/task-state/`; both runtime directories are gitignored. The hook removes the pending input and prompt state after successful publication.

The hook retries a missing or invalid report up to three times. If it still cannot publish the report, it emits a warning and allows the turn to end; this is an explicit failure mode, not a successful report. Inspect the hook warning and create a corrected report manually when this occurs.

## Evidence and limitations

- The model-authored report is still a claim. The hook validates structure, matching execution identity, and timestamps; it does not independently prove work performed, skills loaded, tests executed, or approvals granted.
- Only list a role if its canonical skill content was actually read in the current task. Keep considered-but-unread roles out of `activated_roles`.
- Record exact verification commands and observed results. Unknown or unrun checks must remain unrun.
- The hook is triggered by agent turn completion, not a daily schedule. A turn that ends to ask for clarification may be reported as blocked; the next user prompt receives a new execution identity.
- The hook depends on Python being available to the VS Code Copilot hook process. It prefers the repository `.venv` interpreter when present, then falls back to the interpreter running the hook command.
- This workspace hook applies only when VS Code runs the repository's Copilot harness and loads the trusted workspace hook configuration. It does not configure other harnesses or guarantee behavior in remote/cloud workspaces.
- Do not create a duplicate hook in the Hooks UI if this repository hook is already loaded. Use the UI to inspect and verify the workspace hook.
