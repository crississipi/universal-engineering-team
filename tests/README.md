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