# Phase 0 implementation flags

## Confirmed repository facts

- The repository has 17 canonical role skill folders.
- `ROLE-INDEX.md` includes all 17 roles.
- `SKILLS-RESOLVER.md` already includes Delivery Lead routing.
- `AGENTS.md` already defines project discovery, collaboration, verification,
  anti-stuck behavior, and documentation expectations.
- The existing skill validator does not enforce a central expected-role manifest.
- `docs/team/ownership.md` does not currently include Delivery Lead.
- The current GitHub Actions workflow runs skill validation and the token report.

## Missing governance files

The following proposed files were not present when Phase 0 was inspected:

- `.skill-policy.yml`
- `docs/team/expected-roles.yml`
- `docs/team/ownership.yml`
- `docs/team/cross-cutting.md`
- `docs/team/evaluation-methodology.md`
- `scripts/inventory.py`
- `scripts/validate-artifacts.py`
- `scripts/validate-handoffs.py`
- `scripts/validate-scenarios.py`

## Decisions

1. Preserve all 17 specialist `SKILL.md` bodies in Phase 0.
2. Do not infer artifact ownership from free-form role descriptions.
3. Do not invent producer/consumer handoffs.
4. Keep the ownership manifest's artifact and handoff lists empty until evidence
   supports explicit entries.
5. Do not create fictional scenario fixtures or review records.
6. Do not claim that a pilot or baseline evaluation has been executed.
7. Keep provider compatibility claims limited to tested provider/version pairs.
8. Treat token measurements as method-specific and baseline-relative.
9. Keep model-assisted evaluation outside ordinary CI.

## Known inconsistency to correct

`docs/team/ownership.md` omits the Delivery Lead role even though the role is
present in `ROLE-INDEX.md`, `SKILLS-RESOLVER.md`, and `skills/delivery-lead/SKILL.md`.

Add the missing row without changing the existing role boundaries.

## Git baseline limitation

A GitHub repository checkout has Git metadata, but a downloaded source ZIP does
not. Generate the authoritative inventory from a clean local Git checkout after
the Phase 0 changes have been committed.

Do not substitute an archive hash or guessed commit identifier for a Git commit SHA.