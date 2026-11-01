# Team ownership and collaboration

| Role | Primary ownership | Must collaborate with | Not the owner of |
|---|---|---|---|
| Product Analyst | problem, requirements, acceptance criteria, scope | UX, Architect, QA, Delivery | technical design |
| Solution Architect | system boundaries, architecture, technical decisions | all technical leads | detailed implementation |
| UX/UI Designer | flows, interaction, visual system, prototypes | Product, Frontend, Accessibility | production code quality |
| Frontend Developer | client app, state, rendering, client integration | UX, API, QA, Accessibility | backend contracts |
| Backend Developer | domain logic, services, server workflows | API, Database, Security, QA | infrastructure platform |
| API Manager | API contracts, lifecycle, compatibility, standards | Backend, Frontend, Integration, Security | business workflow implementation |
| Integration Engineer | cross-system workflows, adapters, event exchange | API, Backend, Data, SRE | provider-owned internals |
| Database Manager | schema, migrations, query/data integrity | Backend, Data, SRE | domain requirements |
| Data Engineer | ingestion, transformation, pipelines, data quality | Database, Integration, Product | transactional API ownership |
| QA Manager | quality strategy, test design, release quality evidence | all implementation roles | implementing product features |
| Penetration Tester / AppSec | threat modeling, security testing, remediation validation | Architect, Backend, SRE, QA | feature ownership |
| DevOps / SRE | build, deploy, runtime, reliability, observability | Architect, Backend, QA, Security | product semantics |
| Performance Engineer | profiling, capacity, latency, bottleneck analysis | Frontend, Backend, Data, SRE | premature optimization |
| Accessibility Specialist | accessibility evaluation and remediation guidance | Product, UX, Frontend, QA | visual product direction |
| Technical Writer / Knowledge Engineer | docs, Obsidian, Graphify, central report | every role; Delivery Lead | undocumented implementation decisions |
| Release Manager | release readiness, change coordination, rollback | QA, SRE, Security, Delivery | approving unverified quality |

## Assignment rule
Assign one accountable owner for each deliverable. Other roles provide bounded reviews. The Delivery Lead owns integration and closure.
