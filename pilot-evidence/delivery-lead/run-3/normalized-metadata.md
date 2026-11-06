# Normalized pilot run metadata

## A. Run identification

| Field | Value |
|---|---|
| Scenario ID | `SCEN-DELIVERY-CROSSROLE-WEBHOOK` |
| Role | Delivery Lead |
| Run number | 3 |
| Scenario status | `approved` |
| Rubric version | `pilot-v2` |
| Base repository commit | unknown |
| Scenario revision commit | unknown |
| Skill revision commit | unknown |
| Working branch | `pilot-run/delivery-lead-3` (`run-metadata.md`, `get_current_session` result) |
| Worktree / workspace | Workspace `pilot-delivery-3`; recorded worktree path `C:\Users\cris\Downloads\set\ontap\pilot-delivery-3`. |

## B. Execution environment

| Field | Value |
|---|---|
| Provider | Copilot SDK in VS Code (runtime identity); underlying model-serving provider unknown |
| Host / application | VS Code |
| Displayed model label | Unknown; `run-metadata.md` says no label was exposed. |
| Exact model identifier / version | unknown |
| Agent mode | unknown |
| Interaction mode | unknown |
| Model selection mode | unknown |
| Reasoning effort | unknown |
| Temperature | unknown |
| Permission mode | unknown |
| Other relevant settings | No settings were available through the session metadata, per `run-metadata.md`. |

## C. Execution timestamps

| Field | Value |
|---|---|
| Task start time (UTC) | `2026-11-06T02:19:07.726Z` (converted from the user-supplied `2026-11-06T10:19:07.726+08:00`) |
| Task end time (UTC) | unknown |
| Session creation time (UTC) | `2026-11-06T02:17:26.283Z` (`get_current_session`) |
| Duration | unknown |
| Timestamp source | `run-metadata.md` distinguishes the task-message timestamp from `get_current_session` creation time; they are retained separately. |

## D. Prompt provenance

| Field | Value |
|---|---|
| Prompt filename | Exact prompt remains missing. A candidate `pilot-output/prompt-used.md` was found in the retained run worktree and copied to `candidate-prompt-used-unverified.md`; it is not accepted as the exact submitted prompt. |
| Prompt location | Candidate source: `C:\Users\cris\Downloads\set\ontap\pilot-delivery-3\pilot-output\prompt-used.md`; evidence copy: `candidate-prompt-used-unverified.md`. |
| Prompt SHA-256 | unknown for the exact submitted prompt; candidate file SHA-256 `e27f4b503da09fa38958242333c6cce804d5a9b868d6b3fb4e009d41cf037d29`. |
| Prompt preserved verbatim | The candidate was copied byte-for-byte from the retained run-worktree artifact, but it does not match the approved source file: it omits the title/intro/separator and has no final line terminator. The truncated transcript prevents confirming that it is the submitted prompt. |
| Prompt modifications during execution | The preserved final status lists only `?? pilot-output/`; the tracked source prompt is unchanged in the retained worktree. The candidate artifact differs from that source, but whether it was the exact prompt used is unknown. |

## E. Output artifacts

| Artifact relative path | Description | Original preserved |
|---|---|---|
| `pilot-output/delivery-plan.md` | Primary proposed delivery plan; not an execution record. | Yes |
| `pilot-output/git-status-short.txt` | Preserved final status output, `?? pilot-output/`. | Yes |
| `pilot-output/run-metadata.md` | Detailed run record, settings/timestamps, transcript limitations, commands, and errors. | Yes |
| `pilot-output/transcript-session-export-20261106T021907Z.json` | Earlier truncated raw session-context export. | Yes |
| `pilot-output/transcript-session-export-latest.json` | Later truncated raw session-context export; contains more tool-call entries than the earlier snapshot. | Yes |
| `candidate-prompt-used-unverified.md` | Byte-for-byte copy of the prompt candidate found in the retained run worktree; not verified as the exact submitted prompt. | Recovered candidate; not treated as the run prompt |
| `normalized-metadata.md` | Post-run normalization output created by this curation, not a pilot-produced artifact. | No — created during this curation |

## F. Transcript and evidence completeness

| Evidence item | Status | Details |
|---|---|---|
| Full conversation transcript | partial | Both session-context snapshots report `truncated: true`; the user message is truncated and neither is a complete transcript. |
| Raw session export | partial | Two raw session-context snapshots are preserved, but both are truncated. |
| Tool-call evidence | partial | Exports preserve tool-call entries (68 and 97 respectively) but not a complete verbatim record of tool results. |
| Prompt evidence | partial | A run-worktree candidate was recovered, but it omits the approved source's title/intro/separator and its exact relationship to the submitted prompt cannot be confirmed from the truncated user message. |
| Final output artifact | complete | `pilot-output/delivery-plan.md` is present. |
| Git status evidence | complete | The exact preserved status line is present; it reports the untracked output directory as a whole. |
| Metadata evidence | partial | Run metadata records scenario, runtime identity, task/session timestamps, branch/workspace, and limitations; many environment values remain unavailable. |

## G. Commands and validation

The following describes the pilot execution evidence, not this later normalization.

| Command / operation | Purpose | Actual result | Evidence location |
|---|---|---|---|
| `get_current_session` | Capture current session context. | Returned session creation `2026-11-06T02:17:26.283Z`, workspace `pilot-delivery-3`, branch `pilot-run/delivery-lead-3`, and zero pre-existing worktree changes at that observation. | `run-metadata.md` |
| `get_session_context` with `detail=full`, `transcriptLimit=1` | Preserve session evidence. | Two exports were saved (17,186 and 24,428 bytes); JSON parsing succeeded; both report `truncated: true`, `hasMoreHistory: false`; tool-call counts were 68 and 97. | `run-metadata.md`; both `transcript-session-export-*.json` files |
| PowerShell copy of initial/latest session exports | Preserve raw exports. | Run record states copies completed with exit code 0 and the stated byte lengths. | `run-metadata.md` |
| PowerShell output-target check | Check expected output targets before creation. | Run record says `delivery-plan.md`, `run-metadata.md`, and `git-status-short.txt` did not exist before creation. | `run-metadata.md` |
| Targeted PowerShell plan-content check | Check plan against role/ownership/scenario requirements. | Run record states 17 canonical roles/rows, no missing or extra roles, no invalid classifications, all 16 referenced artifact IDs exist, and scenario/rubric check returned `True`. | `run-metadata.md` |
| `github-mcp-server-get_copilot_space` without owner | Attempt Copilot Space lookup. | Executed and failed: `missing required parameter: owner`; no Copilot Space content was returned or used. | `run-metadata.md`; session export |
| `session_store_sql` queries by session ID | Look for session record in cloud/local stores. | Run record states both queries returned 0 rows. | `run-metadata.md` |
| `git status --short` | Capture final working-tree scope. | Executed; exit code 0; output `?? pilot-output/`. | `pilot-output/git-status-short.txt`; `run-metadata.md` |
| Tests, builds, linters, validators, and application checks | Planning-only task; no application implementation. | Not executed. | `run-metadata.md` |

## H. Repository scope and changes

| Field | Value |
|---|---|
| Final `git status --short` | `?? pilot-output/` |
| Scope boundary verified | Yes, with the limitation that Git reports the untracked directory as a whole and does not enumerate its contents. |
| Files changed | Pilot output files listed in section E; preserved status does not enumerate individual files. |
| Files outside permitted output directory | None reported by the preserved final status. The newly created `normalized-metadata.md` is intentionally at the run root as required by this curation, not a pilot-execution change. |
| Scope deviations | None evidenced by the captured final status. Earlier session observation reported zero pre-existing changes. This normalization did not modify original evidence. |

## I. Interruptions, errors, and limitations

Three attempts to use the VS Code export/copy UI were interrupted by detected user input; the run record says no further UI action was taken. Both raw session-context exports are truncated and do not provide a complete transcript. A Copilot Space lookup failed because the required owner parameter was absent. The recovered candidate prompt does not match the approved source file, and the transcript's 1,000-character user field is truncated; the exact prompt remains missing. Task end time, duration, exact model, agent mode, settings, and commit identifiers are not available.

## J. Metadata confidence and unresolved fields

| Field name | Current value | Reason it cannot be established | Could additional original evidence resolve it? |
|---|---|---|---|
| Base repository commit | unknown | No commit identifier appears in preserved run evidence. | Yes, if the original run's commit record exists. |
| Scenario revision commit | unknown | No scenario commit identifier appears in preserved run evidence. | Yes, if the original run's revision record exists. |
| Skill revision commit | unknown | No skill commit identifier appears in preserved run evidence. | Yes, if the original run's revision record exists. |
| Displayed model and exact model/version | unknown | Metadata says no label was exposed; no exact model identifier is present. | Yes, if original runtime/UI metadata exists. |
| Agent mode and settings | unknown | Run metadata says settings were unavailable. | Yes, if a contemporaneous settings capture exists. |
| Task end time and duration | unknown | No end timestamp or duration is recorded. | Yes, if original task/session timing metadata exists. |
| Exact prompt file and SHA-256 | missing/unknown | A run-worktree candidate exists, but it is not identical to the approved prompt source and cannot be verified against the truncated user message. | A complete original user-message capture or a verified prompt copy could resolve it. |
| Candidate prompt identity | unverified | Candidate SHA-256 and source comparison are documented in section K; its title/intro/separator are absent. | A complete original chat capture could establish whether the candidate is the prompt actually submitted. |
| Exact file-level Git changes | partially supported | `?? pilot-output/` does not enumerate its contents. | Yes, if the original complete status/diff is available. |
| Full transcript/tool results | partial | Both exports are explicitly truncated; the user field and tool results are incomplete. | Yes, if a complete original chat export exists. |

## K. Additional recovery checks

- **Candidate recovery:** found `pilot-output/prompt-used.md` in the retained `pilot-delivery-3` worktree and copied it byte-for-byte to `candidate-prompt-used-unverified.md` (2,615 bytes; SHA-256 `e27f4b503da09fa38958242333c6cce804d5a9b868d6b3fb4e009d41cf037d29`). The source `evaluations/pilot/evidence/SCEN-DELIVERY-CROSSROLE-WEBHOOK/prompt-used.md` matches its checked-out Git source after line-ending normalization, while the candidate omits the source's title/intro/separator and final line terminator.
- **Identity check:** both preserved session exports mark the user field truncated at 1,000 characters. Its visible prefix is consistent with the candidate, but it does not establish the remaining text. Accordingly, the exact prompt status remains missing; the candidate is not substituted for it.
- **Other metadata:** the contemporaneous `get_current_session` record supports the already-recorded branch and session-creation time; the task-message record supports the already-recorded task-start time. No original commit ID or additional settings were found. Current worktree refs/settings were not used as historical values.
