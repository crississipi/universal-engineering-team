# Stage B baseline scenario second-pass design review

- Review date: 2026-11-08
- Reviewed branch: `chore/stage-b-repository-health`
- Reviewed baseline context: `f7d30d8f7fd868f7154fa08cfce1a36362ecf5ff`
- Scenario set: 17 role-specific drafts under `tests/scenarios/SCEN-BASELINE-*.yml`
- Review type: AI-assisted second-pass design audit against canonical repository sources
- Independent human reviewer: not performed
- Human pre-run approval: not performed
- Baseline execution: not started
- Decision: **Needs changes before any scenario is approved**

## 1. Review boundary and evidence

This review inspected all 17 scenario task prompts and rubrics, the corresponding 17 canonical role-skill identity/boundary sections, and these governance sources:

- `docs/team/expected-roles.yml`
- `docs/team/ownership.yml`
- `docs/team/role-activation-rules.md`
- `docs/team/producer-consumer-matrix.md`
- `docs/evaluation/baseline/README.md`
- `docs/evaluation/baseline/DESIGN-PREFLIGHT-2026-11-08.md`
- `scripts/validate-scenarios.py`

The 17 scenario files are present, use the canonical role IDs, have five criteria each, use the role's requirement anchor in each criterion, and have rubric weights totaling 100. Their execution boundaries consistently prohibit live network activity, production actions, invented approvals, and unsupported verification claims. The prompts generally respect the role ownership boundaries.

The user subsequently reported a local full-suite result of **65/65 unit tests passing** after pulling commit `0ff6f9c968404489f2e83cc062531f495ff1b4f7`, and the user reported that `validate-requirements.py`, `validate-scenarios.py` (0 warnings), and `git diff --check` passed. These are user-provided local results; this review did not execute the repository locally or independently reproduce them. The structural scenario validator does not check semantic completeness, artifact-package mapping, metric definitions, or criterion-specific scoring anchors.

This is a second-pass AI review, not an independent human review. It must not be counted as the independent human design review or human pre-run approval required by the baseline protocol. No scenario status or approval metadata was changed.

## 2. Overall assessment

### Strengths
- Role-specific deliverables are distinct and generally achievable in one agent session.
- Shared MerchantCloud-to-OrderDesk facts support useful cross-role comparability.
- Unknown infrastructure, provider retry behavior, SLOs, retention, permissions, and production authorization are consistently treated as unknown.
- Security and accessibility scenarios explicitly limit their methods and prohibit unsupported conformance or exploitability claims.
- The backend, database, API, and integration prompts recognize the difference between event identity and order identity.
- The Delivery Lead prompt explicitly requires task-specific activation and preservation of specialist authority.

### Approval blockers
- Artifact package identity is missing from the scenario records despite the prompts claiming it is supplied.
- The daily operational summary has no fully specified producer-to-support-view path.
- Timestamp and daily aggregation semantics are not aligned across roles.
- Duplicate delivery attempt auditability and duplicate-count semantics are not specified consistently.
- The backend rejection path lacks an explicit domain rule or injected policy boundary.
- Three inherited requirement anchors still need semantic review.

## 3. Required findings

### F-01 — Canonical artifact package IDs are not actually identified

- **Severity:** High
- **Affected:** All 17 scenario files
- **Evidence:** Each task prompt says that artifact IDs below identify the relevant proposed artifact package, but the scenario YAML contains no artifact-package field and the task prompt does not name an artifact ID. The only references are requirement IDs. The canonical owner manifest defines one package per role.
- **Why it matters:** The agent being evaluated cannot reliably identify the exact package it is producing, and a reviewer cannot mechanically or consistently trace the task output to the declared package owner. This weakens ownership-boundary scoring and makes the current prompt wording factually inaccurate.
- **Required change:** Add an explicit top-level `artifact_package` (or an equally unambiguous field) and state the package ID and accountable owner in each prompt. Keep package status explicitly `proposed`; do not imply approval or a formal handoff.
- **Canonical mapping:**

| Role | Required artifact package |
|---|---|
| product-analyst | `ART-PRODUCT-REQUIREMENTS` |
| solution-architect | `ART-ARCHITECTURE` |
| api-manager | `ART-API-CONTRACT` |
| backend-developer | `ART-BACKEND` |
| frontend-developer | `ART-FRONTEND` |
| ux-ui-designer | `ART-UX-DESIGN` |
| database-manager | `ART-DATA-MODEL` |
| integration-engineer | `ART-INTEGRATION` |
| data-engineer | `ART-DATA-PIPELINE` |
| qa-manager | `ART-QUALITY-EVIDENCE` |
| penetration-tester | `ART-SECURITY-ASSESSMENT` |
| devops-sre | `ART-OPERATIONS` |
| performance-engineer | `ART-PERFORMANCE-EVIDENCE` |
| accessibility-specialist | `ART-ACCESSIBILITY-ASSESSMENT` |
| technical-writer-knowledge-engineer | `ART-KNOWLEDGE-DOCS` |
| release-manager | `ART-RELEASE-PACKAGE` |
| delivery-lead | `ART-DELIVERY-RECORD` |

- **Owner:** Each corresponding artifact owner; Delivery Lead coordinates the cross-role correction.
- **Exit evidence:** All 17 scenario files identify exactly one existing package and its single canonical owner; validator or review checklist confirms every ID resolves in `ownership.yml`.

### F-02 — Daily operational summary is not connected to the UX/frontend deliverables

- **Severity:** High
- **Affected:** Product Analyst, Data Engineer, UX/UI Designer, Frontend Developer, Delivery Lead scenarios
- **Evidence:** The Product Analyst stakeholder notes require Operations to have a daily view of received, accepted, rejected, and duplicate event counts. The Data Engineer scenario designs a pipeline for a support-facing daily summary. The UX/UI scenario specifies the order investigation journey, while the Frontend scenario implements a recent-outcomes view; neither explicitly requires a daily summary or identifies its consumer.
- **Why it matters:** The scenarios may produce a daily aggregate that no in-scope support interface consumes, or a UI that omits a stated stakeholder need. The ownership and interface boundary between the aggregate and support view is not assessable.
- **Required change:** Product Analyst must state whether the daily summary is part of the first-release support experience and define its user-visible acceptance criteria. If included, UX/UI and Frontend must specify/design/render the summary and its loading, empty, error, and date-range behavior. Data Engineer should remain conditional unless the approved solution actually requires a separate pipeline; a simple application query may not require a separate pipeline. If the summary is delivered outside the UI, name that destination and its owner instead.
- **Owner:** Product Analyst for product meaning and scope; UX/UI Designer and Frontend Developer for experience/implementation; Data Engineer only if a pipeline trigger is confirmed.
- **Exit evidence:** One consistent, traceable producer/consumer path from approved product requirement to design, implementation, and any required aggregate.

### F-03 — Event occurrence time and receiver receipt time are conflated

- **Severity:** High
- **Affected:** Product Analyst, UX/UI Designer, Frontend Developer, Database Manager, Integration Engineer, Data Engineer, Technical Writer scenarios
- **Evidence:** The supplied event contains provider-supplied `occurred_at`. The Frontend task asks for a “received time”; the UX task asks for “event time”; the Data Engineer task needs daily grouping and late-arrival handling. The shared facts do not supply a receiver-side timestamp or define the daily grouping clock.
- **Why it matters:** `occurred_at` and the time OrderDesk received a delivery are different facts. Substituting one for the other can misstate delays, daily counts, late-arriving events, and support investigation timelines.
- **Required change:** Define distinct semantics for provider event occurrence time and receiver-observed receipt time. Require the ingress/persistence design to capture a receiver timestamp if it is a product requirement. Product Analyst must identify which timestamp governs daily grouping and delay definitions, or explicitly leave that decision open. UI fixtures must label synthetic timestamps as demonstration data and must not infer receipt time from `occurred_at`.
- **Owner:** Product Analyst for metric and user-facing meaning; Integration Engineer/Backend Developer for capture boundary; Database Manager for persistence model; Data Engineer for aggregation; UX/UI and Frontend for presentation.
- **Exit evidence:** Scenario prompts, data model, UI, and aggregation design use the same named timestamp fields and clearly identify unknowns.

### F-04 — Duplicate event identity is defined, but duplicate delivery-attempt evidence and counting are not

- **Severity:** High
- **Affected:** Product Analyst, Backend Developer, Database Manager, Integration Engineer, Data Engineer, QA Manager scenarios
- **Evidence:** The Backend task requires an event_id claim and a duplicate outcome. The Database task asks for duplicate delivery to be represented without losing auditability. The Integration task asks for duplicate handling. The Product Analyst and Data Engineer tasks require daily duplicate counts. The current Backend task does not explicitly require durable evidence of each repeated delivery attempt, while a unique event registry alone may retain only the first event.
- **Why it matters:** A system can correctly prevent duplicate order creation yet be unable to report how many duplicate delivery attempts occurred. “Duplicate count” could mean duplicate attempts, unique event IDs with a duplicate status, or duplicate business orders; those are not equivalent.
- **Required change:** Product Analyst must define the duplicate metric (for example, duplicate delivery attempts versus distinct events flagged duplicate). Integration and Database scenarios must distinguish a unique event from each delivery attempt and describe what evidence is retained. Backend must state whether it records the duplicate attempt or only returns a duplicate result, consistent with the approved contract and persistence design. QA must test both idempotent business behavior and the approved audit/counting behavior. Do not prescribe a particular table or schema in non-database roles.
- **Owner:** Product Analyst for metric definition; API Manager/Integration Engineer for delivery semantics; Database Manager for durable representation; Backend Developer for implementation; Data Engineer for aggregation; QA Manager for verification.
- **Exit evidence:** A single event/attempt model and duplicate-count definition used consistently across all affected scenarios.

### F-05 — Backend rejection path has no supplied domain rejection rule

- **Severity:** High
- **Affected:** Backend Developer scenario
- **Evidence:** The task requires the service to return a rejected domain-event outcome, but the input is described as already authenticated and validated/normalized and no business rule is supplied that makes a valid event domain-rejected.
- **Why it matters:** The agent may invent business policy to create a rejection test, violating the Product Analyst's ownership of domain requirements. Conversely, it may omit the rejection path and fail a rubric criterion that is not fully specified.
- **Required change:** Either supply an approved, deterministic domain rejection rule from Product Analyst, or make the domain decision an injected caller-supplied policy/validator whose result the service handles. The latter is preferable for this baseline: test that a supplied rejection result is propagated without the Backend Developer inventing the rule. State that the scenario does not evaluate the business policy itself.
- **Owner:** Product Analyst for any domain rejection rule; Backend Developer for the service boundary and behavior.
- **Exit evidence:** The rejection test has a deterministic input and expected outcome without an invented business rule.

### F-06 — Criterion descriptions lack criterion-specific score anchors

- **Severity:** Medium
- **Affected:** All 17 scenario rubrics
- **Evidence:** Each scenario provides five criterion descriptions, weights, and critical flags, plus generic overall score bands. It does not specify criterion-specific evidence examples or what materially incomplete, partial, core-meeting, and complete performance look like for each criterion.
- **Why it matters:** Two reviewers can apply the same broad 0–100 scale differently, reducing repeatability across 170 runs and across role-specific criteria.
- **Required change:** Add concise criterion-level evidence anchors (at minimum: absent/materially contrary, partial, core met, and complete/evidence-backed) or a shared rubric guidance section that gives observable examples for each criterion. Avoid requiring exact wording or rewarding verbosity.
- **Owner:** Baseline evaluation method owner / scenario author, with review by the relevant role owner and human evaluator.
- **Exit evidence:** Each criterion has observable scoring guidance; reviewers can distinguish score bands using deliverable evidence.

### F-07 — Three existing requirement anchors need semantic review before they are used as baseline measurement targets

- **Severity:** High
- **Affected:** Backend Developer, Penetration Tester, Delivery Lead scenarios
- **Evidence:** The canonical Backend anchor is framed as a purpose rather than an observable requirement; the Penetration Tester anchor says “Assess security risks…” but does not clearly state the evidence and limitation discipline that defines successful assessment; the Delivery Lead anchor describes coordination and accountability but is not phrased as a concise, measurable requirement. The author preflight already identified these three for semantic review.
- **Why it matters:** Every criterion in each affected scenario points to the same role-level anchor. A structurally valid anchor that is too broad or purpose-like weakens traceability and construct validity.
- **Required change:** Have the respective role/governance owner review and, if needed, refine the anchor into one concise observable requirement that reflects the full role boundary. Update the baseline register and scenario reference only after the canonical anchor is agreed. Do not rewrite the anchors merely to satisfy a validator.
- **Owner:** Backend Developer, Penetration Tester, and Delivery Lead role owners respectively; governance owner coordinates stable IDs and register updates.
- **Exit evidence:** Written semantic review disposition for all three anchors; any approved changes are reflected consistently in skill, register, and scenario.

### F-08 — Delayed-event handling is requested without an explicit measurement threshold

- **Severity:** Medium
- **Affected:** Product Analyst, UX/UI Designer, QA Manager, Data Engineer scenarios
- **Evidence:** Product and UX tasks require missing/delayed/not-yet-visible journeys, but the provider retry schedule and numerical latency/availability targets are explicitly unknown.
- **Why it matters:** A candidate could invent a delay threshold or be scored inconsistently for not doing so.
- **Required change:** State explicitly that the candidate must describe the delayed/not-yet-visible state and identify the decision needed, but must not define a numeric threshold unless it is labeled as a proposal requiring owner confirmation. QA must mark threshold-dependent assertions blocked or not yet testable.
- **Owner:** Product Analyst for the user-facing definition and decision routing; Operations/provider owners for evidence needed to set a threshold.
- **Exit evidence:** No scenario rubric rewards an invented delay SLA; the unresolved threshold is visible as an open decision.

## 4. Role-by-role review disposition

The following table is a design disposition, not approval. “No role-specific blocker found” means only that the task boundary and requested deliverable appear appropriate from the inspected prompt and role identity; it is not a score or approval.

| Role | Scenario | Review disposition |
|---|---|---|
| Product Analyst | `SCEN-BASELINE-PRODUCT-ANALYST` | **Revise:** F-02, F-03, F-04, F-08. Explicitly define the daily-summary requirement, metric decisions, and event-versus-receipt timestamps while preserving open decisions. |
| Solution Architect | `SCEN-BASELINE-SOLUTION-ARCHITECT` | No role-specific blocker found. Preserve neutral comparison of synchronous durable write and durable queue acceptance; do not assume a queue exists. Add package mapping per F-01. |
| API Manager | `SCEN-BASELINE-API-MANAGER` | No role-specific blocker found. Raw-body HMAC and retry uncertainty are appropriately bounded. Clarify receipt/attempt metadata and duplicate contract semantics under F-03/F-04; add package mapping. |
| Backend Developer | `SCEN-BASELINE-BACKEND-DEVELOPER` | **Revise:** F-04 and F-05. Keep atomic persistence as a repository contract, not a claim that a fake repository proves production concurrency. Add package mapping. |
| Frontend Developer | `SCEN-BASELINE-FRONTEND-DEVELOPER` | **Revise:** F-02 and F-03. Specify whether daily metrics are displayed and label receipt-time fixtures as synthetic; do not derive receipt time from `occurred_at`. |
| UX/UI Designer | `SCEN-BASELINE-UX-UI-DESIGNER` | **Revise:** F-02, F-03, F-08. Include daily summary design if in first-release scope; distinguish event time from receipt time and leave delay threshold open. |
| Database Manager | `SCEN-BASELINE-DATABASE-MANAGER` | **Revise:** F-03 and F-04. Make receipt timestamp and delivery-attempt audit model explicit as design questions/requirements; retain engine-neutral DDL and migration caveats. |
| Integration Engineer | `SCEN-BASELINE-INTEGRATION-ENGINEER` | **Revise:** F-03 and F-04. Separate provider event identity from delivery attempts, record receipt-time semantics, and keep retry policy unknown. |
| Data Engineer | `SCEN-BASELINE-DATA-ENGINEER` | **Revise:** F-02, F-03, F-04. Define the proposed source contract, grouping timestamp, and duplicate metric; do not assume a pipeline is required until its trigger is confirmed. |
| QA Manager | `SCEN-BASELINE-QA-MANAGER` | **Revise:** F-02, F-04, F-08. Add coverage for the agreed duplicate audit/count model and daily-summary consumer; keep unknown permissions and delay thresholds blocked pending decisions. |
| Penetration Tester | `SCEN-BASELINE-PENETRATION-TESTER` | No role-specific blocker found. Static-only scope and limits are clear. Complete anchor review under F-07 and add package mapping. |
| DevOps/SRE | `SCEN-BASELINE-DEVOPS-SRE` | No role-specific blocker found. Implementation-neutral operational design and explicit no-deployment boundary are appropriate. Add package mapping. |
| Performance Engineer | `SCEN-BASELINE-PERFORMANCE-ENGINEER` | No role-specific blocker found. Workload profiles are expressly illustrative and no benchmarks are claimed. Add package mapping. |
| Accessibility Specialist | `SCEN-BASELINE-ACCESSIBILITY-SPECIALIST` | No role-specific blocker found. Static markup, evidence limits, and retest planning are clear. Add package mapping. |
| Technical Writer / Knowledge Engineer | `SCEN-BASELINE-TECHNICAL-WRITER-KNOWLEDGE-ENGINEER` | No role-specific blocker found. Source traceability and unknowns are explicit. Align timestamp/status terminology after F-02–F-04 are resolved; add package mapping. |
| Release Manager | `SCEN-BASELINE-RELEASE-MANAGER` | No role-specific blocker found. Missing release evidence and no-go discipline are clear. Add package mapping. |
| Delivery Lead | `SCEN-BASELINE-DELIVERY-LEAD` | **Revise:** F-02–F-04 and F-07. The activation matrix must not assume Data Engineer, Performance Engineer, Release Manager, or other conditional roles are automatically active; state each trigger and whether it is met. Add package mapping. |

## 5. Required cross-scenario decisions and owner routing

Before scenario revisions are finalized, resolve these in the canonical Product/Architecture/API/Data/UX sources rather than inventing answers in individual prompts:

1. **Daily summary:** Is it first-release scope? What exactly is counted, and where is it displayed? Product Analyst owns the product definition; Data Engineer only designs a pipeline if the data-processing trigger is confirmed.
2. **Time semantics:** What is `occurred_at` versus receiver `received_at`? Which timestamp governs the daily summary and any delay indication? Product Analyst owns the metric definition; integration/backend/database roles own their respective technical capture and storage designs.
3. **Duplicate semantics:** Is the daily duplicate count a count of repeated delivery attempts, unique event IDs marked duplicate, or something else? Product Analyst owns the definition; API/Integration and Database own contract and persistence designs.
4. **Domain rejection:** What approved condition can cause a syntactically valid event to be rejected by domain policy? Product Analyst owns the rule; Backend owns only its implementation boundary.
5. **Delay threshold:** What evidence and owner decision are required before a delay can be classified operationally? Do not infer the provider retry schedule or a latency target.
6. **Requirement anchors:** What are the role-owner dispositions for the existing Backend, Penetration Tester, and Delivery Lead anchors?

These decisions may remain open if the scenarios explicitly preserve them as unknowns and the rubrics do not score candidates for inventing them. The goal is not to force premature product or technical decisions.

## 6. Review gate status

| Gate | Status |
|---|---|
| 17 canonical role IDs present | Structurally confirmed in scenario set |
| 17 scenario drafts present | Confirmed by repository register and file inspection |
| Five criteria per scenario | Confirmed by inspection |
| Rubric weights total 100 | Confirmed by inspection; local validator reported pass by user |
| Requirement reference structurally mapped | Local validator reported pass by user; semantic fit still open for three anchors |
| Role identity/boundary second-pass inspection | Completed by this AI-assisted review |
| Canonical artifact package mapping | **Needs changes** |
| Cross-scenario daily-summary path | **Needs changes** |
| Timestamp semantics | **Needs changes** |
| Duplicate audit/count semantics | **Needs changes** |
| Backend domain rejection policy boundary | **Needs changes** |
| Criterion-specific scoring anchors | Improvement required before controlled scoring |
| Independent human design review | Not performed |
| Human pre-run approval | Not performed; 0/17 |
| Execution configuration pinning | Not performed |
| Baseline run-record/reporting tooling | Not complete |
| Baseline executions | 0/170 |

## 7. Approval recommendation

**Do not approve any of the 17 scenarios yet.** Resolve F-01 through F-05 and F-07 before seeking human pre-run approval. Resolve F-06 and F-08 before running a controlled cohort so scoring and delay-related judgments remain repeatable.

After the corrections:
1. Run all local validators and the full unit suite.
2. Have a reviewer independent of the scenario author inspect the revised 17 drafts against the canonical role skills and governance.
3. Record the independent design review separately from human pre-run approval.
4. Obtain explicit human approval for each scenario individually.
5. Complete baseline-specific run-record/reporting tooling and pin the execution cohort.
6. Only then begin the 10 independent runs per approved scenario.

This review creates no approval, no run record, no formal handoff, and no evidence that any baseline execution occurred.


## 8. Remediation progress — 2026-11-08

The following design corrections have now been applied to the 17 draft scenario files on the Stage B branch. These are author-side scenario revisions, not stakeholder decisions, independent review, or approval.

| Finding | Scenario correction applied | Remaining qualification |
|---|---|---|
| F-01 — artifact mapping | Every baseline YAML now declares its canonical `artifact_package` and `artifact_owner`; the prompt repeats the package identity and preserves proposed/not-approved status. The scenario validator now checks package existence, owner match, and role-owner alignment. | Ownership records remain proposed; no formal handoff contracts were created. |
| F-02 — daily summary consumer | Product scope, UX design, frontend demonstration, data-engineering source contract, and QA coverage now explicitly include the support/operations daily summary. The Data Engineer task must justify a pipeline rather than assume one. Received attempts may exceed terminal outcome subtotals while work is in flight. | Product/Operations must confirm the proposed metric contract and final consumer/implementation path. |
| F-03 — timestamp semantics | Prompts distinguish provider `occurred_at` from receiver-generated `received_at`; UX/frontend must label them separately and data aggregation uses receipt time as the proposal. | Reporting timezone/day boundary and operational meaning require Product/Operations confirmation. |
| F-04 — duplicate audit/count semantics | Prompts distinguish `delivery_attempt_id`, `event_id`, and `order_id`; repeated attempts remain auditable, while event-level idempotency prevents duplicate business processing. The proposed summary counts attempts, not unique events or orders. A repeat is a duplicate only after a durable terminal event outcome exists; a transient/nonterminal failure is not mislabeled duplicate. | Product/Operations must confirm the proposed metric. Product must decide the domain rule for distinct event IDs referencing one order ID. |
| F-05 — backend rejection policy | Backend scenario now requires an injected caller-supplied domain-policy decision and tests both policy outcomes; the Backend role must not invent the business rule. | Product must supply/approve any actual domain rejection rule before implementation. |
| F-06 — criterion scoring | All 85 baseline criteria now contain four explicit score anchors: absent, partial, core, and complete. The scenario validator checks that each baseline criterion supplies all four non-empty anchors. | Human evaluators must review the anchors for role-specific fairness and apply them consistently. |
| F-07 — requirement anchor semantics | Backend, Penetration Tester, and Delivery Lead identity sections now state concise observable requirement anchors. Their baseline evidence pins were updated to the revised skill commits, and `ALL-ROLE-SKILLS.md` was synchronized with the source text. | Role/governance owners and an independent human reviewer must confirm semantic fit. Stable requirement IDs were retained. |
| F-08 — delayed-event threshold | Product, UX, frontend, and QA prompts prohibit invented numeric delay thresholds and use a neutral not-yet-visible state; threshold-dependent tests remain blocked pending owner input. | Product/Operations must decide whether a threshold is needed and define it from evidence. |

### Additional structural validation

`scripts/validate-scenarios.py` now validates baseline artifact-package/owner mapping and the four criterion-level score anchors. Its unit tests include mismatched-owner and missing-score-anchor regressions. The full test suite and local validators have **not yet been rerun against this latest remediation commit series**; the earlier user-reported 65/65 result predates these changes.

### Updated gate disposition

- Scenario author-side corrections: applied to all 17 drafts for F-01 and F-06; cross-role prompt changes applied for F-02 through F-05 and F-08; three role requirement anchors refined for F-07.
- Stakeholder decisions still open: reporting timezone, precise inclusion boundary for business-event counts versus invalid ingress telemetry, confirmation of attempt-level metric semantics, same-order/multiple-event domain policy, and any delay threshold.
- Independent human design review: not performed (0/17).
- Human pre-run approval: not performed (0/17).
- Baseline executions: 0/170.

**Recommendation:** Treat the current scenario set as revised drafts ready for local validation and then independent human review, not as approved scenarios. Do not begin baseline execution until the remaining stakeholder decisions are either confirmed or explicitly retained as non-scored open decisions, human review is recorded, individual pre-run approvals are obtained, and execution-readiness tooling is complete.
