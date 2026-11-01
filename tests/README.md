# Evaluation and validation data

## Repository validation

Run the validation scripts from the repository root:

```powershell
python -m pip install -r requirements-dev.txt
python scripts/validate-skills.py
python scripts/validate-artifacts.py
python scripts/validate-handoffs.py
python scripts/validate-scenarios.py
python scripts/build-agents-section.py --check


## Handoff contract validation

The handoff validator checks formal contracts against:

- Canonical roles in `docs/team/expected-roles.yml`.
- Package ownership in `docs/team/ownership.yml`.
- Producer-consumer relationships in
  `docs/team/producer-consumer-matrix.md`.
- Contract rules in `docs/team/handoff-contract-schema.md`.

Run:

`python scripts/validate-handoffs.py`

An empty handoff list is valid during architecture setup. The validator
will report a warning rather than requiring speculative handoff records.

The validator checks declared structure and references. It does not
evaluate subjective technical judgments, evidence quality, or risk
acceptance decisions.

Run the focused validator unit tests:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

Keep the existing handoff contract validation content after that heading.

## 5. Validator and manifest decision

<badge color="info">No new validator or manifest required</badge>

For this phase, I recommend **not** creating a new workflow-state YAML manifest or validator.

Reasons:

- The repository has no approved machine-readable execution-record schema yet.
- The work-item state model is currently governance documentation, not executable configuration.
- A validator that merely searches Markdown for state names would not prove that transitions are followed correctly.
- Duplicating the state machine in YAML would create another source of truth that could drift from the documentation.

The existing validators remain appropriate for their current responsibilities:

| Validator | Responsibility |
|---|---|
| `validate-skills.py` | Role skill structure, frontmatter, and existing link checks |
| `validate-artifacts.py` | Artifact package ownership |
| `validate-handoffs.py` | Formal handoff contract governance |
| `validate-scenarios.py` | Scenario and review-record structure |
| `build-agents-section.py --check` | Generated `AGENTS.md` section synchronization |

We can introduce an automated workflow-state validator later, if the team adopts a structured execution-record format. That should be a deliberate architecture decision, not an assumption made during documentation consolidation.

## 6. Final consistency adjustments

A few existing sentences also need to use the new terminology consistently.

### A. `docs/team/workflow-lifecycle.md`

Make these targeted replacements:

| Existing wording | Replace with |
|---|---|
| `The relationship between workflow stages and task statuses.` | `The relationship between workflow stages, overall workflow status, and individual work-item states.` |
| `Workflow stages describe the progress of work; task statuses describe its current execution state.` | `Workflow stages describe the type of work being performed; overall workflow status describes the project or change condition; work-item states describe individual execution conditions.` |
| `Confirm the final work item status.` | `Confirm the final overall workflow status and the disposition of individual work items.` |

The second sentence appears in the governing principles section. The third appears in the Closure stage.

### B. `docs/team/workflow.md`

Under `## Change packet`, replace:

```markdown
- The relationship between workflow stages, overall workflow status, and individual work-item states.