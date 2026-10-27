# API Ship Gate

## When to use

Run this before any Go HTTP service leaves the Implementation phase. This is a
narrow gate: it covers only the API-surface items that a solo-plus-agents shop
actually gets wrong and pays for. Everything else an enterprise API checklist
would demand is either owned by another skill or rejected outright at the
bottom of this file.

Source: mined 2026-10-27 from a generic "API Development Checklist" paste.
Roughly 15% of that document was load-bearing for this shop, 15% duplicated
skills we already own, 70% was process theater for a large org. The split is
recorded at the bottom so this decision is not re-made every time someone
pastes a checklist.

## The gate

### Contract (blocking)

- [ ] `routes.go` and the OpenAPI spec agree. Generate the spec with the
      `golang-swagger` skill rather than writing it by hand; a hand-written
      spec drifts from code within one release.
- [ ] Every route's request and response schema is typed. `map[string]any` on
      an API boundary is a contract, just an unwritten one.
- [ ] Breaking change check ran. Compare the new spec against the previous
      release; any removed or retyped field is a version bump, not a merge.
- [ ] Every 4xx and 5xx the handler can return is in the spec. Handlers that
      return a bare `500` with no body shape are untestable from the client.

### Retry safety (blocking)

- [ ] Every mutation (POST/PATCH/DELETE) is idempotent or carries an
      idempotency key. Networks retry; a double-provision is a money bug.
- [ ] Idempotency keys are scoped per tenant, not global. One tenant's key
      must never be able to replay or probe another tenant's operation.
- [ ] The replay path returns the original response, not a fresh execution.

Idempotency key shape that works:

```go
type mutateRequest struct {
    IdempotencyKey string `json:"idempotency_key" validate:"required,uuid4"`
}

// First call: run the operation, store (tenant, key) -> response under the
// operation's row. Replay: look up (tenant, key), return stored response with
// the original status code. Never re-execute on hit.
// Key uniqueness index: UNIQUE(tenant_id, idempotency_key). The tenant column
// is what makes cross-tenant replay impossible at the database level rather
// than in application code.
```

### Backpressure (blocking)

- [ ] Every list endpoint is paginated. An unpaginated list is an outage
      waiting on one large tenant.
- [ ] Rate limits exist per tenant AND per endpoint, and a limited response
      carries `429` plus `Retry-After`. A `429` with no hint tells the client
      nothing and turns a bounded retry into a hot loop.
- [ ] Request body size limits are enforced before parsing, not after.
- [ ] Timeouts on every upstream call. A handler without a context deadline
      holds a connection until the caller gives up.

```go
// 429 with a retry hint the client can actually use.
func rateLimited(w http.ResponseWriter, retryAfter time.Duration) {
    w.Header().Set("Retry-After", strconv.Itoa(int(retryAfter.Seconds())))
    w.WriteHeader(http.StatusTooManyRequests)
    _ = json.NewEncoder(w).Encode(errorBody{
        Code:  "rate_limited", RetryAfterSeconds: int(retryAfter.Seconds()),
    })
}
```

### Operability (blocking)

- [ ] `/healthz` (liveness) and `/readyz` (readiness) are distinct. Liveness
      answers "should this process be restarted"; readiness answers "should
      this process receive traffic". Collapsing them makes a dependency outage
      look like a crash loop.
- [ ] Graceful shutdown drains in-flight requests before exit.
- [ ] Structured logs carry a request ID that appears in error responses too,
      so a user-reported error maps to server logs without guessing.

### Security (verify, do not re-derive)

Every item below is already owned by the `security-auditor` skill. Run that
skill's tenancy sweep; do not re-check these by hand from this file.

- Resource-level authorization (a valid session is not authorization for that
  row)
- Tenant isolation on every query, proven route by route
- CORS allowlist, HSTS, CSP
- Input validation, SQL injection, XSS, CSRF, path traversal, command
  injection, XXE, unsafe deserialization, ReDoS
- Secret storage and rotation

## Rejected on purpose

Recorded so the next pasted checklist does not reopen these. Each is either
theater for a solo-plus-agents shop or actively wrong for this stack.

| Item | Why rejected |
| --- | --- |
| HATEOAS | No consumer of these APIs navigates by links. It is cost without a client that benefits. |
| Team sign-offs (API team, security team, QA team, change management, business approval) | There is no team. The reviewer is an agent plus one human, and the review column already holds that role. |
| SLA docs, on-call rosters, incident comms plans | No one is paged. A watchdog cron covers detection. |
| Postman collections, SDK generation, mock servers | Premature until a public API has external consumers. Today the only consumer is the product's own client. |
| Blue-green, canary, circuit breaker, bulkhead | Single-host Dokploy deploys with SQLite and local models. These patterns pay off at a scale this stack is deliberately not at. |
| Cache invalidation and CDN strategy | Nothing here has CDN-shaped traffic. Adding it is cost without load. |
| >90% coverage targets as a number | A coverage number without an error-path assertion is a green suite that proves nothing. The gate is error-path tests, not a percentage. |

## Worked example: the two that bite

Both items below have failed in production on this stack in the last month, in
different shapes, which is why they carry examples and the rest do not.

**1. Retry safety.** A mobile client on a flaky connection retries a POST. With
no idempotency key the operation runs twice. In a multi-tenant billing surface
that is a double charge; in a provisioning surface a duplicate resource. The
fix is a unique index on (tenant_id, idempotency_key) so the database rejects
the second execution even if application logic is wrong.

**2. Backpressure.** A search aggregator upstream returned HTTP 429 to this
host's egress IP repeatedly in October 2026. Engines that retried without
honoring a retry hint were suspended for hours to days by the upstream. A
bounded `Retry-After` on the way out is the same contract extended to callers:
it converts a hard failure into a recoverable one.

## Exit gate

No API surface ships with a red item above. Contract, retry safety,
backpressure, and operability are blocking; security is blocking and owned by
`security-auditor`. Record the run in the phase's TODO item with the proof
that existed, not a claim that it passed.
