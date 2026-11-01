
### C. `scripts/validate-skills.ps1`

Replace the complete contents with:

```powershell
$ErrorActionPreference = "Stop"

$checks = @(
    "validate-skills.py",
    "validate-artifacts.py",
    "validate-handoffs.py",
    "validate-scenarios.py"
)

foreach ($check in $checks) {
    Write-Host "`nRunning $check..." -ForegroundColor Cyan

    python (Join-Path $PSScriptRoot $check)

    if ($LASTEXITCODE -ne 0) {
        throw "Validation failed: $check"
    }
}

Write-Host "`nChecking generated AGENTS.md section..." -ForegroundColor Cyan

python (Join-Path $PSScriptRoot "build-agents-section.py") --check

if ($LASTEXITCODE -ne 0) {
    throw "Generated AGENTS.md section is out of sync."
}

Write-Host "`nGenerating skill size report..." -ForegroundColor Cyan

python (Join-Path $PSScriptRoot "measure-skill-tokens.py")

if ($LASTEXITCODE -ne 0) {
    throw "Skill size report failed."
}

Write-Host "`nAll repository governance checks passed." -ForegroundColor Green