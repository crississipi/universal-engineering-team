# Skills Resolver

Use this guide to select the smallest sufficient set of specialist skills. It is a routing aid, not a replacement for repository discovery, the role ownership model, or specialist instructions.

## Routing rules

1. Identify the primary deliverable and activate its owning role.
2. Add supporting roles only when the task crosses their responsibility boundary or carries a material risk in that domain.
3. Activate QA Manager for every meaningful code, configuration, data, integration, or release change. Scale test depth to risk.
4. Activate Technical Writer / Knowledge Engineer for every meaningful change because documentation and knowledge updates are part of completion.
5. Activate Solution Architect for multi-service, cross-platform, major refactor, or high-risk boundary decisions.
6. Activate Release Manager for production/shared-environment release coordination, not for ordinary local implementation.
7. The resolver never grants permission for destructive actions, production changes, credential access, or security testing beyond explicit authorization.
8. Activate Delivery Lead for multi-step, cross-functional, or multi-system work that needs coordinated ownership, sequencing, handoffs, blocker management, or integration oversight. For a small task owned by one specialist, that specialist can coordinate the task without activating a separate Delivery Lead.

## Task-to-role map

| Task or change | Primary role | Add supporting roles when relevant |
|---|---|---|
| New feature, unclear scope, user workflow | Product Analyst | UX/UI, Solution Architect, QA |
| System design, service boundaries, major refactor | Solution Architect | API, Integration, Database, Backend, Frontend, DevOps/SRE, Security, QA |
| API or event contract | API Manager | Backend, Frontend, Integration, Security, QA |
| Server-side behavior, jobs, business rules | Backend Developer | API, Database, Integration, Security, QA |
| Browser/mobile UI, client state | Frontend Developer | UX/UI, Accessibility, API, QA |
| Interaction design, navigation, visual system | UX/UI Designer | Product Analyst, Frontend, Accessibility, QA |
| Schema, migration, integrity, query | Database Manager | Backend, Data Engineer, DevOps/SRE, Security, QA |
| SaaS/partner integration, webhook, queue, event flow | Integration Engineer | Architect, API, Backend, Database, Security, DevOps/SRE, QA |
| ETL/ELT, ingestion, transformation, analytics pipeline | Data Engineer | Database, Integration, Security, DevOps/SRE, QA |
| Test strategy, regression, defect verification | QA Manager | Relevant implementation owner and specialist reviewers |
| Authentication, authorization, threat, dependency or trust-boundary risk | Penetration Tester / AppSec | Architect, API, Backend, Frontend, DevOps/SRE, QA |
| CI/CD, hosting, infrastructure, monitoring, recovery | DevOps / SRE | Architect, Backend, Database, Security, QA, Release |
| Measured latency, throughput, memory, scaling issue | Performance Engineer | Relevant implementation owner, Architect, QA, DevOps/SRE |
| Accessibility audit or inclusive interaction change | Accessibility Specialist | UX/UI, Frontend, QA |
| Docs, diagrams, Graphify, Obsidian, HTML report | Technical Writer / Knowledge Engineer | Source-domain owner(s) for verified facts |
| Production release, rollout, rollback, go/no-go | Release Manager | QA, DevOps/SRE, Security, Architect, Product |
| Multi-step, cross-functional, or multi-system delivery coordination | Delivery Lead | Relevant specialists; Solution Architect for material architecture decisions; QA and Technical Writer / Knowledge Engineer for verification and documentation |

## Examples

- **Small UI defect:** Frontend Developer + QA Manager + Technical Writer / Knowledge Engineer. Add Accessibility Specialist only if an accessibility concern is implicated.
- **New authenticated API:** API Manager + Backend Developer + Penetration Tester / AppSec + QA Manager + Technical Writer / Knowledge Engineer. Add Database Manager if persistence changes.
- **Webhook to an external CRM:** Integration Engineer + API Manager + Backend Developer + Database Manager + Penetration Tester / AppSec + QA Manager + Technical Writer / Knowledge Engineer. Add Solution Architect and DevOps/SRE when topology or operations materially change.
- **Production deployment:** Release Manager + DevOps / SRE + QA Manager; add Security and Solution Architect according to risk.

If the task does not fit a row, select roles by ownership boundaries and explain the selection briefly. Do not activate every role by default.
