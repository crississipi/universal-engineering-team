# Static Security Assessment: Order Webhook

## Assessment record

- Scenario: `SCEN-APPSEC-STATIC-WEBHOOK-REVIEW`
- Role: Penetration Tester
- Scenario status: `approved`
- Rubric: `pilot-v2`
- Scope: The fictional handler and context included in the approved scenario only.
- Authorization: No target or live environment is authorized. This was a documentation-only static review.
- Tested revision/environment: Not applicable; no implementation or live environment was supplied.
- Session UTC start: `2026-11-06T00:30:15.475Z` (session metadata).
- Assessment runtime metadata: Provider `unknown`; displayed model label `unknown`; exact model/version `unknown`; Agent mode `unknown`; relevant settings `unknown`.

## Summary

The route is described as publicly reachable, and the supplied handler writes request-body fields to the orders database without checking request headers. The scenario also states that the provider signs webhook requests, may retry delivery, and that no authentication, signature verification, replay protection, schema validation, rate limiting, or retention policy is shown. These are observations about the supplied snippet and context, not proof that no upstream or database controls exist.

The main conditional risk is unauthorized order-record creation if no external authentication or signature verification protects the route. The handler also logs the full request body, inserts on every invocation, and has no visible input validation or local error handling. No dynamic validation or exploit attempt was performed.

## Assets and trust boundaries

- **Order integrity:** `order.id` and `order.total` are persisted as order data.
- **Customer data confidentiality:** `order.customer.email` is persisted, and the entire request body is sent to the application logger.
- **Public ingress:** Requests from the public internet cross into the webhook handler. The provider's HMAC header is a potential authenticity signal, but no verification is visible in the snippet.
- **Persistence and operations:** The handler writes to `db.orders` and emits a log record. Database constraints, log destinations, access, and retention are unknown.

## Findings

### PT-01 — Request authenticity is not checked in the supplied handler

- **Severity:** Medium
- **Classification:** Confirmed code observation; end-to-end exposure is conditional.
- **Evidence:** The route is stated to be public. The provider documentation says requests include an HMAC signature header, while the handler reads `req.body` and does not inspect request headers before inserting an order. The scenario says no authentication or signature-verification middleware is shown.
- **Impact:** If no upstream control verifies the sender and signature, an unauthenticated party able to reach the route could cause attacker-chosen order fields to be inserted. The snippet does not establish whether those records trigger fulfillment or other downstream effects.
- **Prerequisites:** The request must reach this handler without an upstream authentication/signature check, and the submitted body must be accepted by the database. Those conditions are not established for the whole application.
- **Confidence:** High that the supplied handler itself contains no visible verification; Medium that the complete endpoint is vulnerable, because middleware and upstream controls are unknown.
- **Remediation:** Verify the provider's HMAC against the exact raw request bytes before trusting or persisting the body. Compare signatures using a constant-time operation, reject missing/invalid signatures, and keep the signing secret in the approved secret store. If verification is middleware-owned, confirm it is mandatory for this route and covered by tests.

### PT-02 — Full request body is written to application logs

- **Severity:** Medium
- **Classification:** Confirmed logging behavior; exposure impact depends on logging controls.
- **Evidence:** `console.log("order received", req.body);` logs the complete body. The handler also reads `order.customer.email` from that body, so customer email is among the data handled by this route.
- **Impact:** Customer and order data may be retained or disclosed through log access, exports, or backups. The exact payload fields and log audience, storage, and retention are unknown.
- **Prerequisites:** Sensitive values are present in the body and a person or system without a business need can access or retain the resulting logs. The latter is not established.
- **Confidence:** High that the body is logged; Medium that this results in unauthorized disclosure.
- **Remediation:** Remove the raw body from routine logs. Log a minimal event identifier and outcome, redact any necessary fields, and apply access controls and retention limits consistent with the data policy.

### PT-03 — Repeated deliveries are inserted without visible idempotency handling

- **Severity:** Low
- **Classification:** Conditional data-integrity/operational risk.
- **Evidence:** Each invocation proceeds to `db.orders.insert(...)`. The provider may retry when it does not receive a 2xx response. No replay or duplicate-delivery handling is shown.
- **Impact:** A retry or replay may create duplicate order records if neither this handler nor the database deduplicates them. Downstream effects are not shown.
- **Prerequisites:** A delivery is processed more than once and there is no applicable uniqueness constraint or idempotency control. Database uniqueness constraints and upstream controls are unknown.
- **Confidence:** High that the snippet makes an insert on each invocation; Medium that duplicate rows result.
- **Remediation:** Use a stable provider event/delivery identifier as an idempotency key, enforce uniqueness transactionally, and make retries safe. Acknowledge success only after durable processing; handle a repeated event as an already-processed result.

### PT-04 — Request shape and failure handling are not visible

- **Severity:** Low
- **Classification:** Hardening observation; impact depends on controls outside the snippet.
- **Evidence:** The handler directly dereferences `order.customer.email` and inserts fields without visible schema validation or a local error handler. The provider may retry if it does not receive a 2xx response.
- **Impact:** Unexpected or malformed bodies may cause processing errors or invalid data. A failed operation may lead to a retry; the framework's response behavior and whether an earlier write could already have committed are unknown.
- **Prerequisites:** Invalid input reaches this handler without upstream validation, or a database operation fails. Neither condition nor its resulting response is established.
- **Confidence:** High that validation and local error handling are not shown; Low-to-Medium that this causes a security-relevant failure in the deployed system.
- **Remediation:** Validate the body against a strict schema before use, reject invalid requests with a controlled response, and handle persistence failures explicitly. Preserve retryable failure semantics without returning success for uncommitted work, and combine this with PT-03 idempotency.

## Confirmed observations versus conditional risks

The snippet confirms the raw request body is logged, selected body fields are inserted, the handler itself does not inspect headers, and no schema validation, idempotency logic, or local error handling appears in the supplied code. The context confirms public reachability, provider HMAC documentation, and possible provider retries.

It does **not** establish that the overall deployed endpoint lacks upstream authentication or signature middleware, that the database permits duplicate order IDs, that the logged data is broadly accessible, that invalid input can reach the handler, or that downstream fulfillment or other high-impact effects occur. No exploitability was tested or confirmed.

## Limitations and exclusions

- Static review only; no network traffic, payload execution, host/service probing, scanning, or exploitation.
- Only the fictional code and scenario context were reviewed.
- Upstream middleware/network controls, runtime/framework behavior, body parsing, database uniqueness/transaction behavior, downstream processing, logging access/retention, and operational error handling were not supplied and remain unknown.
- Rate limiting and data-retention controls are stated as not shown; their presence elsewhere was not determined.
- No remediation was implemented or retested.

## Execution and evidence notes

- Scenario approval and rubric version were read from the scenario file.
- Transcript preservation was attempted using the available session-context mechanism, but its result reported `truncated: true`. The current VS Code window exposed a document rather than the chat transcript; attempts to open its chat control were interrupted twice because user input was detected. No partial transcript is represented as complete, and no transcript artifact was created.
- The initial `git --no-pager status --short` completed with exit code 0 and no status entries.
- No tests, scanners, dependency checks, or dynamic tests were run.
