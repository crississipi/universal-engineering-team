# Penetration Tester pilot — exact run prompt

Use this exact prompt in a fresh GitHub Copilot Agent conversation for each of the three independent runs.

---

Before producing anything, read:
- `skills/penetration-tester/SKILL.md`
- `tests/scenarios/SCEN-APPSEC-STATIC-WEBHOOK-REVIEW.yml`

You are being evaluated as **Penetration Tester**. Confirm that the scenario has `status: approved` and uses rubric `pilot-v2`. Follow the role skill and execute the scenario's `task_prompt` exactly. Do not modify the scenario, rubric, role skill, or any canonical repository file.

Execution constraints:
- This is a documentation-only static assessment of fictional code. Do not send network traffic, execute payloads, scan hosts, probe services, access a live target, or attempt exploitation.
- Use only the facts and code supplied by the scenario. Do not invent environment details or claim controls are absent when they are merely unknown.
- Create your assessment at `pilot-output/security-assessment.md`. Keep all new or modified files inside `pilot-output/`.
- Do not add unrelated files, tools, dependencies, or implementation code.
- Do not score yourself or recommend a pass/fail result.
- Report only checks actually performed. Do not claim dynamic validation, exploitability, or tool execution that did not occur.
- At completion, report the artifact path, a concise summary, the exact files changed, any commands/tools actually used and their actual results, assumptions, limitations, and any interruption. If no commands or tools were needed, say so.
- Do not use or refer to outputs from other pilot runs. Treat this as an independent first run.

Evidence capture:
- Preserve the complete Copilot conversation/transcript using the available export or copy mechanism; do not replace it with a summary.
- Preserve the final `pilot-output/` artifact files and the actual `git status --short` output showing the scope of changes.
- Do not manually edit or repair the output before preserving the original evidence.
- Record the actual provider, displayed model label, exact model/version if exposed, Agent mode, relevant settings, and UTC start time. If a value is unavailable, record `unknown`; never infer it.
