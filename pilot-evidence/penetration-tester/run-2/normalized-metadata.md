# Normalized pilot run metadata

## A. Run identification

| Field | Value |
|---|---|
| Scenario ID | `SCEN-APPSEC-STATIC-WEBHOOK-REVIEW` |
| Role | Penetration Tester |
| Run number | 2 |
| Scenario status | `approved` (assessment and transcript) |
| Rubric version | `pilot-v2` (assessment and transcript) |
| Base repository commit | unknown |
| Scenario revision commit | unknown |
| Skill revision commit | unknown |
| Working branch | unknown |
| Worktree / workspace | `C:\Users\cris\Downloads\set\ontap\pilot-penetration-2` (path in transcript tool records) |

## B. Execution environment

| Field | Value |
|---|---|
| Provider | Copilot SDK in VS Code (runtime identity, per assessment); underlying model-serving provider unknown |
| Host / application | VS Code |
| Displayed model label | Conflicting: `metadata.md` records `GPT 6 LUNA`; `security-assessment.md` says the displayed model label is `unknown`. Unresolved. |
| Exact model identifier / version | unknown |
| Agent mode | unknown |
| Interaction mode | unknown |
| Model selection mode | unknown |
| Reasoning effort | unknown |
| Temperature | unknown |
| Permission mode | unknown |
| Other relevant settings | `metadata.md` records `CREDITS USED: 2.7` (usage metadata, not a setting); other settings unknown. |

## C. Execution timestamps

| Field | Value |
|---|---|
| Task start time (UTC) | `2026-11-06T00:57:27Z` (assessment says converted from the task message timestamp) |
| Task end time (UTC) | unknown |
| Session creation time (UTC) | unknown |
| Duration | `5m 22s` (`metadata.md`, field `DURATION`); no end time is inferred. |
| Timestamp source | Task message timestamp converted to UTC, as stated in `security-assessment.md`; separate session creation time is not preserved. |

## D. Prompt provenance

| Field | Value |
|---|---|
| Prompt filename | `pilot-output/prompt-used.md` |
| Prompt location | `C:\Users\cris\Downloads\set\ontap\pilot-evidence\penetration-tester\run-2\pilot-output\prompt-used.md` |
| Prompt SHA-256 | `1271d56183edc5e57ef11c61144baaaa0e4a47384011e21b1ae0c02bab856304` (calculated from this run's preserved file) |
| Prompt preserved verbatim | Yes; the preserved prompt matches the initial user prompt in `transcript.md` after line-ending normalization. |
| Prompt modifications during execution | None evidenced for the prompt file; the preserved prompt matches the recorded initial user prompt. |

## E. Output artifacts

| Artifact relative path | Description | Original preserved |
|---|---|---|
| `pilot-output/metadata.md` | Original short metadata record (model label, duration, credits). | Yes |
| `pilot-output/prompt-used.md` | Preserved execution prompt. | Yes |
| `pilot-output/security-assessment.md` | Primary static assessment artifact. | Yes |
| `pilot-output/transcript.md` | Partial conversation/tool record; it explicitly states complete transcript capture was not achieved. | Yes |
| `pilot-output/git-status-short.txt` | Preserved status capture; contains two identical `?? pilot-output/` lines. | Yes |
| `normalized-metadata.md` | Post-run normalization output created by this curation, not a pilot-produced artifact. | No — created during this curation |

## F. Transcript and evidence completeness

| Evidence item | Status | Details |
|---|---|---|
| Full conversation transcript | partial | `transcript.md` contains a conversation/tool record but explicitly says the complete transcript was not captured. |
| Raw session export | missing | No raw session-export file is present; transcript says no complete export/copy was available. |
| Tool-call evidence | partial | The markdown transcript records some calls/results, but is not a complete conversation export. |
| Prompt evidence | complete | Preserved prompt is present and matches the transcript's initial user prompt. |
| Final output artifact | complete | `pilot-output/security-assessment.md` is present. |
| Git status evidence | complete | The status file is preserved as written, including its duplicate status line. |
| Metadata evidence | partial | A short model/duration/credits record and assessment metadata exist, but displayed-model values conflict and settings are unavailable. |

## G. Commands and validation

The following describes the pilot execution evidence, not this later normalization.

| Command / operation | Purpose | Actual result | Evidence location |
|---|---|---|---|
| `git --no-pager status --short` | Check worktree before artifact creation. | Executed; transcript records the command but does not preserve its complete result or exit code. | `transcript.md` |
| `git status --short \| Tee-Object -FilePath 'pilot-output\git-status-short.txt'` (recorded twice) | Save status output. | Executed; preserved file has two identical lines, each `?? pilot-output/`. Exit code is not recorded. | `pilot-output/git-status-short.txt`; `transcript.md` |
| `Get-Content -Raw 'pilot-output\git-status-short.txt'` | Read saved status output. | Executed; transcript records the operation. | `transcript.md` |
| Read of the not-yet-existing `pilot-output` path | Locate output directory. | Executed and failed: `Path does not exist`. | `transcript.md` |
| Static/dynamic tests, scans, payload execution, or network activity | Not applicable to the authorized documentation-only static assessment; no such validation is evidenced. | Not executed. | `security-assessment.md`; `transcript.md` |

## H. Repository scope and changes

| Field | Value |
|---|---|
| Final `git status --short` | Preserved output: `?? pilot-output/` followed by a duplicate `?? pilot-output/`. |
| Scope boundary verified | Yes, with the limitation that Git reports the untracked directory as a whole and does not enumerate its contents. |
| Files changed | Pilot output files listed in section E; the preserved status does not enumerate individual files within the untracked directory. |
| Files outside permitted output directory | None reported by the preserved status output. The newly created `normalized-metadata.md` is intentionally at the run root as required by this curation, not a pilot-execution change. |
| Scope deviations | The status snapshot contains a duplicate line; no out-of-directory change is evidenced. No original evidence was changed by this normalization. |

## I. Interruptions, errors, and limitations

The transcript records a failed read because `pilot-output` did not yet exist. It says no interruption occurred. Transcript export/copy was unavailable, so the full conversation is not preserved. The assessment records the task-message timestamp but not session creation time. The short metadata model label conflicts with the assessment's `unknown` value. The transcript also records a request to fix all issues, but no real implementation path was provided and no code changes were made.

## J. Metadata confidence and unresolved fields

| Field name | Current value | Reason it cannot be established | Could additional original evidence resolve it? |
|---|---|---|---|
| Base repository commit | unknown | No commit identifier appears in the run evidence. | Yes, if the original run's commit record exists. |
| Scenario revision commit | unknown | No scenario commit identifier appears in the run evidence. | Yes, if the original run's revision record exists. |
| Skill revision commit | unknown | No skill commit identifier appears in the run evidence. | Yes, if the original run's revision record exists. |
| Working branch | unknown | No branch value is preserved. | Yes, if contemporaneous Git/session metadata exists. |
| Displayed model label | conflicting | `metadata.md` says `GPT 6 LUNA`; `security-assessment.md` says `unknown`. | Yes, if a contemporaneous UI capture exists. |
| Exact model identifier/version | unknown | No exact identifier/version is recorded. | Yes, if original runtime metadata exists. |
| Agent/interaction/model-selection modes and settings | unknown | No setting values are preserved. | Yes, if a contemporaneous settings capture exists. |
| Task end time and session creation time | unknown | Neither timestamp is recorded in the preserved evidence. | Yes, if original task/session event timestamps exist. |
| Exact command exit codes | not recorded | Transcript records commands but not reliable exit codes for the status captures. | Yes, if original terminal results exist. |
| Exact file-level Git changes | partially supported | Git reports the untracked directory as a whole, not its contents. | Yes, if the original full status/diff is available. |

## K. Additional recovery checks

- **Git/runtime metadata:** checked the run-local transcript, assessment, short metadata, and the named retained worktree. The worktree's current Git refs are not timestamped to execution and were not used to fill historical branch or commit fields. No further contemporaneous session timestamp or settings capture was found; the recorded task-start/duration data and displayed-model conflict remain as documented.
- **Scope:** the duplicate `?? pilot-output/` line in the original status capture was retained as-is; no evidence establishes additional file-level changes inside that untracked directory.
