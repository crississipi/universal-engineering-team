# Normalized pilot run metadata

## A. Run identification

| Field | Value |
|---|---|
| Scenario ID | `SCEN-APPSEC-STATIC-WEBHOOK-REVIEW` |
| Role | Penetration Tester |
| Run number | 3 |
| Scenario status | `approved` (assessment and transcript) |
| Rubric version | `pilot-v2` (assessment and transcript) |
| Base repository commit | unknown |
| Scenario revision commit | unknown |
| Skill revision commit | unknown |
| Working branch | unknown |
| Worktree / workspace | `C:\Users\cris\Downloads\set\ontap\pilot-penetration-3` (path in transcript tool records) |

## B. Execution environment

| Field | Value |
|---|---|
| Provider | `Copilot Fusion` (provider label displayed in VS Code chat); underlying model-serving provider unknown |
| Host / application | VS Code |
| Displayed model label | `GPT-6 Luna` (`security-assessment.md`; `metadata.md` records `GPT 6 LUNA`) |
| Exact model identifier / version | `gpt-6-luna` was exposed as the displayed identifier; no further version detail is recorded. |
| Agent mode | `Agent` |
| Interaction mode | `Interactive` (`Pick Mode`) |
| Model selection mode | `Auto` |
| Reasoning effort | `Standard` |
| Temperature | unknown |
| Permission mode | `Manual permissions` |
| Other relevant settings | `Remote Connections: Off`; `metadata.md` records `DURATION: 7m 57s` and `CREDITS USED: 6.4` (usage metadata, not settings). |

## C. Execution timestamps

| Field | Value |
|---|---|
| Task start time (UTC) | unknown |
| Task end time (UTC) | unknown |
| Session creation time (UTC) | `2026-11-06T01:11:43.933Z` (`security-assessment.md` identifies this as session metadata) |
| Duration | `7m 57s` (`metadata.md`, field `DURATION`); no end time is inferred. |
| Timestamp source | Session metadata timestamp repeated in `security-assessment.md`; it is not treated as task start. |

## D. Prompt provenance

| Field | Value |
|---|---|
| Prompt filename | `pilot-output/prompt-used.md` |
| Prompt location | `C:\Users\cris\Downloads\set\ontap\pilot-evidence\penetration-tester\run-3\pilot-output\prompt-used.md` |
| Prompt SHA-256 | `1271d56183edc5e57ef11c61144baaaa0e4a47384011e21b1ae0c02bab856304` (calculated from this run's preserved file) |
| Prompt preserved verbatim | Yes; the preserved prompt matches the initial user prompt in `transcript.md` after line-ending normalization. |
| Prompt modifications during execution | None evidenced for the prompt file; the preserved prompt matches the recorded initial user prompt. |

## E. Output artifacts

| Artifact relative path | Description | Original preserved |
|---|---|---|
| `pilot-output/metadata.md` | Original short metadata record (model label, duration, credits). | Yes |
| `pilot-output/prompt-used.md` | Preserved execution prompt. | Yes |
| `pilot-output/security-assessment.md` | Primary static assessment artifact. | Yes |
| `pilot-output/transcript.md` | Partial conversation/tool record; it states that session-context export was truncated. | Yes |
| `pilot-output/git-status-short.txt` | Preserved status capture, `?? pilot-output/`. | Yes |
| `normalized-metadata.md` | Post-run normalization output created by this curation, not a pilot-produced artifact. | No — created during this curation |

## F. Transcript and evidence completeness

| Evidence item | Status | Details |
|---|---|---|
| Full conversation transcript | partial | `transcript.md` records activity but says `get_session_context` returned `truncated: true`; it is not a complete transcript. |
| Raw session export | missing | No raw session-export file is preserved in this run directory. |
| Tool-call evidence | partial | `transcript.md` contains selected tool calls/results, but its own limitation statement says complete transcript preservation was not achieved. |
| Prompt evidence | complete | Preserved prompt is present and matches the transcript's initial user prompt. |
| Final output artifact | complete | `pilot-output/security-assessment.md` is present. |
| Git status evidence | complete | The exact preserved status line is present; it reports the untracked output directory as a whole. |
| Metadata evidence | partial | Model/UI settings and session time are recorded, but commits, task times, and other settings are unavailable. |

## G. Commands and validation

The following describes the pilot execution evidence, not this later normalization.

| Command / operation | Purpose | Actual result | Evidence location |
|---|---|---|---|
| `$ErrorActionPreference = 'Stop'; ... Get-Date ...; git --no-pager status --short; ... Get-ChildItem pilot-output` | Capture current UTC time, status, and output listing. | Executed; command is recorded, but its complete output/exit code is not preserved in the transcript. The separately preserved status file reports `?? pilot-output/`. | `transcript.md`; `pilot-output/git-status-short.txt` |
| `git --no-pager status --short` (recorded twice) | Check worktree status. | Executed; preserved status file contains `?? pilot-output/`. Exit codes are not recorded. | `pilot-output/git-status-short.txt`; `transcript.md` |
| `session_store_sql` query filtered to `pilot-run/penetration-tester-3` | Look for a session record. | Executed; transcript records the query but does not preserve its result. | `transcript.md` |
| Static/dynamic tests, scans, payload execution, or network activity | Not applicable to the authorized documentation-only static assessment; no such validation is evidenced. | Not executed. | `security-assessment.md`; `transcript.md` |

## H. Repository scope and changes

| Field | Value |
|---|---|
| Final `git status --short` | `?? pilot-output/` |
| Scope boundary verified | Yes, with the limitation that Git reports the untracked directory as a whole and does not enumerate its contents. |
| Files changed | Pilot output files listed in section E; exact per-file status is not enumerated by the preserved Git output. |
| Files outside permitted output directory | None reported by the preserved status output. The newly created `normalized-metadata.md` is intentionally at the run root as required by this curation, not a pilot-execution change. |
| Scope deviations | None evidenced in the preserved status. No original evidence was changed by this normalization. |

## I. Interruptions, errors, and limitations

The transcript records two VS Code command-palette attempts interrupted by user input while seeking export/copy; the attempt was stopped. The transcript says session-context export was truncated and a complete transcript was not preserved. The status capture does not enumerate files inside the untracked directory. Task start/end times, branch, commits, temperature, and other settings are not recorded.

## J. Metadata confidence and unresolved fields

| Field name | Current value | Reason it cannot be established | Could additional original evidence resolve it? |
|---|---|---|---|
| Base repository commit | unknown | No commit identifier appears in the run evidence. | Yes, if the original run's commit record exists. |
| Scenario revision commit | unknown | No scenario commit identifier appears in the run evidence. | Yes, if the original run's revision record exists. |
| Skill revision commit | unknown | No skill commit identifier appears in the run evidence. | Yes, if the original run's revision record exists. |
| Working branch | unknown | No branch value is preserved in the run-local evidence. | Yes, if contemporaneous Git/session metadata exists. |
| Underlying model-serving provider | unknown | `Copilot Fusion` is a displayed provider label, not evidence of the underlying serving provider. | Yes, if original runtime metadata exists. |
| Task start and end times | unknown | Only a session metadata timestamp is recorded; no task-end timestamp exists. | Yes, if original task/session event timestamps exist. |
| Temperature and unlisted settings | unknown | No values are captured in the run evidence. | Yes, if a contemporaneous settings capture exists. |
| Exact file-level Git changes | partially supported | Git reports `?? pilot-output/` without listing its contents. | Yes, if the original full status/diff is available. |

## K. Additional recovery checks

- **Git/runtime metadata:** checked the run-local transcript, assessment, short metadata, and the named retained worktree. The worktree's current Git refs are not timestamped to execution and were not used to fill historical branch or commit fields. No additional contemporaneous task timestamp or settings capture was found; the recorded session-creation timestamp and visible settings remain as documented.
- **Additional execution timestamp:** `security-assessment.md` records a PowerShell status-check time of `2026-11-06T01:13:18.1008026Z`. This is a command timestamp, not a task-start or task-end time; those fields remain unknown.
- **Transcript limitation:** the preserved transcript still reports a truncated session-context export; no complete transcript or additional prompt/settings evidence was recovered.
