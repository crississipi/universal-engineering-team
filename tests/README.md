# Validation and tests

## Install validation dependencies

Run these commands from the repository root:

```powershell
python -m pip install -r requirements-dev.txt
```

## Run repository validation

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate-execution.py --check-schemas
python scripts/validate-skills.py
python scripts/validate-manifest.py
python scripts/validate-artifacts.py
python scripts/validate-handoffs.py
python scripts/validate-scenarios.py
python scripts/build-agents-section.py --check
```

The unit tests cover deterministic validator behavior, including manifest
declarations, handoff contracts, malformed skill frontmatter, blocker
lifecycle synchronization, integrated execution-validation orchestration,
and resolver alignment with canonical role-activation triggers.
The same unit-test command runs in GitHub Actions.

The execution schema check meta-validates all ten record schemas and their
shared definitions without requiring a populated execution directory. To
validate a specific execution end to end, run:

```powershell
python scripts/validate-execution.py "executions/EXE-<uuid>"
```

The integrated command parses all ten required YAML records, rejects duplicate
mapping keys, validates each record against its Draft 2020-12 schema, and only
then runs cross-record and lifecycle validation. A failed prerequisite causes
dependent checks to be reported as skipped, not passed.

The blocker governance regression tests can also be run independently:

```powershell
python -m unittest discover -s tests -p "test_blocker_status_governance.py" -v
```

## Validator responsibilities

| Validator | Responsibility |
|---|---|
| `validate-skills.py` | Skill inventory, frontmatter, role index, manifest/source projection drift, and local Markdown links |
| `validate-manifest.py` | Manifest schema, declaration references, relationship mirrors, handoff role/artifact ownership, and declaration uniqueness |
| `validate-artifacts.py` | Artifact package ownership |
| `validate-handoffs.py` | Formal handoff contract governance |
| `validate-scenarios.py` | Scenario and review-record structure |
| `validate-execution.py` | Integrated execution parsing, JSON Schema, cross-record, and lifecycle validation; `--check-schemas` validates schema documents without an execution fixture |
| `build-agents-section.py --check` | Generated `AGENTS.md` section synchronization |

The manifest validator complements the source-projection check in
`validate-skills.py`; it does not replace that check or make the manifest
a new source of truth. Canonical roles, artifact ownership, relationships,
and formal handoffs remain in their existing governance files.

These validators check declared structure and consistency. They do not
replace independent technical review or prove subjective quality, evidence
sufficiency, or risk acceptance. Model-assisted evaluation remains separate
from ordinary structural CI.
