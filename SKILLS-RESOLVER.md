# Skills Resolver

Use this guide to select the smallest sufficient set of specialist skills. It is a routing aid, not a replacement for repository discovery, the role ownership model, or specialist instructions.

## Routing rules

1. Identify the primary deliverable and activate its owning role.
2. Add supporting roles only when the task crosses their responsibility boundary or carries a material risk in that domain.
3. Evaluate QA Manager activation using the triggers in `docs/team/role-activation-rules.md`. Do not activate QA automatically for every change. Formal acceptance/regression evidence, multi-component verification, a QA release/delivery gate, or material quality risk requires QA participation. For a bounded change without those triggers, the accountable implementation owner still performs and records proportionate verification; QA may remain inactive.
4. Evaluate Technical Writer / Knowledge Engineer activation using the triggers in `docs/team/role-activation-rules.md`. Do not activate this role automatically for every change. Activate it when documentation/knowledge work is an explicit deliverable, a significant change requires specialist documentation, knowledge transfer is required, or an existing documentation/knowledge surface needs specialist maintenance. The accountable source owner still supplies accurate facts and completes documentation obligations assigned to that owner when the specialist is inactive.
5. Activate Solution Architect for multi-service, cross-platform, major refactor, or high-risk boundary decisions.
6. Activate Release Manager for production/shared-environment release coordination, not for ordinary local implementation.
7. The resolver never grants permission for destructive actions, production changes, credential access, or security testing beyond explicit authorization.
8. Activate Delivery Lead for multi-step, cross-functional, or multi-system work that needs coordinated ownership, sequencing, handoffs, blocker management, or integration oversight. For a small task owned by one specialist, that specialist can coordinate the task without activating a separate Delivery Lead.

## Task-to-role map

| Task or change | Primary role | Add supporting roles when relevant |
|---|---|---|
| New feature, unclear scope, user workflow | Product Analyst | UX/UI, Solution Architect, relevant implementation roles; QA when its verification triggers apply |
| System design, service boundaries, major refactor | Solution Architect | API, Integration, Database, Backend, Frontend, DevOps/SRE, Penetration Tester, QA when its triggers apply |
| API or event contract | API Manager | Backend, Frontend, Integration; Penetration Tester or QA when their triggers apply |
| Server-side behavior, jobs, business rules | Backend Developer | API, Database, Integration; Penetration Tester or QA when their triggers apply |
| Browser/mobile UI, client state | Frontend Developer | UX/UI, Accessibility, API; QA when its triggers apply |
| Interaction design, navigation, visual system | UX/UI Designer | Product Analyst, Frontend, Accessibility |
| Schema, migration, integrity, query | Database Manager | Backend, Data Engineer, DevOps/SRE; Penetration Tester or QA when their triggers apply |
| SaaS/partner integration, webhook, queue, event flow | Integration Engineer | Architect, API, Backend, Database, DevOps/SRE; Penetration Tester or QA when their triggers apply |
| ETL/ELT, ingestion, transformation, analytics pipeline | Data Engineer | Database, Integration, Penetration Tester, DevOps/SRE; QA when its triggers apply |
| Test strategy, regression, defect verification | QA Manager | Relevant implementation owner and specialist reviewers |
| Authentication, authorization, threat, dependency or trust-boundary risk | Penetration Tester | Architect, API, Backend, Frontend, DevOps/SRE; QA when its triggers apply |
| CI/CD, hosting, infrastructure, monitoring, recovery | DevOps / SRE | Architect, Backend, Database, Penetration Tester, Release when applicable |
| Measured latency, throughput, memory, scaling issue | Performance Engineer | Relevant implementation owner, Architect, DevOps/SRE; QA when its triggers apply |
| Accessibility audit or inclusive interaction change | Accessibility Specialist | UX/UI, Frontend; QA when its triggers apply |
| Docs, diagrams, Graphify, Obsidian, HTML report | Technical Writer / Knowledge Engineer | Source-domain owner(s) for verified facts |
| Production release, rollout, rollback, go/no-go | Release Manager | DevOps/SRE; QA when release verification evidence is required; other specialists according to risk |
| Multi-step, cross-functional, or multi-system delivery coordination | Delivery Lead | Relevant accountable owners and specialists activated by scope, dependencies, and risk |

## Examples

- **Small UI defect:** Frontend Developer. Add QA Manager when formal/regression verification, a delivery gate, multi-component verification, or material quality risk requires it. Add Accessibility Specialist only when its trigger applies. The implementation owner performs proportionate checks; activate Technical Writer only if a documentation/knowledge trigger applies.
- **New authenticated API:** API Manager + Backend Developer. Assess Penetration Tester when authentication, authorization, sensitive data, exposure, or trust-boundary triggers apply; add Database Manager if persistence changes and QA Manager when its verification triggers apply. Activate Technical Writer when API/developer documentation or knowledge transfer is required.
- **Webhook to an external CRM:** Integration Engineer + relevant API/Backend/Database owners. Assess Penetration Tester, QA Manager, Solution Architect, and DevOps/SRE against their specific security, verification, architecture, and operations triggers. Activate Technical Writer when integration documentation, runbooks, or knowledge transfer are required.
- **Production deployment:** Release Manager + DevOps / SRE. Add QA Manager when release verification evidence is a gate; add other specialists according to the release's actual risk and scope. Activate Technical Writer when release notes, runbooks, or other documentation deliverables are required.

## Cross-cutting completion obligations are not automatic role activations

A requirement to verify, document, or record a change does not by itself require activating a specialist role. Distinguish the work obligation from the role that performs it:

- **Verification:** The accountable implementation owner performs proportionate checks and records evidence. Activate QA Manager when the formal QA triggers or a required QA gate apply. QA inactivity never waives required verification.
- **Documentation:** The accountable source owner supplies accurate facts and completes documentation obligations assigned to that owner. Activate Technical Writer / Knowledge Engineer when the specialist documentation/knowledge triggers apply. Specialist inactivity never waives an explicit documentation deliverable.
- **Specialist review:** Apply each specialist's own required and conditional triggers. Do not infer activation from a role merely appearing in a task-map row, ownership contributor list, or collaboration relationship.

For every task, record the activation classification and reason for required/conditional roles under `docs/team/role-activation-rules.md`. If no specialist trigger applies, leave the role inactive rather than activating it as a universal process tax.

If the task does not fit a row, select roles by ownership boundaries and explain the selection briefly. Do not activate every role by default.
