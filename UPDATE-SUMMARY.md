# Update package — change summary

## Compatibility and correctness
- Preserved the existing 16 specialist roles and each role's technical ownership, workflow, collaboration, deliverables, and guardrails.
- Retained standard Agent Skills `name` and `description` frontmatter keys.
- Shortened descriptions while retaining role domains and activation terms.
- Added concise provider-neutral operating contracts to all 16 role skills.
- Corrected role-index links to the actual `skills/<role>/SKILL.md` layout.
- Updated README installation guidance without claiming universal provider auto-loading.

## Routing and governance
- Added `SKILLS-RESOLVER.md` as an advisory task-to-role map.
- Updated `AGENTS.md` to reference the resolver and clarify cross-provider instruction loading.
- Kept core safety, anti-stuck, architecture, verification, and documentation rules in `AGENTS.md`; no critical rule was moved exclusively into optional references.

## Validation
- Added `scripts/validate-skills.py` for frontmatter, naming, index, and local Markdown link checks.
- Added `scripts/measure-skill-tokens.py` for approximate or `tiktoken`-based size reporting.
- Added `scripts/validate-skills.ps1` for Windows PowerShell.
- Added GitHub Actions validation on push and pull request.

## Deliberate non-changes
- No role was deleted, merged, or renamed. The task-lead responsibility remains an orchestration rule, not an extra specialist skill.
- No role-specific workflow or technical guardrail was removed.
- No universal provider installation path or CLI command is asserted.
- Token counts are not treated as a quality metric; correctness and discoverability take priority.

## Delivery Lead correction
- Added `skills/delivery-lead/SKILL.md` as the 17th role: a coordination role alongside the 16 specialist roles.
- Preserved the original Delivery Lead mission, ownership boundaries, workflow, anti-stuck protocol, handoff contract, and required closeout.
- Shortened only the Delivery Lead frontmatter description to meet the skill-description length target.
- Added Delivery Lead to `ROLE-INDEX.md`, `SKILLS-RESOLVER.md`, `ALL-ROLE-SKILLS.md`, and the README role count/list.
- Confirmed the role is intended for multi-step, cross-functional, or multi-system coordination; it does not replace specialist ownership.