# Producer-Consumer Relationship Matrix

## Purpose

This document identifies the package-level relationships between producers
and consumers in the Universal Engineering Team.

The canonical package ownership source remains:

`docs/team/ownership.yml`

This matrix supplements ownership by identifying:

- Which package provides an output.
- Which package consumes that output.
- What information or deliverable is consumed.
- Whether the relationship is required, conditional, or feedback-oriented.
- Whether the relationship creates a genuine work prerequisite.

This document does not define formal handoff contracts.

The contract schema is defined in:
`docs/team/handoff-contract-schema.md`

Acceptance and resubmission procedures are defined in:
`docs/team/handoff-acceptance-rules.md`

Escalation and conflict-resolution procedures are defined in:
`docs/team/handoff-escalation-rules.md`

## 1. Relationship types

### `required_input`

The consumer needs the producer's output to complete the relevant
part of its work.

A required input is scoped to the applicable project work. It does not
mean every project must activate every package.

### `conditional_input`

The relationship applies only when a relevant feature, system,
technology, or risk exists in the project.

The Delivery Lead must not activate the relationship when its trigger
does not apply.

### `feedback`

The consumer receives findings, recommendations, or verification results
from the producer and may need to revise its own package.

Feedback does not normally prevent the receiving package from starting.
It may, however, become a completion or release condition when the
relevant risk or acceptance requirement demands it.

## 2. Producer-consumer matrix

| Producer package | Consumer package | Output consumed | Relationship | Trigger / boundary |
|---|---|---|---|---|
| `ART-PRODUCT-REQUIREMENTS` | `ART-ARCHITECTURE` | Approved scope, requirements, constraints, quality attributes, and acceptance criteria | `required_input` | Required for architecture decisions addressing the requested outcome. |
| `ART-PRODUCT-REQUIREMENTS` | `ART-UX-DESIGN` | User needs, journeys, priorities, and user-facing acceptance criteria | `conditional_input` | When the project includes user-facing experiences. |
| `ART-PRODUCT-REQUIREMENTS` | `ART-QUALITY-EVIDENCE` | Acceptance criteria, scope boundaries, and expected outcomes | `required_input` | Required to establish acceptance traceability for in-scope requirements. |
| `ART-PRODUCT-REQUIREMENTS` | `ART-PERFORMANCE-EVIDENCE` | Performance-related user outcomes and non-functional requirements | `conditional_input` | When performance targets or measurable service expectations exist. |
| `ART-PRODUCT-REQUIREMENTS` | `ART-ACCESSIBILITY-ASSESSMENT` | Accessibility-related requirements and applicable user scenarios | `conditional_input` | When accessibility requirements or user-facing interfaces are in scope. |
| `ART-ARCHITECTURE` | `ART-API-CONTRACT` | System boundaries, service responsibilities, interaction patterns, and architectural constraints | `conditional_input` | When APIs or events cross a defined system boundary. |
| `ART-ARCHITECTURE` | `ART-DATA-MODEL` | Data ownership, system boundaries, consistency requirements, and architecture constraints | `conditional_input` | When the project creates or changes persistent data structures. |
| `ART-ARCHITECTURE` | `ART-BACKEND` | Service boundaries, backend responsibilities, technical decisions, and relevant architecture diagrams | `required_input` | Required for backend work governed by a defined system design. |
| `ART-ARCHITECTURE` | `ART-FRONTEND` | Client architecture, integration boundaries, and relevant technical constraints | `conditional_input` | When frontend implementation depends on cross-system or client architecture decisions. |
| `ART-ARCHITECTURE` | `ART-INTEGRATION` | Integration topology, trust boundaries, system interactions, and architecture decisions | `conditional_input` | When external systems or separately operated services are integrated. |
| `ART-ARCHITECTURE` | `ART-OPERATIONS` | Deployment topology, runtime boundaries, infrastructure decisions, and operational constraints | `conditional_input` | When deployment or infrastructure work is in scope. |
| `ART-ARCHITECTURE` | `ART-SECURITY-ASSESSMENT` | System context, assets, trust boundaries, and architecture diagrams | `conditional_input` | When security assessment or threat modeling is required. |
| `ART-UX-DESIGN` | `ART-FRONTEND` | User flows, wireframes, interaction states, information hierarchy, and visual guidance | `conditional_input` | Required for the user-facing portions of projects that include UX design. |
| `ART-UX-DESIGN` | `ART-ACCESSIBILITY-ASSESSMENT` | Interaction patterns, content structure, and design decisions to assess | `conditional_input` | When the design includes user-facing interactions or content. |
| `ART-API-CONTRACT` | `ART-BACKEND` | API/event schemas, validation rules, authentication requirements, and error semantics | `conditional_input` | When backend work implements the defined API or event contract. |
| `ART-API-CONTRACT` | `ART-FRONTEND` | Endpoint definitions, request/response schemas, error behavior, and compatibility rules | `conditional_input` | When the frontend consumes the defined API. |
| `ART-API-CONTRACT` | `ART-INTEGRATION` | External API/event schemas, authentication requirements, versioning, and compatibility rules | `conditional_input` | When an integration uses the defined API or event interface. |
| `ART-API-CONTRACT` | `ART-QUALITY-EVIDENCE` | Contract schemas, examples, error behavior, and compatibility expectations | `conditional_input` | When API or event contract testing is applicable. |
| `ART-DATA-MODEL` | `ART-BACKEND` | Entity definitions, relationships, constraints, migration plans, and data access guidance | `conditional_input` | When backend behavior reads or writes the governed data structures. |
| `ART-DATA-MODEL` | `ART-DATA-PIPELINE` | Source and target structures, data definitions, schema constraints, and evolution guidance | `conditional_input` | When pipelines read from or write to the governed data structures. |
| `ART-DATA-MODEL` | `ART-INTEGRATION` | Persistence structures, identifier rules, and data ownership constraints | `conditional_input` | When integration mappings or reconciliation persist data in the governed database. |
| `ART-DATA-MODEL` | `ART-QUALITY-EVIDENCE` | Data constraints, migration expectations, and integrity requirements | `conditional_input` | When database behavior, migrations, or data integrity are tested. |
| `ART-INTEGRATION` | `ART-DATA-PIPELINE` | Source connectivity, extraction behavior, mapping details, and integration failure semantics | `conditional_input` | When a data pipeline depends on external or integrated sources. |
| `ART-INTEGRATION` | `ART-QUALITY-EVIDENCE` | Integration flows, mapping rules, retry behavior, idempotency, and reconciliation scenarios | `conditional_input` | When integration behavior requires verification. |
| `ART-INTEGRATION` | `ART-OPERATIONS` | Runtime dependencies, delivery/retry behavior, failure modes, and recovery requirements | `conditional_input` | When integration components require deployment, monitoring, or operational recovery. |
| `ART-BACKEND` | `ART-QUALITY-EVIDENCE` | Backend implementation, automated tests, and observable service behavior | `required_input` | Required for verification of implemented backend scope. |
| `ART-BACKEND` | `ART-SECURITY-ASSESSMENT` | Implemented authentication, authorization, validation, and service behavior | `conditional_input` | When backend security assessment is in scope. |
| `ART-BACKEND` | `ART-PERFORMANCE-EVIDENCE` | Running service behavior, workload paths, and profiling targets | `conditional_input` | When backend performance is being measured or optimized. |
| `ART-BACKEND` | `ART-OPERATIONS` | Runtime requirements, health behavior, configuration needs, and deployment constraints | `conditional_input` | When backend deployment or operations are in scope. |
| `ART-BACKEND` | `ART-KNOWLEDGE-DOCS` | Verified implementation behavior, service interfaces, and operational facts | `conditional_input` | When backend changes affect technical documentation. |
| `ART-FRONTEND` | `ART-QUALITY-EVIDENCE` | UI implementation, user-visible states, and frontend test results | `required_input` | Required for verification of implemented frontend scope. |
| `ART-FRONTEND` | `ART-ACCESSIBILITY-ASSESSMENT` | Implemented semantics, controls, navigation, focus behavior, and user interactions | `conditional_input` | When frontend accessibility assessment is in scope. |
| `ART-FRONTEND` | `ART-PERFORMANCE-EVIDENCE` | Render behavior, client-side workloads, and profiling targets | `conditional_input` | When frontend performance is being measured or optimized. |
| `ART-FRONTEND` | `ART-KNOWLEDGE-DOCS` | Verified user-visible behavior, routes, component behavior, and implementation notes | `conditional_input` | When frontend changes affect technical or user-facing documentation. |
| `ART-DATA-PIPELINE` | `ART-QUALITY-EVIDENCE` | Pipeline behavior, transformation rules, lineage, and data quality results | `conditional_input` | When pipeline behavior or data quality requires verification. |
| `ART-DATA-PIPELINE` | `ART-OPERATIONS` | Scheduling, dependencies, monitoring needs, replay, and backfill procedures | `conditional_input` | When pipeline execution requires operational deployment or support. |
| `ART-DATA-PIPELINE` | `ART-KNOWLEDGE-DOCS` | Verified lineage, transformation behavior, and pipeline operating procedures | `conditional_input` | When pipeline changes affect technical documentation. |
| `ART-SECURITY-ASSESSMENT` | `ART-ARCHITECTURE` | Threats, trust-boundary findings, and architecture-level recommendations | `feedback` | When assessment findings require architecture review or a design change. |
| `ART-SECURITY-ASSESSMENT` | `ART-BACKEND` | Backend vulnerabilities, remediation recommendations, and retest findings | `feedback` | When backend security findings are identified. |
| `ART-SECURITY-ASSESSMENT` | `ART-INTEGRATION` | Integration vulnerabilities, provider risks, and remediation recommendations | `feedback` | When integration security findings are identified. |
| `ART-SECURITY-ASSESSMENT` | `ART-OPERATIONS` | Infrastructure, configuration, and runtime security findings | `feedback` | When operational security findings are identified. |
| `ART-SECURITY-ASSESSMENT` | `ART-RELEASE-PACKAGE` | Security findings, severity, remediation status, and unresolved risk evidence | `conditional_input` | When security assessment is required for release readiness. |
| `ART-ACCESSIBILITY-ASSESSMENT` | `ART-FRONTEND` | Accessibility findings, reproduction details, remediation guidance, and verification results | `feedback` | When frontend accessibility barriers are identified. |
| `ART-ACCESSIBILITY-ASSESSMENT` | `ART-UX-DESIGN` | Design-level accessibility findings and inclusive interaction recommendations | `feedback` | When design changes are needed to address accessibility barriers. |
| `ART-ACCESSIBILITY-ASSESSMENT` | `ART-RELEASE-PACKAGE` | Accessibility findings and applicable verification evidence | `conditional_input` | When accessibility evidence is a release requirement. |
| `ART-PERFORMANCE-EVIDENCE` | `ART-BACKEND` | Backend bottleneck analysis and optimization recommendations | `feedback` | When backend performance issues are identified. |
| `ART-PERFORMANCE-EVIDENCE` | `ART-FRONTEND` | Client-side bottleneck analysis and optimization recommendations | `feedback` | When frontend performance issues are identified. |
| `ART-PERFORMANCE-EVIDENCE` | `ART-DATA-MODEL` | Query, indexing, and database performance findings | `feedback` | When database performance issues are identified. |
| `ART-PERFORMANCE-EVIDENCE` | `ART-OPERATIONS` | Capacity, infrastructure, and runtime performance findings | `feedback` | When operational capacity or runtime issues are identified. |
| `ART-PERFORMANCE-EVIDENCE` | `ART-RELEASE-PACKAGE` | Performance baseline, target results, and unresolved performance risks | `conditional_input` | When performance targets are release acceptance criteria. |
| `ART-QUALITY-EVIDENCE` | `ART-RELEASE-PACKAGE` | Test execution results, acceptance traceability, regression evidence, and unresolved defects | `required_input` | Required when a release is subject to the team's QA process. |
| `ART-OPERATIONS` | `ART-RELEASE-PACKAGE` | Deployment readiness, monitoring, backup, restore, rollback, and operational procedures | `conditional_input` | Required when the release includes deployment or runtime changes. |
| `ART-PRODUCT-REQUIREMENTS` | `ART-RELEASE-PACKAGE` | Approved scope and user-facing change expectations | `conditional_input` | When release notes or release scope must be checked against approved requirements. |
| `ART-RELEASE-PACKAGE` | `ART-DELIVERY-RECORD` | Release status, readiness decision, rollout outcome, and outstanding follow-up actions | `conditional_input` | When a release is part of the delivery being coordinated. |

## 3. Cross-cutting consumers

Some consumers use information from many packages rather than depending
on one specific package.

### Documentation and Knowledge Package

`ART-KNOWLEDGE-DOCS` consumes verified facts from every active package
when those facts affect documentation, diagrams, knowledge links,
Obsidian, Graphify, or the central report.

This is an ongoing documentation responsibility, not a requirement to
create a separate formal handoff for every package in every task.

The Technical Writer / Knowledge Engineer must use the accountable
producer's verified output as the source of technical facts. It must
not independently invent or reinterpret implementation behavior.

### Delivery Coordination Package

`ART-DELIVERY-RECORD` consumes status and coordination information from
the active package owners, including:

- Current owner and work status.
- Declared dependencies and blockers.
- Completed outputs and verification evidence.
- Unresolved decisions and risks.
- Next action and accountable role.

This is an internal coordination relationship. It does not make the
Delivery Lead the owner of specialist outputs.

## 4. Dependency rules

1. A producer-consumer relationship does not automatically create a
   blocking prerequisite.
2. A `required_input` must be available before the consumer finalizes
   the work that depends on it.
3. A `conditional_input` is activated only when its stated trigger applies.
4. A `feedback` relationship may cause rework or reassessment, but it
   does not prevent the receiving package from starting.
5. Consumers may begin non-dependent work in parallel while waiting
   for required inputs.
6. A consumer must identify the exact missing input and its impact when
   blocked. It must not silently invent a substitute.
7. A producer remains accountable for the accuracy and completeness
   of its output after it is consumed.
8. A consumer remains accountable for its own package and decisions.
9. A handoff transfers a defined output, not package ownership.
10. Contributor lists do not establish producer-consumer relationships.
11. Role names, workflow order, and informal collaboration descriptions
    must not be used as the sole evidence for a dependency.
12. Feedback loops are permitted. The collaboration graph may contain
    cycles.

## 5. Work prerequisite graph

The matrix describes package relationships, including feedback.
It must not be interpreted as one global linear execution sequence.

For dependency planning:

- Use `required_input` relationships to identify genuine prerequisites.
- Activate `conditional_input` relationships only when their triggers apply.
- Treat `feedback` relationships as review and correction paths.
- Allow parallel work that does not depend on an unavailable input.
- Do not require an entire upstream package to be complete when only
  a specific approved portion is needed.
- Do not treat release-readiness evidence as a prerequisite for starting
  implementation.

The Delivery Lead coordinates sequencing. Specialist owners retain
authority over their respective outputs.

## 6. Relationship to handoff contracts

This matrix identifies candidate producer-consumer relationships.

It does not yet define:

- Formal handoff IDs.
- Exact handoff payload schemas.
- Required metadata.
- Delivery channels or storage locations.
- Acceptance checks.
- Rejection and resubmission procedures.
- Escalation and timeout rules.

Those are defined in Phase 1.2.3 and subsequent Phase 1.2 stages.

Only relationships approved during review should become formal handoffs.

## 7. Review and maintenance

Before activating these relationships:

1. Confirm the producer package and accountable owner.
2. Confirm the consumer package and accountable owner.
3. Verify that the listed output exists in the producer package's scope.
4. Confirm that the consumer genuinely needs the output.
5. Confirm the relationship type and trigger.
6. Determine whether it is a real prerequisite or only a feedback path.
7. Remove duplicate, speculative, or unnecessary relationships.
8. Record unresolved relationships as open review items rather than
   silently treating them as approved.

Update this matrix when package scope, responsibility boundaries,
or verified producer-consumer needs change.

Run the repository validation scripts after changes.
