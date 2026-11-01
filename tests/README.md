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
