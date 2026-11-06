# Pilot run metadata

- Scenario: `SCEN-DELIVERY-CROSSROLE-WEBHOOK`
- Scenario status / rubric: `approved` / `pilot-v2`
- UTC start time: `2026-11-06T01:30:06.425Z` (session `createdAt` exposed by `list_sessions`; used as the available run-start timestamp).
- Runtime/provider: Copilot SDK in VS Code. UI header displayed `Copilot`; UI notice stated “Copilot Fusion selected GPT-6 Luna because it was the best choice out of the models available in your plan.” The underlying routing provider/version beyond these labels is unknown.
- Displayed model label: `GPT-6 Luna`.
- Exact model/version: `unknown` (not exposed).
- Agent mode: UI displayed `Agent`; mode picker displayed `Interactive`.
- Other relevant visible settings: model selection `Auto`; `Standard`; permissions `Manual permissions`; `Remote Connections: Off`. Other settings not visible here: `unknown`.

## Evidence capture and limitations

- The original scenario prompt is preserved verbatim as `pilot-output/prompt-used.md`, copied from `evaluations/pilot/evidence/SCEN-DELIVERY-CROSSROLE-WEBHOOK/prompt-used.md`.
- A full-detail session-context export is preserved as `pilot-output/session-context-export.json`. The export is not a complete transcript: its `user` field is truncated, and it does not contain a complete verbatim record of all tool results. It has not been manually reconstructed or summarized.
- The VS Code UI export/copy action could not be completed: three click attempts were interrupted because user input was detected in that window. The window was re-read after interruptions; no further UI action was taken.
- `pilot-output/git-status.txt` contains the exact final `git status --short` output captured after the other pilot-output artifacts were present. Because Git collapses the untracked directory, that output reports the `pilot-output/` directory rather than enumerating its contents.

## Execution record

- Created: `pilot-output/delivery-plan.md`.
- No application code was changed. No feature implementation, tests, build, static analysis, security testing, formal handoff, feature approval, release, or deployment was performed.
- The only shell command used for repository state was `git status --short` (PowerShell). Its pre-change execution exited 0 and printed no lines. Its final execution and output are preserved in `pilot-output/git-status.txt`.
- Read-only inspection used `view`, `rg`, and `glob`; session/runtime evidence used `list_sessions`, `get_session_context`, `computer-use-list_apps`, and `computer-use-get_window_state`. Planning skills invoked: `delivery-lead` and `brainstorming`. Artifact edits used `apply_patch`; evidence files were copied without alteration.
- Repository validators and tests were not run because this was a planning-only task and no canonical repository files were changed.
