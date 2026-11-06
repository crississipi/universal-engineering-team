# Delivery Lead pilot — exact run prompt

Use this exact prompt in a fresh GitHub Copilot Agent conversation for each of the three independent runs.

---

Before producing anything, read:
- `skills/delivery-lead/SKILL.md`
- `tests/scenarios/SCEN-DELIVERY-CROSSROLE-WEBHOOK.yml`
- `docs/team/expected-roles.yml`
- `docs/team/ownership.yml`
- `docs/team/producer-consumer-matrix.md`
- `docs/team/execution-protocol.md`
- The lifecycle/status documentation referenced by the role skill and execution protocol.

You are being evaluated as **Delivery Lead**. Confirm that the scenario has `status: approved` and uses rubric `pilot-v2`. Follow the role skill and execute the scenario's `task_prompt` exactly. Do not modify the scenario, rubric, role skill, ownership rules, role inventory, lifecycle specifications, or any canonical repository file.

Execution constraints:
- This is a planning/orchestration exercise only. Do not implement the feature, change application code, execute real cross-role handoffs, create formal approvals, or deploy anything.
- Use the canonical 17-role inventory, artifact ownership, collaboration declarations, and lifecycle vocabulary exactly as written. Do not invent role IDs, artifact IDs, states, approvals, formal handoff contracts, or completed work.
- Keep proposed work clearly distinct from execution evidence. No implementation, verification, handoff, approval, release, or production deployment has occurred as part of this task.
- Create the delivery plan at `pilot-output/delivery-plan.md`. Keep all new or modified files inside `pilot-output/`.
- Do not add unrelated files, tools, dependencies, or implementation code.
- Do not score yourself or recommend a pass/fail result.
- Report only checks actually performed. Do not claim repository validation or other commands passed unless you ran them.
- At completion, report the artifact path, a concise summary, the exact files changed, the exact commands/tools actually used and their actual results, assumptions, limitations, and any interruption. If no commands or tools were needed, say so.
- Do not use or refer to outputs from other pilot runs. Treat this as an independent first run.

Evidence capture:
- Preserve the complete Copilot conversation/transcript using the available export or copy mechanism; do not replace it with a summary.
- Preserve the final `pilot-output/` artifact files and the actual `git status --short` output showing the scope of changes.
- Do not manually edit or repair the output before preserving the original evidence.
- Record the actual provider, displayed model label, exact model/version if exposed, Agent mode, relevant settings, and UTC start time. If a value is unavailable, record `unknown`; never infer it.

