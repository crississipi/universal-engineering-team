# Reproducible baseline pin preparation

This procedure derives candidate scenario, role-skill, and prompt pins from Git
history. It does not modify `cohorts.yml`, approve scenarios, resolve
stakeholder decisions, or authorize baseline execution.

## Preconditions

1. Work in a complete local clone of this repository with the relevant commit
   history available (not a shallow clone missing path history).
2. Check out the intended repository state and inspect the commit you intend to
   use as the cohort base.
3. Obtain explicit agreement on that base commit. Do not use a moving branch
   name as the recorded pin.
4. Do not use this procedure to imply that draft scenarios are approved.

## Generate candidate pins

From the repository root, run:

```powershell
python scripts/prepare-baseline-pins.py --base-commit <FULL_40_CHARACTER_COMMIT_SHA>
```

For machine-readable output:

```powershell
python scripts/prepare-baseline-pins.py --base-commit <FULL_40_CHARACTER_COMMIT_SHA> --format json
```

The script reads the canonical role inventory and, for each of the 17 roles:

- Finds the latest commit changing that role's scenario file, reachable from
  the selected base commit.
- Finds the latest commit changing that role's canonical `SKILL.md`, reachable
  from the selected base commit.
- Reads the scenario file from its selected scenario commit, parses its YAML,
  and computes SHA-256 over the UTF-8 bytes of the parsed `task_prompt` string.
- Verifies the scenario ID/role and that the pinned skill file is non-empty.

It emits a candidate `repository_base_commit` and the complete
`scenario_pins` list. Review the output and copy only the corresponding pin
values into `cohorts.yml` as a separate, deliberate change. The tool never
writes the cohort register automatically.

## Interpretation and limitations

- The scenario and skill commits are file-history pins, not a claim that the
  entire repository was unchanged at those revisions.
- The prompt hash represents the parsed YAML string value. YAML block-scalar
  syntax is therefore interpreted by the YAML parser before hashing. It is not
  a hash of the source file's raw bytes.
- The selected base commit must be an explicit, agreed commit. The script does
  not decide which base commit is appropriate.
- The script requires local Git history and fails if any path has no reachable
  change commit.
- This process does not record provider, model, model version, agent mode,
  temperature, reasoning effort, tool permissions, operating environment, or
  other material runtime settings. Those must be observed and recorded
  separately; unknown values remain blockers.
- Git-derived pins do not establish scenario approval, stakeholder decision
  resolution, actual runtime identity, isolation, comparability, or execution
  authorization.

After reviewing and recording candidate pins, run:

```powershell
python scripts/check-baseline-cohort.py
python scripts/check-baseline-governance.py
```

A clear cohort pin check is not execution authorization. The governance
checker and all human approval gates remain separate. No baseline run may
begin until every applicable gate is explicitly satisfied.
