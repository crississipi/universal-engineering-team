# Validation and tests

## Install validation dependencies

Run these commands from the repository root:

```powershell
python -m pip install -r requirements-dev.txt
```

## Run repository validation

```powershell
python scripts/validate-skills.py
python scripts/validate-artifacts.py
python scripts/validate-handoffs.py
python scripts/validate-scenarios.py
python scripts/build-agents-section.py --check
```

## Run validator unit tests

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

The focused tests cover deterministic validator behavior, including valid
handoff contracts, malformed skill frontmatter, and synchronization between
the canonical blocker lifecycle specification and its JSON Schema. The same
unit-test command runs in the GitHub Actions validation workflow.

The blocker governance regression tests can also be run independently:

```powershell
python -m unittest discover -s tests -p "test_blocker_status_governance.py" -v
```

## Validator responsibilities

| Validator | Responsibility |
|---|---|
| `validate-skills.py` | Skill inventory, frontmatter, role index, manifest/source drift, and local Markdown links |
| `validate-artifacts.py` | Artifact package ownership |
| `validate-handoffs.py` | Formal handoff contract governance |
| `validate-scenarios.py` | Scenario and review-record structure |
| `build-agents-section.py --check` | Generated `AGENTS.md` section synchronization |

These validators check declared structure and consistency. They do not
replace independent technical review or prove subjective quality, evidence
sufficiency, or risk acceptance. Model-assisted evaluation remains separate
from ordinary structural CI.
