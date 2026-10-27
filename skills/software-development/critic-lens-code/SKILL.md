---
name: critic-lens-code
description: "Use when skeptic reviews code or architecture."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
 hermes:
 tags: [critic, code-review, security, tenancy, performance, architecture]
 related_skills: [persona-skeptic, security-auditor, commit-gates, exec-scripts, ui-visual-check, golang, flutter, rust, mojo, systematic-debugging]
---

# Critic Lens: Code and Architecture

## When to Use

Load alongside `persona-skeptic` when the artifact under attack is source code, an API, a schema, an architecture, or infrastructure config. This lens aims the skeptic's hostility at the seams where software actually breaks.

## The attack surface (in severity order)

Run these passes top-down. Stop inflating about style when a load-bearing defect is open.

**Execute before you attack (checklist A).** Load `exec-scripts` and run the build, vet, linter, type checker, and full test suite with race detector, then boot the app and read the logs. Capture real exit codes and output. In our own experiment the two critics that ran `go test` both caught a live test-harness leak that all four static readers missed. Reading without running is half a review.

**Sweep, do not sample (checklist B).** Enumerate every route, handler, and exported function programmatically (grep or AST) and produce a matrix marking each PASS/FAIL/UNTESTED against the access-control rule. Every critic in our experiment admitted the sibling routes went unchecked; that admission is the defect. Finish the sweep. (Anecdote, not artifact: internal sessions, run ledgers not committed; treat n as illustrative.)

**Severity is deterministic (checklist C).** Score exploitability x impact and map to Critical/High/Medium/Low with a fixed rubric. The same defect always gets the same severity.

For anything with a running UI, hand off to `ui-visual-check` so the browser pass and screenshots are captured, and route findings into the fix loop per `QA-LOOP.md`.

### 1. Tenancy and access (the AlphaFlux-class killer)

- For every query, cache, file path, queue message, search index, and log: does tenant A reach tenant B? One missed filter is a breach, not a nit.
- Identity from the verified session only, never a client-supplied header or body field.
- Scoping inside the query, not a WHERE clause a builder can forget.
- Foreign-object responses match the nonexistent-object shape so existence cannot be probed.
- Deny by default on new routes.

### 2. Security (OWASP Top 10:2025 lens)

- A01 Broken Access Control (SSRF folded in), A02 Misconfiguration, A03 Supply Chain, A04 Crypto, A05 Injection, A06 Insecure Design, A07 Auth, A08 Integrity, A09 Logging, A10 Exceptional Conditions (fail-open, panic paths).
- Injection sinks parameterized or allowlisted: SQL, command, template, path, deserialization, log/CSV.
- Secrets never in code, logs, images, or git history. Error and panic paths do not fail open or leak state across requests.

### 3. Correctness and failure behavior

- Happy path, negative path, and boundary tested. Empty, zero, one-past-max, unicode, huge payload, DST and month-end, double-submit.
- Error handled explicitly, never swallowed. No silent failures, no dead code.
- Race conditions and goroutine/thread leaks on concurrent paths.

### 4. Performance and scale

- N+1 query patterns, unbounded queries, missing pagination, missing indexes on the hot path.
- Connection and resource pools, timeouts, backpressure.
- Does it hold at 1000x tenants or traffic, or does one tenant starve the rest.

### 5. Maintainability

- Module isolation, one responsibility, tight scope. No monolith or spaghetti.
- Interface seams at provider, executor, storage, transport boundaries.
- Debugging and logging built in from birth: can you pull the bug information out when it misbehaves.

## What the code skeptic always demands

- **Evidence over claims.** "It compiles" is not "it works". "Tests pass" requires the command and the raw output, run this session, not a paraphrase.
- **The diff, not the summary.** Review the real changed lines. A summary of a diff is a claim about a diff.
- **The class, not the instance.** For every bug found, ask the sibling call paths. Fix the class, note the audit.

## Output additions (append to the core contract)

- **Defect ledger.** Numbered by severity (Critical, High, Medium, Low). Each: file:line, the defect, the exploit or failure path, the smallest fix.
- **Untested surface.** What was claimed but has no runnable proof attached.
- **Verdict** folds into the core one-line: ship, fix first, or do not trust.

## Failure modes this lens exists to catch

- Tenancy sampled instead of swept. Spot-checking three routes and declaring isolation good.
- "Reachability" as a pass: "we never call that function" with no evidence.
- Trusting a green pipeline badge as proof of production behavior.
- A fix that patches one instance while the bug class survives in sibling paths.

## Mapping to David's Products

- AlphaFlux: tenancy sweep is mandatory, route by route, no sampling. Go backend, Flutter clients, SurrealDB.
- AlphaVision: update-path integrity, untrusted input (remote, cast, deep links), local port exposure.
- the harness: the full agent surface, prompt injection via repo content, tool abuse, sandbox egress, secret exposure.
- Any Go service: golang and golang-pro idioms; any Flutter surface: flutter widget and state tests.
