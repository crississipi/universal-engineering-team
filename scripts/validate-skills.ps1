$ErrorActionPreference = "Stop"
python (Join-Path $PSScriptRoot "validate-skills.py")
if ($LASTEXITCODE -ne 0) { throw "Skill validation failed." }
python (Join-Path $PSScriptRoot "measure-skill-tokens.py")
if ($LASTEXITCODE -ne 0) { throw "Skill size report failed." }
