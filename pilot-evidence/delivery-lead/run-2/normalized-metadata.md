# Normalized pilot run metadata

## A. Run identification

| Field | Value |
|---|---|
| Scenario ID | `SCEN-DELIVERY-CROSSROLE-WEBHOOK` |
| Role | Delivery Lead |
| Run number | 2 |
| Scenario status | `approved` (recorded in the run's prompt/context) |
| Rubric version | `pilot-v2` (recorded in the run's prompt/context) |
| Base repository commit | unknown |
| Scenario revision commit | unknown |
| Skill revision commit | unknown |
| Working branch | unknown |
| Worktree / workspace | `C:\Users\cris\Downloads\set\ontap\pilot-delivery-2` (path in preserved session tool records) |

## B. Execution environment

| Field | Value |
|---|---|
| Provider | Runtime/provider not stated; underlying model-serving provider unknown |
| Host / application | VS Code is evidenced by the captured VS Code interaction calls. |
| Displayed model label | `GPT 6 LUNA` (`metadata.md`; no independent display capture is preserved) |
| Exact model identifier / version | unknown |
| Agent mode | unknown |
| Interaction mode | unknown |
| Model selection mode | unknown |
| Reasoning effort | unknown |
| Temperature | unknown |
| Permission mode | unknown |
| Other relevant settings | `metadata.md` records `DURATION: 17m 44s` and `CREDITS USED: 8.4`; these are usage metadata, not settings. Other settings unknown. |

## C. Execution timestamps

| Field | Value |
|---|---|
| Task start time (UTC) | unknown |
| Task end time (UTC) | unknown |
| Session creation time (UTC) | unknown |
| Duration | `17m 44s` (`metadata.md`, field `DURATION`); no timestamps are inferred from it. |
| Timestamp source | No task or session timestamp is recorded in the run-local metadata. |

## D. Prompt provenance

| Field | Value |
|---|---|
| Prompt filename | `pilot-output/prompt-used.md` |
| Prompt location | `C:\Users\cris\Downloads\set\ontap\pilot-evidence\delivery-lead\run-2\pilot-output\prompt-used.md` |
| Prompt SHA-256 | `022b4e2765ba34516be265bd336d516a63b9566343d37336d580ac38bf3109e9` (calculated from this run's preserved file) |
| Prompt preserved verbatim | `pilot-output/prompt-used.md` and the recovered current-source copy have the same SHA-256. Compared with the checked-out approved source, the wording is identical; the modified copy has one extra blank line at EOF. It is not byte-for-byte identical to the approved file. |
| Prompt modifications during execution | Final status reports the source prompt as modified. The recovered diff shows one extra blank line at EOF. The initial status command is recorded, but its result is not preserved, so when the source changed cannot be established. |

## E. Output artifacts

| Artifact relative path | Description | Original preserved |
|---|---|---|
| `pilot-output/delivery-plan.md` | Primary proposed delivery plan; not an execution record. | Yes |
| `pilot-output/git-status-short.txt` | Preserved final status output, including a modified source prompt and untracked output directory. | Yes |
| `pilot-output/metadata.md` | Short metadata record (model label, duration, credits). | Yes |
| `pilot-output/prompt-used.md` | Preserved scenario prompt file. | Yes |
| `pilot-output/transcript.json` | Truncated full-detail session-context representation, not a complete transcript. | Yes |
| `recovered-source-prompt-current.md` | Byte-for-byte copy of the modified source prompt from the retained run worktree. | Recovered |
| `recovered-source-prompt.diff` | Recovered Git diff between the modified source prompt and the checked-out source version. | Recovered |
| `normalized-metadata.md` | Post-run normalization output created by this curation, not a pilot-produced artifact. | No — created during this curation |

## F. Transcript and evidence completeness

| Evidence item | Status | Details |
|---|---|---|
| Full conversation transcript | partial | `transcript.json` is a session-context export with `truncated: true`; its user message is truncated and its assistant content is a summary, not a complete transcript. |
| Raw session export | partial | `transcript.json` preserves the raw session-context representation but explicitly reports truncation. |
| Tool-call evidence | partial | Export includes tool-call names/inputs, but does not preserve a complete verbatim record of tool results. |
| Prompt evidence | partial | The preserved copy is byte-for-byte identical to the modified source copy recovered from the run worktree. The diff against the checked-out approved source shows one extra blank line at EOF; the session export truncates the user turn, so exact input identity cannot be independently checked. |
| Final output artifact | complete | `pilot-output/delivery-plan.md` is present. |
| Git status evidence | complete | Preserved status output reports the modified scenario prompt and `?? pilot-output/`; output directory contents are not enumerated. |
| Metadata evidence | partial | Model label, duration, and credits are recorded; timestamps, exact model version, and settings are unavailable. |

## G. Commands and validation

The following describes the pilot execution evidence, not this later normalization.

| Command / operation | Purpose | Actual result | Evidence location |
|---|---|---|---|
| `git --no-pager status --short` | Check initial repository state. | Executed; the session export records the command, but its result is not preserved there. | `transcript.json` |
| `git --no-pager status --short` and PowerShell status capture | Capture final scope. | Preserved status is ` M evaluations/pilot/evidence/SCEN-DELIVERY-CROSSROLE-WEBHOOK/prompt-used.md` and `?? pilot-output/`; exit code is not available in the preserved evidence. | `pilot-output/git-status-short.txt`; `transcript.json` |
| `get_session_context` | Preserve conversation/session evidence. | Export exists, parses as JSON according to the run record, but has `truncated: true`, `hasMoreHistory: false`, one in-progress turn, and 90 tool-call entries. | `pilot-output/transcript.json` |
| Tests, builds, linters, validators, or application checks | No implementation was performed in this planning-only task. | Not executed; no passing result is claimed. | `delivery-plan.md`; `transcript.json` |

## H. Repository scope and changes

| Field | Value |
|---|---|
| Final `git status --short` | ` M evaluations/pilot/evidence/SCEN-DELIVERY-CROSSROLE-WEBHOOK/prompt-used.md`<br>`?? pilot-output/` |
| Scope boundary verified | No. The preserved output reports a modified source prompt outside `pilot-output/`; the untracked output directory is collapsed. |
| Files changed | Files in `pilot-output/` listed in section E; Git reports the directory, not its individual contents. |
| Files outside permitted output directory | `evaluations/pilot/evidence/SCEN-DELIVERY-CROSSROLE-WEBHOOK/prompt-used.md` is reported modified. The newly created `normalized-metadata.md` is intentionally at the run root as required by this curation, not a pilot-execution change. |
| Scope deviations | Preserved status evidences a modified source prompt outside the permitted output directory. Its recovered diff is limited to one extra blank line at EOF; the initial status result is absent, so the timing and cause remain unknown. The source prompt was not restored, and this normalization did not modify it. |

## I. Interruptions, errors, and limitations

No interruptions or errors are described in the preserved run records. The session-context export is explicitly truncated and does not contain a complete transcript or complete tool results. The source diff is recovered and shows one extra blank line at EOF, but the initial status result is missing, so it is unknown whether that change occurred during the run. Task/session timestamps, exact model version, runtime settings, and commit identifiers remain unavailable.

## J. Metadata confidence and unresolved fields

| Field name | Current value | Reason it cannot be established | Could additional original evidence resolve it? |
|---|---|---|---|
| Base repository commit | unknown | No commit identifier appears in preserved run evidence. | Yes, if the original run's commit record exists. |
| Scenario revision commit | unknown | No scenario commit identifier appears in preserved run evidence. | Yes, if the original run's revision record exists. |
| Skill revision commit | unknown | No skill commit identifier appears in preserved run evidence. | Yes, if the original run's revision record exists. |
| Working branch | unknown | No branch value is preserved. | Yes, if contemporaneous Git/session metadata exists. |
| Runtime/provider and exact model identifier/version | unknown | Only a model label is present in short metadata; provider routing/version is absent. | Yes, if original runtime metadata exists. |
| Agent/interaction/model-selection modes and settings | unknown | No values are preserved. | Yes, if a contemporaneous settings capture exists. |
| Task start/end and session creation times | unknown | No timestamps are preserved. | Yes, if original task/session event timestamps exist. |
| Source prompt modification | diff recovered; timing unresolved | Final status reports `M`, and the recovered diff shows one extra blank line at EOF. The initial status command has no preserved output. | A preserved initial status result or file snapshot could establish when it changed. |
| Exact file-level Git changes | partially supported | `?? pilot-output/` does not enumerate its files. | Yes, if the original full status/diff is available. |
| Tool operation results | partially supported | Session export records inputs/calls but is truncated and lacks complete tool results. | Yes, if a complete session/tool log exists. |

## K. Additional recovery checks

- **Recovered current source:** copied byte-for-byte from `pilot-delivery-2/evaluations/pilot/evidence/SCEN-DELIVERY-CROSSROLE-WEBHOOK/prompt-used.md` to `recovered-source-prompt-current.md` (SHA-256 `022b4e2765ba34516be265bd336d516a63b9566343d37336d580ac38bf3109e9`); this hash matches the original `pilot-output/prompt-used.md`.
- **Recovered diff:** `recovered-source-prompt.diff` was captured with `git diff --no-ext-diff --binary` for that source path in the run worktree. It shows one added blank line at EOF versus the checked-out source. The run's final status proves the file was modified by the final capture; the missing initial status result prevents timing attribution.
- **Other metadata:** checked the run-local transcript and named retained worktree. Current worktree refs are not timestamped to execution and were not used for historical commit or branch fields. No additional contemporaneous timestamps or settings were found; existing values remain as recorded above.
