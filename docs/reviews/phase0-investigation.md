# Phase 0 CI Investigation

## Scope

This record documents the GitHub Actions failure observed before Phase 0
changes. It deliberately distinguishes observed evidence from an unconfirmed
root cause.

## Repository baseline

- Repository: `crississipi/universal-engineering-team`
- Branch: `main`
- Baseline commit: `0f0224314c509e5bef1c12ec55712fb00f42b8ec`
- Workflow: `.github/workflows/validate-skills.yml`
- Workflow run: [Run #27](https://github.com/crississipi/universal-engineering-team/actions/runs/41468375675)
- Run ID: `41468375675`
- Job ID: `125355144615`
- Observed conclusion: `failure`

## Evidence observed on 2026-11-03

1. The latest ten workflow runs (#18 through #27) all reported
   `conclusion: failure`.
2. The latest run started at `2026-11-02T15:06:49Z` and completed at
   `2026-11-02T15:06:53Z`.
3. GitHub's job summary returned an empty `steps` array for the failed job.
4. The workflow-job log download returned HTTP 404 with
   `BlobNotFound`; usable runner output was not available through the
   connected GitHub interface.
5. The workflow definition contains checkout, Python setup, dependency
   installation, and validation steps, but the available run metadata does not
   identify which step failed.

## Diagnosis status

**Root cause not established.**

The available evidence is insufficient to attribute the failures to
`validate-skills.py`, another repository validator, dependency installation,
or GitHub runner provisioning. The short run duration and empty step list
suggest that failure may have occurred before step summaries were recorded,
but that is not proof of a runner-side failure.

Do not mark CI healthy or Phase 0 complete based on this investigation alone.

## Actions in this stabilization change

- Harden `parse_skill()` so malformed YAML and unreadable files produce
  controlled validation errors instead of uncaught exceptions.
- Add regression tests for valid, malformed, missing-closer, and
  non-mapping frontmatter.
- Repair the test README's unclosed code fence and remove editing residue.
- Add the unit-test command to the workflow so future runs expose test
  failures explicitly.

## Required follow-up

1. Inspect the annotations and runner diagnostics for Run #27 in GitHub Actions.
2. Re-run the failed workflow job or trigger the pull-request workflow.
3. Confirm that GitHub records actual step results.
4. If the workflow reaches repository commands, fix the first evidenced
   failing command and repeat until the complete workflow passes.

Phase 0 remains open until a complete validation workflow run succeeds.
