# Normalized pilot run metadata

## A. Run identification

| Field | Value |
|---|---|
| Scenario ID | `SCEN-DELIVERY-CROSSROLE-WEBHOOK` |
| Role | Delivery Lead |
| Run number | 1 |
| Scenario status | `approved` |
| Rubric version | `pilot-v2` |
| Base repository commit | unknown |
| Scenario revision commit | unknown |
| Skill revision commit | unknown |
| Working branch | unknown |
| Worktree / workspace | `C:\Users\cris\Downloads\set\ontap\pilot-delivery-1` (path in preserved session tool records) |

## B. Execution environment

| Field | Value |
|---|---|
| Provider | Copilot SDK in VS Code (runtime identity); underlying model-serving provider/version unknown |
| Host / application | VS Code |
| Displayed model label | `GPT-6 Luna` (UI notice quoted in `metadata.md`) |
| Exact model identifier / version | unknown |
| Agent mode | `Agent` |
| Interaction mode | `Interactive` |
| Model selection mode | `Auto` |
| Reasoning effort | `Standard` |
| Temperature | unknown |
| Permission mode | `Manual permissions` |
| Other relevant settings | `Remote Connections: Off`; metadata states other settings were not visible. |

## C. Execution timestamps

| Field | Value |
|---|---|
| Task start time (UTC) | unknown |
| Task end time (UTC) | unknown |
| Session creation time (UTC) | `2026-11-06T01:30:06.425Z` (`session.createdAt` from `list_sessions`) |
| Duration | unknown |
| Timestamp source | `metadata.md` says the available `list_sessions` `createdAt` timestamp was used as the available run-start timestamp; normalized here only as session creation time, not task start. |

## D. Prompt provenance

| Field | Value |
|---|---|
| Prompt filename | `pilot-output/prompt-used.md` |
| Prompt location | `C:\Users\cris\Downloads\set\ontap\pilot-evidence\delivery-lead\run-1\pilot-output\prompt-used.md` |
| Prompt SHA-256 | `03919c5e1e3dee8a0fd0f9f64661ba927574163a293b4928c94c970606695c1e` (calculated from this run's preserved file) |
| Prompt preserved verbatim | `pilot-output/prompt-used.md` and the recovered current-source copy have the same SHA-256. Compared with the checked-out approved source, the wording is identical; the modified copy is missing only the final line terminator. It is not byte-for-byte identical to the approved file. |
| Prompt modifications during execution | The recorded pre-artifact status was clean and the final status reports the source prompt as modified. The recovered diff establishes a missing final line terminator only; the prompt wording did not change during the run interval. |

## E. Output artifacts

| Artifact relative path | Description | Original preserved |
|---|---|---|
| `pilot-output/delivery-plan.md` | Primary proposed delivery plan; not an execution record. | Yes |
| `pilot-output/git-status.txt` | Captured final status output, including a modified source prompt and untracked output directory. | Yes |
| `pilot-output/metadata.md` | Run metadata, runtime values, transcript limitation, and execution record. | Yes |
| `pilot-output/prompt-used.md` | Preserved copy of the scenario prompt; source path is reported modified in Git status. | Yes |
| `pilot-output/session-context-export.json` | Truncated full-detail session-context representation, not a complete transcript. | Yes |
| `recovered-source-prompt-current.md` | Byte-for-byte copy of the modified source prompt from the retained run worktree. | Recovered |
| `recovered-source-prompt.diff` | Recovered Git diff between the modified source prompt and the checked-out source version. | Recovered |
| `normalized-metadata.md` | Post-run normalization output created by this curation, not a pilot-produced artifact. | No — created during this curation |

## F. Transcript and evidence completeness

| Evidence item | Status | Details |
|---|---|---|
| Full conversation transcript | partial | The preserved context export has a truncated user field and incomplete tool results; metadata says UI export/copy did not complete. |
| Raw session export | partial | `session-context-export.json` is present, but it is a truncated session-context representation rather than a complete export. |
| Tool-call evidence | partial | Export includes tool-call records, but not a complete verbatim record of all results. |
| Prompt evidence | partial | The preserved copy is byte-for-byte identical to the modified source copy recovered from the run worktree. The diff against the checked-out approved source shows only the absent final line terminator; the session-context export truncates the user turn, so it is not an independent full transcript comparison. |
| Final output artifact | complete | `pilot-output/delivery-plan.md` is present. |
| Git status evidence | complete | Exact final output is preserved in `pilot-output/git-status.txt`; it reports the out-of-directory modified prompt and `?? pilot-output/`. |
| Metadata evidence | partial | Runtime and session creation values are recorded, but task timestamps, duration, commits, and exact model version are missing. |

## G. Commands and validation

The following describes the pilot execution evidence, not this later normalization.

| Command / operation | Purpose | Actual result | Evidence location |
|---|---|---|---|
| `git status --short` before artifact creation | Baseline worktree check. | Executed; exit code 0; printed no lines. | `metadata.md` |
| `git status --short` after artifact creation | Capture final worktree state. | Executed; exit code 0; output was ` M evaluations/pilot/evidence/SCEN-DELIVERY-CROSSROLE-WEBHOOK/prompt-used.md` and `?? pilot-output/`. | `pilot-output/git-status.txt`; `metadata.md` |
| PowerShell prompt/session-context copying | Preserve prompt and session-context output. | Metadata states prompt was copied verbatim and the session-context export is preserved; exact command exit codes are not recorded here. | `metadata.md`; corresponding files in `pilot-output/` |
| Tests, builds, linters, validators, and application checks | No application code was changed; plan says these were not run. | Not executed. | `metadata.md` |
| VS Code export/copy action | Attempt full transcript preservation. | Executed but not completed; three clicks were interrupted by detected user input. | `metadata.md` |

## H. Repository scope and changes

| Field | Value |
|---|---|
| Final `git status --short` | ` M evaluations/pilot/evidence/SCEN-DELIVERY-CROSSROLE-WEBHOOK/prompt-used.md`<br>`?? pilot-output/` |
| Scope boundary verified | No. The captured status reports a modified scenario prompt outside `pilot-output/`; the untracked output directory itself is not enumerated. |
| Files changed | Files in `pilot-output/` listed in section E; captured status reports the directory as untracked rather than listing its contents. |
| Files outside permitted output directory | `evaluations/pilot/evidence/SCEN-DELIVERY-CROSSROLE-WEBHOOK/prompt-used.md` is reported modified. The newly created `normalized-metadata.md` is intentionally at the run root as required by this curation, not a pilot-execution change. |
| Scope deviations | The preserved status evidences a modified source prompt outside the permitted output directory. Its recovered diff is limited to the missing final line terminator; the cause of that whitespace change is unknown. The source prompt was not restored, and this normalization did not modify it. |

## I. Interruptions, errors, and limitations

Three UI attempts to export/copy the conversation were interrupted by detected user input; the window was reread and no further UI action was taken. The preserved session-context export truncates the user message and does not include complete tool results, so it is not a full transcript. The source prompt diff is recovered and shows only a missing final line terminator; why that whitespace change occurred is unknown. Exact model version, task start/end, duration, and commit identifiers remain unavailable.

## J. Metadata confidence and unresolved fields

| Field name | Current value | Reason it cannot be established | Could additional original evidence resolve it? |
|---|---|---|---|
| Base repository commit | unknown | No commit identifier appears in preserved run evidence. | Yes, if the original run's commit record exists. |
| Scenario revision commit | unknown | No scenario commit identifier appears in preserved run evidence. | Yes, if the original run's revision record exists. |
| Skill revision commit | unknown | No skill commit identifier appears in preserved run evidence. | Yes, if the original run's revision record exists. |
| Working branch | unknown | No branch value is preserved. | Yes, if contemporaneous Git/session metadata exists. |
| Exact model identifier/version | unknown | UI notice identifies a displayed model label only. | Yes, if original runtime metadata exists. |
| Task start and end times | unknown | The recorded timestamp is session `createdAt`; no task-end timestamp is preserved. | Yes, if original task/session event timestamps exist. |
| Duration | unknown | No duration is recorded. | Yes, if original session timing metadata exists. |
| Temperature and unlisted settings | unknown | No values are captured. | Yes, if a contemporaneous settings capture exists. |
| Source prompt modification | recovered | Pre-run status was clean; final status reports `M`. The preserved recovered diff shows only deletion of the final line terminator; prompt wording is unchanged. | The cause of the whitespace-only modification remains unknown. |
| Exact file-level contents of `pilot-output/` Git changes | partially supported | Git reports the directory as untracked without enumerating its contents. | Yes, if the original complete status or index snapshot is available. |

## K. Additional recovery checks

- **Recovered current source:** copied byte-for-byte from `pilot-delivery-1/evaluations/pilot/evidence/SCEN-DELIVERY-CROSSROLE-WEBHOOK/prompt-used.md` to `recovered-source-prompt-current.md` (SHA-256 `03919c5e1e3dee8a0fd0f9f64661ba927574163a293b4928c94c970606695c1e`); this hash matches the original `pilot-output/prompt-used.md`.
- **Recovered diff:** `recovered-source-prompt.diff` was captured with `git diff --no-ext-diff --binary` for that source path in the run worktree. It shows only the removed final line terminator versus the checked-out source; no wording changed. The preserved initial clean status and final modified status establish that the source changed during the run interval.
- **Other metadata:** checked the run-local transcript and named retained worktree. Current worktree refs are not timestamped to execution and were not used for historical commit or branch fields. No additional contemporaneous timestamps or settings were found; existing values remain as recorded above.
