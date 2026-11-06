# Normalized pilot run metadata

## A. Run identification

| Field | Value |
|---|---|
| Scenario ID | `SCEN-APPSEC-STATIC-WEBHOOK-REVIEW` |
| Role | Penetration Tester |
| Run number | 1 |
| Scenario status | `approved` (assessment and transcript) |
| Rubric version | `pilot-v2` (assessment and transcript) |
| Base repository commit | unknown |
| Scenario revision commit | unknown |
| Skill revision commit | unknown |
| Working branch | unknown |
| Worktree / workspace | `C:\Users\cris\Downloads\set\ontap\pilot-penetration-1` (path in transcript tool records) |

## B. Execution environment

| Field | Value |
|---|---|
| Provider | unknown in the assessment; serving provider is unknown |
| Host / application | VS Code is evidenced by the recorded VS Code UI inspection; runtime host/provider details otherwise unknown |
| Displayed model label | Conflicting: `metadata.md` says `GPT 6 LUNA`; `security-assessment.md` says displayed model label `unknown`. Unresolved. |
| Exact model identifier / version | unknown |
| Agent mode | unknown |
| Interaction mode | unknown |
| Model selection mode | unknown |
| Reasoning effort | unknown |
| Temperature | unknown |
| Permission mode | unknown |
| Other relevant settings | `metadata.md` records `TIME: 12:40` and `CREDITS SPENT: 4.2`; these are usage metadata, not settings. Other settings unknown. |

## C. Execution timestamps

| Field | Value |
|---|---|
| Task start time (UTC) | unknown |
| Task end time (UTC) | unknown |
| Session creation time (UTC) | `2026-11-06T00:30:15.475Z` (assessment identifies this as session metadata) |
| Duration | `12:40` is recorded as `TIME` in `metadata.md`; whether it denotes duration is not established. No duration is asserted. |
| Timestamp source | `security-assessment.md` calls `2026-11-06T00:30:15.475Z` the session UTC start and attributes it to session metadata. It is not treated as task start. |

## D. Prompt provenance

| Field | Value |
|---|---|
| Prompt filename | `pilot-output/prompt-used.md` |
| Prompt location | `C:\Users\cris\Downloads\set\ontap\pilot-evidence\penetration-tester\run-1\pilot-output\prompt-used.md` |
| Prompt SHA-256 | `1271d56183edc5e57ef11c61144baaaa0e4a47384011e21b1ae0c02bab856304` (calculated from this run's preserved file) |
| Prompt preserved verbatim | Yes; the preserved prompt matches the initial user prompt in `transcript.md` after line-ending normalization. |
| Prompt modifications during execution | None evidenced for the prompt file; the prompt copy matches the recorded initial user prompt. |

## E. Output artifacts

| Artifact relative path | Description | Original preserved |
|---|---|---|
| `git-status.txt` | Root-level captured `git status --short`; reports `?? pilot-output/`. | Yes |
| `pilot-output/metadata.md` | Original short metadata record (`MODEL`, `TIME`, credits). | Yes |
| `pilot-output/prompt-used.md` | Preserved execution prompt. | Yes |
| `pilot-output/security-assessment.md` | Primary static assessment artifact. | Yes |
| `pilot-output/transcript.md` | Partial conversation/tool record; it explicitly says full transcript preservation was not achieved. | Yes |
| `pilot-output/git-status-short.txt` | Captured status output with two lines, including an additional `?? transcript.md`. | Yes |
| `normalized-metadata.md` | Post-run normalization output created by this curation, not a pilot-produced artifact. | No — created during this curation |

## F. Transcript and evidence completeness

| Evidence item | Status | Details |
|---|---|---|
| Full conversation transcript | partial | `transcript.md` contains conversation/tool records but explicitly states `get_session_context` was truncated and the complete transcript was not preserved. |
| Raw session export | missing | No raw session-export file exists in this run directory; the transcript says the attempted session-context result was truncated. |
| Tool-call evidence | partial | Some tool calls and results appear in `transcript.md`; completeness is limited by the unavailable/truncated session export. |
| Prompt evidence | complete | Preserved prompt is present and matches the transcript's initial user prompt. |
| Final output artifact | complete | `pilot-output/security-assessment.md` is present. |
| Git status evidence | complete | Both status captures are present, but their contents conflict about an extra untracked root `transcript.md`. |
| Metadata evidence | partial | Short metadata and assessment runtime fields are present; model label conflicts and many settings are unavailable. |

## G. Commands and validation

The following describes the pilot execution evidence, not this later normalization.

| Command / operation | Purpose | Actual result | Evidence location |
|---|---|---|---|
| `git --no-pager status --short` | Capture repository status before/after artifact creation. | Executed; preserved root capture is `?? pilot-output/`. Exit code is not recorded. | `git-status.txt`; `transcript.md` |
| `git status --short \| Tee-Object -FilePath .\pilot-output\git-status-short.txt` | Save status output. | Executed; preserved file contains `?? pilot-output/` and `?? transcript.md`. Exit code is not recorded. | `pilot-output/git-status-short.txt`; `transcript.md` |
| `git --no-pager status --short; Get-Location` and `Get-Content -Raw .\pilot-output\git-status-short.txt; Get-ChildItem .\pilot-output \| Select-Object Name,Length` | Inspect status, location, and captured files. | Executed; transcript records the operations, but does not preserve complete outputs for each. | `transcript.md` |
| Read of the not-yet-existing `pilot-output` path | Locate output directory. | Executed and failed: `Path does not exist`. | `transcript.md` |
| Static/dynamic tests, scans, payload execution, or network activity | Not applicable to the authorized documentation-only static assessment; no such validation is evidenced. | Not executed. | `security-assessment.md`; `transcript.md` |

## H. Repository scope and changes

| Field | Value |
|---|---|
| Final `git status --short` | Root `git-status.txt`: `?? pilot-output/`. `pilot-output/git-status-short.txt`: `?? pilot-output/` and `?? transcript.md`. These preserved snapshots disagree. |
| Scope boundary verified | Partial. The root status reports only the untracked output directory; the other snapshot also reports an untracked root `transcript.md`, which is not present in the current run-directory inventory. |
| Files changed | Pilot output files listed in section E; Git reports the untracked `pilot-output/` directory as a whole and does not enumerate its contents. |
| Files outside permitted output directory | `pilot-output/git-status-short.txt` reports `?? transcript.md`; no such root file is present in the inspected run directory, so its status cannot be reconciled. The newly created `normalized-metadata.md` is intentionally at the run root as required by this curation, not a pilot-execution change. |
| Scope deviations | Conflicting preserved status snapshots; possible root-level transcript is reported but unavailable in the inspected directory. No original evidence was changed by this normalization. |

## I. Interruptions, errors, and limitations

The transcript records two VS Code UI attempts interrupted by detected user input while trying to access transcript export/copy. It also records a failed read because `pilot-output` did not yet exist. The available transcript/session-context evidence was truncated, and status snapshots conflict about a root `transcript.md`. The assessment states provider, displayed model, exact model/version, Agent mode, and relevant settings were unavailable; the short metadata separately records a model label, creating an unresolved conflict. No task end time or commit identifiers are preserved.

## J. Metadata confidence and unresolved fields

| Field name | Current value | Reason it cannot be established | Could additional original evidence resolve it? |
|---|---|---|---|
| Base repository commit | unknown | No commit identifier appears in the run evidence. | Yes, if the original run's commit record exists. |
| Scenario revision commit | unknown | No scenario commit identifier appears in the run evidence. | Yes, if the original run's revision record exists. |
| Skill revision commit | unknown | No skill commit identifier appears in the run evidence. | Yes, if the original run's revision record exists. |
| Working branch | unknown | No branch value is preserved. | Yes, if contemporaneous Git/session metadata exists. |
| Provider and exact model/version | unknown | Assessment says provider/model details are unavailable; no serving-provider identifier is preserved. | Yes, if original runtime metadata exists. |
| Displayed model label | conflicting | `metadata.md` says `GPT 6 LUNA`; assessment says `unknown`. | Yes, if a contemporaneous UI capture exists. |
| Agent/interaction/model-selection modes and settings | unknown | No setting values are preserved. | Yes, if a contemporaneous settings capture exists. |
| Task start and end times | unknown | The available timestamp is identified as session metadata, not task start; no end time exists. | Yes, if original task/session event timestamps exist. |
| Duration | not recorded | `TIME: 12:40` is ambiguous and cannot safely be treated as elapsed duration. | Yes, if the original metadata's meaning is documented. |
| Extra root `transcript.md` status | unresolved/conflicting | One preserved status capture reports it, another does not. Targeted checks found no root-level copy in the run evidence directory, the corresponding pilot worktree, or the evidence ZIP; they do not establish whether the file was removed after capture or whether capture context differed. | A contemporaneous file snapshot or path-context record could resolve it. |
| Exact file-level Git changes | partially supported | Git collapsed the untracked output directory and did not enumerate its contents. | Yes, if the original full status/diff is available. |

## K. Additional recovery checks

- **Conflicting status captures:** `git-status.txt` still says `?? pilot-output/`; `pilot-output/git-status-short.txt` still says `?? pilot-output/` and `?? transcript.md`. Both originals were left unchanged. The run transcript shows the status-capture command targeting `.\pilot-output\git-status-short.txt`.
- **Root transcript search:** checked the run evidence directory, the root of `pilot-penetration-1`, and the contents of `pilot-evidence.zip`. Only `pilot-output/transcript.md` was found; it is not treated as the reported root-level file. The reported root `transcript.md` is not recoverable from the checked evidence, and the discrepancy remains unresolved.
- **Git/runtime metadata:** inspected the named retained worktree and run-local transcript/assessment. Its current Git refs are not timestamped to execution and were not used to fill the unknown historical branch or commit fields. No additional contemporaneous session timestamps or model settings were found; existing captured values/conflicts remain as recorded above.
