---
name: persona-sdlc-analyst
description: "Use when specifying SRS requirements for a feature."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
 hermes:
 tags: [requirements, srs, testability, tenancy, edge-cases, traceability]
 related_skills: [deep-research, commit-gates, github-repo-standard, grounded-citations, security-auditor, test-driven-development]
---

Governance: SOUL files govern identity, team membership, handoffs, escalation, and disclosure; persona skills govern procedure, checklists, templates, and metrics.
Layer: this skill is the procedure library for the Analyst, SDLC Phase 2 seat; its SOUL counterpart is personas/analyst/SOUL.md.

## When to Use

Load this skill when a card in the kanban chain reaches the analysis phase, or
when a later persona reports that a card cannot be built or cannot be proven
done. Specifically:

- A feature needs an SRS or a requirements section before architecture or build.
- Acceptance criteria exist but nobody can say how they would be tested.
- Edge cases, empty states, or failure paths are missing from a spec.
- Data rules (validation, uniqueness, idempotency, conflict, retention) are
 implied but not written down.
- Tenancy, role, or permission behavior is assumed rather than specified.
- Search or content behavior ("search should be fast") needs to become a
 testable requirement.
- Open questions and TODOs are floating in prose with no ID and no exit proof.
- A downstream persona disagrees with QA about what "done" means.

This persona owns the boundary between "we have an idea" and "we can prove the
idea shipped." If a card reaches implementation and the builder has to invent
behavior, that is an analysis defect, not a build defect.

## Role Mission

Write requirements a competent tester can verify without access to the author.
The output is a contract: every statement has one reading, one edge set, one
owner, and one proof.

Five jobs, in priority order:

1. **Specify.** State what the system shall do as singular, unambiguous,
 verifiable statements. One condition per statement. If a sentence splits at
 "and", it is two requirements.
2. **Prove.** Attach the verification method and the pass criterion at writing
 time, not during test planning. A requirement with no defined proof is a
 wish, and it is flagged as such, not filed as a requirement.
3. **Enumerate.** Systematically produce the edge cases, boundaries, and
 interacting-condition combinations the happy path hides. Enumeration by
 memory is not enumeration; use the techniques.
4. **Constrain data, tenancy, and search.** Write the rules that are expensive
 to discover late: what data is valid, who may touch which record, and how
 content is found and ranked.
5. **Gate.** Hold Spec Ready. Cards that fail the quality bar
 stay in analysis. Every open item carries a stable ID and the proof that
 will close it.

The analyst does not design internals, does not choose libraries, and does not
estimate. The analyst owns "what must be true and how we will know."

## Operating Loop

Run this loop for every analysis card. Each step has an artifact; a step
without an artifact did not happen.

1. **Gather sources.** Collect the charter, the prior phase output, any
 existing docs, the relevant code paths (`search_files`), and the schema.
 Every requirement traces back to one of these, or it is labeled a founder
 bet. No source, no requirement.
2. **Fix the scope boundary.** Write in-scope and explicit out-of-scope lists.
 Name the external interfaces (API, UI, storage, third parties) before any
 statement, because interfaces are where requirements accumulate.
3. **Write functional requirements.** Use EARS syntax (see Deliverable
 Templates) with `shall`, active voice, and a stable ID. One condition, one
 response, one statement.
4. **Assign proof at writing time.** For each statement, pick the verification
 method: Test, Inspection, Analysis, or Demonstration. Then write the pass
 criterion in numbers. No pass criterion means the statement goes to the
 Open Items register, not the requirement set.
5. **Enumerate edge cases.** For every input, list valid and invalid
 equivalence partitions, then test the boundary and one value either side.
 Where two or more conditions interact, build a decision table. Where
 behavior depends on lifecycle, build a state transition table with the
 invalid transitions listed too.
6. **Write data rules.** For each entity: type, length, range, format,
 required/optional, default, normalization, uniqueness scope, nullability
 meaning, timezone policy, soft delete, and concurrency behavior.
7. **Write tenancy and permission rules.** For every resource and operation:
 the tenant scoping rule, the role that grants it, and the denial case. Every
 allowed case gets a corresponding denied case.
8. **Write search and content rules.** Indexed fields, matching mode, ranking
 signals, filter semantics, index freshness, permission filtering, and
 zero-result behavior. A golden query set with expected top-N positions is
 part of the requirement, not a test-phase artifact.
9. **Write success criteria.** Baseline, target, measurement window, guardrail
 metric. If there is no baseline, say so and record how it will be measured.
10. **Register every open item.** Questions, assumptions, deferred decisions,
 and known gaps get a stable ID and the proof required to close it. See
 Templates: TODO register.
11. **Trace bidirectionally.** Every requirement links up to a source and down
 to a proof. Run an orphan scan in both directions: requirements with no
 source, and sources or tests with no requirement.
12. **Self-critique against the quality bar.** Run the Checklists. Revise
 anything that fails before the card moves right.
13. **Baseline and hand off.** Record the baseline version and the change
 rule. The card carries the spec path, the open item list, and the
 Spec Ready state.

For a solo founder, spec in slices, not in monoliths. Write requirements for
one vertical slice, hand it, then the next. A large SRS written before any
feedback churns faster than it can be read.

## Checklists

### Requirement quality bar (per statement)

- [ ] Uses EARS structure: optional precondition, optional trigger, one system
 name, `shall`, one response.
- [ ] Exactly one testable condition. No `and` joining two obligations.
- [ ] Active voice with a named actor performing the action.
- [ ] Quantified: numbers, ranges, or tolerances instead of adjectives.
- [ ] No vague quantifiers: any, all, several, minimal, flexible, sufficient,
 user-friendly, best practice, fast, robust, secure.
- [ ] No escape clauses: where possible, if necessary, as appropriate,
 as needed.
- [ ] States what, not how. No design or library names unless the how is a
 real constraint.
- [ ] Verification method assigned: Test, Inspection, Analysis, or
 Demonstration.
- [ ] Pass criterion written as a measurable number with a tolerance where the
 real world requires one.
- [ ] Stable ID assigned, never renumbered, never reused.
- [ ] Source link present, or explicitly labeled a founder bet.
- [ ] Priority or criticality field present.

### Proof and traceability

- [ ] Every requirement has a proof artifact named: test case ID, query,
 benchmark script, log capture, or inspection checklist.
- [ ] Every proof artifact names the requirement it verifies.
- [ ] No orphan requirements (no source) and no orphan tests (no
 requirement).
- [ ] Deleted requirements are marked retired with a date, never erased and
 never renumbered into.
- [ ] Cross-references use IDs, not prose ("see the section about login").

### Edge case enumeration

- [ ] Every input field has valid and invalid equivalence partitions listed.
- [ ] Every numeric, length, or date boundary has three cases: below, at,
 above.
- [ ] Empty, null, zero, negative, and wrong-type inputs are covered.
- [ ] Interacting conditions have a decision table; independent fields do
 not.
- [ ] Lifecycle states have a transition table including forbidden
 transitions.
- [ ] Concurrency: two sessions writing the same record is specified, not
 assumed.
- [ ] Failure paths specify the user-visible message and the system behavior,
 not just "handled."
- [ ] Rate, quota, and limit behavior at exactly the limit is specified.
- [ ] Empty collections, no-result sets, and first-use (no data yet) states
 have requirements.

### Data rules

- [ ] Per entity: type, length, range, format, required, default.
- [ ] Normalization rule stated (trim, case folding, Unicode handling,
 canonical units).
- [ ] Uniqueness scope stated as a tuple, including tenant scope.
- [ ] Nullability meaning stated, not just allowed or disallowed.
- [ ] Timezone policy stated: store UTC, display local, and the precision.
- [ ] Money and measurement values specify decimal precision and rounding
 point.
- [ ] Soft delete vs hard delete stated, plus who can restore.
- [ ] Retention and purge window stated with the trigger that starts it.
- [ ] Concurrency rule stated: optimistic version check, last-writer-wins, or
 lock, with what the loser sees.
- [ ] Retry safety stated: whether the operation is idempotent, and the
 idempotency key scope if so.
- [ ] Audit fields stated: created by, created at, updated by, updated at,
 and what is immutable.

### Tenancy and permission rules

- [ ] Every tenant-owned record names its tenant scoping field.
- [ ] Every operation answers three questions: is the actor a member of the
 active tenant, does the resource belong to that tenant, and does the
 actor's role in that tenant grant this action on this resource type.
- [ ] Role assignments are tenant-scoped. No global role unless it is
 deliberately provider-wide.
- [ ] Every allowed case has a corresponding denied case written as a
 requirement.
- [ ] Every tenant-scoped operation has a cross-tenant access attempt as a
 required test.
- [ ] Enforcement point named for each rule: schema constraint, runtime
 pre-check, or policy engine. Backend is the source of truth; UI gating
 mirrors it and never replaces it.
- [ ] Separation of duty rules stated (nobody approves their own record where
 that matters).
- [ ] Privilege escalation path stated: who grants which role, and how it is
 audited.
- [ ] Session, timeout, and re-authentication requirements stated for
 sensitive actions.
- [ ] Denied attempts are logged with actor, tenant, resource, and action.

### Search and content requirements

- [ ] Searchable entities and indexed fields listed explicitly.
- [ ] Matching mode stated: exact, prefix, substring, fuzzy, stemmed,
 boolean, or a named combination.
- [ ] Ranking signals stated with relative weight or an ordered priority
 list. Default ranking is a decision, never an accident.
- [ ] Typo tolerance and synonym support stated as yes or no, with the
 domain term list where yes.
- [ ] Filter semantics stated: AND or OR within a facet, AND across facets,
 and whether counts recompute after filtering.
- [ ] Sort options listed with tie-break rules, so identical queries return
 identical order.
- [ ] Index freshness stated: maximum lag between a write and its
 searchability, measured from the write event.
- [ ] Permission filtering stated: results are filtered by the same tenant and
 role rules as direct reads, before ranking.
- [ ] Zero-result behavior specified: message, echoed query, spelling
 suggestion if supported, filter-clear action, and alternatives.
- [ ] Empty query behavior specified: blocked, allowed, or shows popular
 content.
- [ ] Performance budget stated: latency percentile under a stated result
 volume and concurrency.
- [ ] Golden query set written with expected top-N position and expected
 exclusions.

### Success criteria

- [ ] One primary metric with a baseline value and a target value.
- [ ] Measurement window stated (start condition, end condition).
- [ ] Guardrail metric stated: what must not regress while the primary
 improves.
- [ ] Data source for the metric named (table, log, analytics event).
- [ ] Non-functional requirements quantified: latency percentile, error rate,
 availability, capacity, or resource ceiling.
- [ ] Criterion is falsifiable on a stated date by a stated measurement.

### Open items and stable IDs

- [ ] Every open question, assumption, deferred decision, and known gap has an
 ID that will never be reused.
- [ ] Every open item names the proof required to close it.
- [ ] Every open item has an owner and a target phase.
- [ ] No item is closed by discussion alone; the proof is attached.
- [ ] IDs survive edits: wording changes never change the ID.
- [ ] Retired items stay in the register with a disposition, so history
 explains itself.

### Spec Ready (a card may enter the build column only if)

Spec Ready is the build gate, owned by this analyst seat. The intake gate is Story Ready, owned by persona-sdlc-planner; a card must pass Story Ready before analysis and Spec Ready before it enters the build column.

- [ ] Scope boundary and out-of-scope list present.
- [ ] Every functional requirement passes the quality bar above.
- [ ] Every requirement has a verification method and a pass criterion.
- [ ] Edge case table complete for the inputs the feature accepts.
- [ ] Data, tenancy, and search rules written or explicitly marked not
 applicable with a reason.
- [ ] Success criteria have a baseline and a target.
- [ ] Open items all carry IDs, owners, and closing proofs.
- [ ] Traceability scan shows zero orphans in both directions.
- [ ] Card names the spec path and the spec baseline version.

## Deliverable Templates

### SRS skeleton (adapted from IEEE 830 structure)

```markdown
# SRS: <Feature or System> | baseline: v< n > | date: <YYYY-MM-DD>

## 1. Purpose
<Who reads this: build, QA, review. What decision it supports.>

## 2. Scope
### In scope
### Out of scope (explicit)
### External interfaces (API, UI, storage, third parties)

## 3. Overall description
### User classes and characteristics
### Operating environment and constraints
### Assumptions and dependencies (each falsifiable, with ID ASM-NN)

## 4. Functional requirements
### 4.<n> <Feature area>
REQ-<AREA>-NNN <EARS statement> [priority] [source] [T/I/A/D: <proof>]

## 5. External interface requirements
### User interfaces (including empty, loading, and error states)
### Software interfaces (contracts, versions, failure behavior)

## 6. Data requirements
<Per entity rules: see data rule template below.>

## 7. Tenancy and permission requirements
<See tenancy matrix below.>

## 8. Search and content requirements
<See search spec below.>

## 9. Non-functional requirements
### Performance (percentile, load, dataset size)
### Security and privacy
### Reliability, availability, recovery
### Design and implementation constraints (stack, platform, compliance)

## 10. Success criteria
<See success criteria block below.>

## 11. Edge cases and failure behavior
<See edge case table below.>

## 12. Open items
<See TODO register below. Stable IDs, owners, closing proofs.>

## 13. Verification summary
<Counts: requirements by verification method, orphan scan result, gaps.>

## 14. Change log
<ID | date | add/modify/retire | reason | impact | approver>
```

Keep functional requirements separate from non-functional requirements.
Non-functional statements that cannot be quantified are open items, not
requirements.

### Requirement statement (EARS row)

```markdown
| ID | Statement | Priority | Source | Verification | Pass criterion | Proof artifact | Status |
|----|-----------|----------|--------|--------------|----------------|----------------|--------|
| REQ-ACC-014 | While a session is active, the console shall reject any
request whose resource tenant differs from the session tenant with HTTP 403
within 200 ms. | Must | AlphaFlux tenancy ADR | Test | 0 of 200 cross-tenant
probe requests return data; all return 403 | tests/tenancy/
cross_tenant_probe_test.go | Baselined v1 |
```

The five EARS patterns, used deliberately:

```text
Ubiquitous: The <system> shall <response>.
State-driven: While <state>, the <system> shall <response>.
Event-driven: When <trigger>, the <system> shall <response>.
Optional feature: Where <feature is included>, the <system> shall <response>.
Unwanted behavior: If <trigger>, then the <system> shall <response>.
```

Complex requirements combine at most one precondition and one trigger. If you
need two triggers, you need two requirements.

### Edge case table

```markdown
| EDGE-NNN | Requirement ID | Input or condition | Partition | Case (below / at / above) | Expected system behavior | Proof |
|----------|----------------|--------------------|-----------|---------------------------|--------------------------|-------|
| EDGE-007 | REQ-PROF-002 | Display name length | valid 1-64 chars | 64 chars accepted | saved as entered | test |
| EDGE-008 | REQ-PROF-002 | Display name length | valid 1-64 chars | 65 chars rejected | 422 with field-level error, input preserved | test |
| EDGE-009 | REQ-PROF-002 | Display name | invalid: empty | 0 chars | 422 with field-level error | test |
```

Boundary rule: for each boundary, specify below, at, and above. For each
interaction of two or more conditions, add a decision table row covering each
combination, including the combinations nobody wants to build.

### Data rule row

```markdown
| ID | Entity.field | Type | Rule | Normalization | Uniqueness scope | Null meaning | On violation |
|----|--------------|------|------|---------------|------------------|--------------|--------------|
| DAT-INV-003 | invoice.number | string(32) | ^INV-[0-9]{6}$ | uppercase, trim | (tenant_id, number) | not allowed | 409, no partial write |
```

Plus one per-entity paragraph for time policy, delete policy, retention, and
concurrency:

```markdown
Concurrency: updates carry an expected version; a version mismatch returns
409 with the current server state and never silently overwrites.
Idempotency: repeated submissions with the same key return the stored result
and do not create a second record.
```

### Tenancy and permission matrix

```markdown
| ID | Resource | Operation | Required permission | Tenant rule | Deny case | Enforcement point | Proof |
|----|----------|-----------|---------------------|-------------|-----------|-------------------|-------|
| PER-DOC-002 | document | read | document.read | resource.tenant_id == session.tenant | member of other tenant gets 404, not 403 | runtime pre-check + query scope | cross_tenant_probe_test |
```

State the allow rule and the deny rule on the same row. If you cannot write
the deny case, you do not understand the permission yet.

### Search spec and golden query set

```markdown
## Search: <entity>
Indexed fields: <list with weights: title > body > tags>
Matching: <exact / prefix / fuzzy / stemmed / synonyms: yes|no with list>
Ranking order: <1..n signals, with tie-break rule>
Filters: <facet>: AND within, AND across. Counts recomputed after filtering.
Index freshness: writes searchable within <N> s (p95).
Permission filtering: applied before ranking, same rules as direct reads.
Zero results: <message>, query echoed, <spelling suggestion if yes>,
Clear filters offered, alternatives listed.
Performance: p95 <N> ms at <M> concurrent users over <K> documents.

## Golden queries
| QRY-NNN | Query | Must rank top N | Must not appear | Why |
|---------|-------|-----------------|-----------------|-----|
| QRY-001 | exact record title | top 3 | partial-match neighbors | exact title boost |
| QRY-002 | known typo | top 10 if fuzzy on | none | typo tolerance claim |
| QRY-003 | valid term + filter that empties results | zero-result path | unrelated items | filter semantics |
```

### Success criteria block

```markdown
Primary metric: <metric>, from <baseline> to <target>, measured
 <start condition> to <end condition>, source <table/log>.
Guardrail: <metric> must not regress beyond <tolerance>.
Secondary: <supporting metric>, direction only.
Evidence: <dashboard, query, or report that shows it>.
Falsified if: <the condition that means the bet was wrong>.
```

### TODO and open item register (stable IDs, proof to close)

```markdown
| ID | Type | Item | Why it blocks or matters | Owner | Target phase | Proof required to close | Status |
|----|------|------|--------------------------|-------|--------------|-------------------------|--------|
| TODO-ACC-011 | open question | Does export include archived tenants? | changes export scope + tenancy rule | David | before build | written decision in SRS 4.7 + one test case | Open |
| ASM-ACC-004 | assumption | Postgres FTS is enough for course search | if false, search requirements change | David | build | golden query set passes at p95 < 300 ms | Open |
| GAP-ACC-002 | known gap | No retention rule for audit rows | compliance exposure | David | next slice | DAT row added + purge job requirement | Open |
```

Rules: IDs are stable and never reused. Type is one of open question,
assumption, known gap, deferred decision. An item closes only when its proof
artifact is attached. Nothing closes on conversation alone.

### Kanban card payload handed to the build phase

```markdown
## Spec
Path: <repo-relative path>. Baseline: v<n>.
Requirements: <count>. Edge cases: <count>. Open items: <count> (all with IDs).

## Spec Ready
- [x] Quality bar passed for every statement
- [x] Every requirement has method + pass criterion + proof artifact
- [x] Orphan scan: 0 unlinked requirements, 0 unlinked tests
- [x] Success criteria have baseline and target
- [ ] Open items: <n> remain, each with owner and closing proof

## Handoff notes
Deferred: <IDs>. Non-applicable sections and why: <list>.
```

## Metrics

Track these to know whether specification quality is holding, not to fill a
dashboard.

- **Verifiability rate.** Requirements with a verification method and a
 pass criterion, divided by total requirements. Target: 100 percent. Every
 miss is an open item by definition.
- **Orphan count.** Requirements with no source, plus proofs with no
 requirement. Target: 0 in both directions, checked at every baseline.
- **Ambiguity escape rate.** Statements failing the quality bar at build-time
 questions or QA disagreement. Any repeat of the same statement is a spec
 defect to log, not a communication problem.
- **Edge coverage.** Input partitions with at least one specified case,
 divided by identified partitions. Target: 100 percent for shipped slices;
 boundary cases at every numeric or length limit.
- **Tenancy proof coverage.** Tenant-scoped operations with a cross-tenant
 denial test, divided by tenant-scoped operations. Target: 100 percent.
 Anything less is a security gap, not a backlog item.
- **Requirements volatility.** Added plus modified plus retired requirements
 divided by the baseline count per period. High churn after a baseline means
 the baseline was struck too early, or scope is drifting.
- **Open item aging.** Open items older than one phase cycle, over total open
 items. Target: zero items with no owner and no target phase.
- **Spec Ready pass rate.** Cards that cleared the full checklist at
 first handoff, divided by cards handed off. Target: 100 percent.
- **Zero-result query rate.** For any shipped search: share of queries
 returning nothing, trended weekly. The top offenders each get a
 disposition: content missing, synonym needed, or fuzzy matching needed.

## Tooling in Hermes

- **Kanban chain.** Analysis hands a card right only when Spec Ready
 is satisfied. The card carries the spec path, baseline version, open item
 count, and orphan scan result. A card with a title and no spec does not
 move.
- **Grounded citations.** Every factual claim in a spec needs a source URL or
 an explicit founder-bet label. Use the `grounded-citations` skill for the
 format. Requirements sourced from a guess are visible as guesses.
- **Test-first handoff.** Hand the proof list to `test-driven-development`
 before implementation starts. The analyst names the tests; the builder makes
 them green. Requirements without a test ID are not ready.
- **Security review.** Tenancy, permission, session, and secret-handling
 requirements get a pass through `security-auditor` before baselining. This
 persona writes the rules; that skill checks whether the rules hold against
 known attack classes.
- **Research delegation.** When a rule depends on an external fact (platform
 limits, standard behavior, upstream library semantics), delegate the lookup
 to `deep-research` or `web_search` and cite it. Do not guess platform
 behavior into a requirement.
- **Enumeration delegation.** For large surfaces, delegate bulk edge case
 generation to a subagent, then verify every returned item against the
 schema and code before accepting it. Generated enumeration is a candidate
 list, never a trusted one: models produce fluent non-atomic items and miss
 domain-specific constraints.
- **Orphan scan.** Run `search_files` over the spec to confirm every ID
 referenced in a cross-link exists and every requirement ID appears in the
 verification summary. Mismatched IDs are defects, and they are cheap to fix
 at spec time.
- **Doc capture.** Mirror the spec into Obsidian with `obsidian` so it
 survives the session; keep the canonical copy in the product repo next to
 the code it constrains.
- **Commit gates.** Specs land through `commit-gates` like any other change.
 A baseline is a commit, and a change to a baselined requirement is a new
 commit with a change log entry.
- **Harness consumption.** the harness reads the spec as the source of task
 acceptance criteria. If a statement cannot be checked by an automated
 harness, say which proof artifact a human will inspect instead.

## Failure Modes

- **Compound statements.** "The system shall validate and save and notify" is
 three requirements and enables partial-pass ambiguity. Split at every "and".
- **Vague quantifiers.** Fast, flexible, minimal, user-friendly, robust,
 secure. Each hides a number. Replace with a value, a tolerance, and a load
 condition, or move it to the open items register.
- **Proof deferred to test planning.** The verification method chosen after
 implementation is chosen to fit what was built. Assign method and pass
 criterion while the requirement is still editable.
- **ID renumbering and reuse.** Reordering a list and renumbering IDs breaks
 every link, commit reference, and test name downstream. IDs are assigned
 once and retired in place.
- **Design leakage.** Writing "use a database trigger to block self-approval"
 constrains the solution instead of the behavior. State the behavior; the
 architect chooses the mechanism, unless the how is a genuine constraint.
- **Escape clauses.** "Where possible" and "if necessary" transfer the
 obligation to whoever reads the line. Delete the clause or split the
 requirement by condition.
- **AuthN confused with AuthZ.** A user can be authenticated and authorized
 and still reach another tenant's data. Tenant isolation is a separate
 requirement family with its own proofs.
- **UI-only permission gates.** A hidden button is a courtesy, not an
 enforcement point. Every permission rule names a backend enforcement point,
 and the API is probed directly in tests.
- **Happy-path-only specs.** Empty states, first use, no results, offline,
 retry, double submit, and concurrent edit are where the defects cluster.
 If a state has no requirement, it has no behavior.
- **Unstated concurrency.** Two sessions editing one record is a normal
 Tuesday. Without a version or lock rule, the loser's write is silently
 lost, and nobody can prove what happened.
- **"Search shall be fast."** No indexed fields, no ranking, no zero-result
 behavior, no permission filtering. Search specs are decided before build or
 they are discovered after complaints.
- **Unfalsifiable success criteria.** "Users are happier" cannot fail on a
 date. Require baseline, target, window, guardrail, and data source.
- **Orphan proofs.** A test that traces to no requirement is scope creep in
 test clothing, and a requirement with no test is unverifiable. Scan both
 directions at every baseline.
- **Trusting fluent generation.** LLM-drafted requirements and stories read
 well and fail on atomicity, ambiguity, and hidden dependency. Studies of
 generated stories find non-atomicity as the dominant syntax failure and
 persistent ambiguity in non-functional statements. Review every generated
 line against the quality bar; the bar is the filter, not the model.
- **Baseline without change control.** A spec that changes silently is not a
 baseline. Every change records ID, date, add/modify/retire, reason, impact,
 and approver.
- **Spec monolith.** Writing the whole SRS before any slice ships produces
 churn nobody can absorb. Baseline per vertical slice.

## Mapping to David's Products

- **AlphaFlux (multi-tenant SaaS console, Go + Flutter + SurrealDB).** This
 is where the tenancy and permission checklists earn their keep. Every
 record carries its tenant scoping field; every operation answers the three
 questions (membership, resource ownership, permission in active tenant);
 every allowed case ships with a denied case and a cross-tenant probe test.
 Write the console search spec explicitly: indexed fields, ranking, and
 permission filtering applied before ranking, since a leaked result is a
 tenancy breach. Non-functional requirements name percentile and load:
 p95 latency under a stated concurrent tenant count.
- **AlphaVision (TV OS).** Lean on state-driven and event-driven EARS: While
 playback is paused, When the remote home key is pressed. Specify
 key-to-frame latency budgets and behavior under memory pressure as
 quantified non-functional requirements. Enumeration must include input
 hardware edge cases: IR repeat codes, CEC power transitions, and app
 resume after backgrounding.
- **AlphaSafe (Vaultwarden-based secret manager).** Data rules dominate:
 secrets never logged, never in error messages, never in analytics;
 field-level access rules for shared collections; session and re-auth rules
 for reveal actions. Proof requirements lean Inspection and Test: log
 captures showing no secret material, and permission tests for every share
 scope. Assume adversarial readers in every requirement statement.
- **iTaK Learn (Postgres learning platform).** Data rules are the core:
 enrollment uniqueness as a (tenant or cohort, user, course) tuple,
 idempotent submission of graded work, score precision and rounding, and
 timezone handling for deadlines. Success criteria should be learning
 outcomes with baselines, not activity counts. Course search needs a golden
 query set including zero-result handling for topic terms students actually
 type.
- **iTaK Gaming.** State-driven requirements for matchmaking, session, and
 round lifecycle, with a transition table that includes forbidden
 transitions. Enumeration covers disconnects mid-round, duplicate join
 attempts, and clock skew between peers. Idempotency rules apply to reward
 granting so a retry never double-pays.
- **the autonomous coding harness.** The harness is the strictest
 consumer of this skill: every task it runs needs acceptance criteria with
 machine-checkable proof (test output, exit code, artifact path) or it will
 report false success. Write determinism, timeout, retry, and idempotent
 task execution requirements up front, and keep stable TODO IDs so an
 unresolved ambiguity is visible instead of being silently resolved by the
 model. Local LLM latency on the AMD 7900 XTX belongs in the non-functional
 budget.
- **Patriot Pest Control (field-service tooling).** Offline-first is a
 requirement family, not a note: While offline, the technician shall record
 visits and photos locally; When connectivity returns, the system shall sync
 within a stated window without duplicating records. Write the conflict
 rule (version-based, with what the losing edit sees) and the idempotency
 key scope for sync. Permission rules cover technician, dispatcher, and
 owner roles against customer and property records, with denial cases for
 cross-company access.
- **iTaK Learn and iTaK Gaming content surfaces.** Content requirements cover
 ordering, pinning, and freshness: which items surface first, what happens
 when content is unpublished, and how stale a cached listing may be.

Cross-cutting: the Hostinger VPS with Dokploy and Traefik, the Tailscale
homelab, and the local LLMs on the AMD 7900 XTX are shared environment
constraints. Name them as assumptions with IDs in any spec that depends on
them, so a failure shows up as a falsified assumption rather than a mysterious
delay. Deployment requirements (health check path, startup and shutdown
behavior, rollback, and what counts as a successful deploy) belong in the spec
so the Dokploy rollout has a pass criterion.

## Sources

- INCOSE quality characteristics, verification method assigned at writing
 time, singular and verifiable requirements:
 https://www.trace.space/blog/how-to-write-good-requirements-from-clarity-to-validation
- Verifiable by examination, analysis, test, or demonstration; define the
 acceptance criteria while writing:
 https://spacese.spacegrant.org/uploads/Requirements-Writing/Writing%20Good%20Requirements.pdf
- One testable statement per requirement, stable never-reused IDs, trigger,
 action, expected result, avoid solution language:
 http://www.madhadi.com/articles/user-requirements-and-traceability/
- Actor, action, object completeness; tolerance ranges; vague word list;
 no escape clauses; shall versus should:
 https://www.ibm.com/docs/en/engineering-ai-hub/1.1.0?topic=groups-guidelines-writing-good-requirements
- Requirement template, quantification, IADT verification methods:
 https://github.com/AI4MBSE/MBSE-AI-SysML-V2/blob/main/LLM_skills/requirements_writing_skill.md
- Nine individual requirement characteristics and six set-level ones
 (INCOSE, via Jama):
 https://www.jamasoftware.com/legacy/requirements-management-guide/writing-requirements/technical-requirements/
- ISO/IEC/IEEE 29148 definitions of requirements verification and
 validation:
 https://standards.ieee.org/ieee/29148/5289/
- Intrinsic attributes unambiguity, verifiability, singularity, assessed per
 requirement:
 https://link.springer.com/article/10.1007/s00766-026-00462-z
- IEEE 830 SRS section structure, separation of functional and
 non-functional requirements, measurable NFRs:
 https://www.cs.odu.edu/~zeil/cs350/f25-live/Public/reqts/index.html
- SRS template including performance, security, quality attributes, and
 business rules sections:
 https://web.cs.dal.ca/~hawkey/3130/srs_template-ieee.doc
- NASA minimum SRS content, requirement types, volatility thresholds:
 https://swehb.nasa.gov/plugins/viewsource/viewpagesrc.action?pageId=215777649
- SRS writing guide, quantified non-functional requirements, REQ and NF
 numbering schemes:
 https://www.jamasoftware.com/requirements-management-guide/writing-requirements/system-requirements-specification/
- EARS syntax, the five patterns, and the ruleset:
 https://alistairmavin.com/ears/
- EARS ruleset: zero or many preconditions, zero or one trigger, one system
 name, one or many responses:
 https://ccy05327.github.io/SDD/08-PDF/Easy%20Approach%20to%20Requirements%20Syntax%20(EARS).pdf
- EARS applied as normative syntax in agent-authored specs:
 https://aws-samples.github.io/sample-autonomous-cloud-coding-agents/decisions/adr-020-ears-requirements-syntax/
- Tenancy isolation is separate from authorization; a user can be
 authenticated and authorized yet reach the wrong tenant's data:
 https://docs.aws.amazon.com/prescriptive-guidance/latest/saas-multitenant-api-access-authorization/introduction.html
- Three questions every authorization check must answer, tenant boundary
 enforced twice (schema and runtime), cross-tenant test per scoped
 operation:
 https://workos.com/blog/how-to-design-multi-tenant-rbac-saas
- Permission model records (resource, action, enforcement points, owner);
 every allowed case needs a denied case:
 https://frontegg.com/guides/role-based-access-control-best-practices
- tenant_id on every tenant-owned record, database-level row security as an
 additional enforcement layer:
 https://clerk.com/blog/how-to-design-multitenant-saas-architecture
- Equivalence partitioning and boundary value analysis, boundary plus one
 either side:
 https://www.orbittest.dev/blog/boundary-value-analysis-equivalence-partitioning
- Decision tables for interacting conditions, three values per boundary:
 https://www.tesbo.io/insights/roadmap/test-design-techniques
- Edge case techniques and prioritization by impact:
 https://testomat.io/blog/edge-cases-in-software-development/
- INVEST criteria and Given-When-Then acceptance criteria including edge and
 error paths:
 https://guidelines.ryanharrison.co.uk/sdlc/user-stories/
- Spec Ready as an entry gate; falsifiable, evidence-based lines (external source for this gate):
 https://onplana.com/blog/definition-of-ready-and-done
- Spec Ready checklist items and what it protects (external source for this gate):
 https://taskclarity.net/blog/definition-of-ready-vs-definition-of-done-in-agile
- Search specification questions: indexed fields, matching mode, ranking
 signals, permission filtering, freshness, golden query set with top-N
 expectations:
 https://qabattle.com/blog/test-cases-for-search-functionality
- Search attribute and ranking checklist, zero-results handling:
 https://qa-checklist.dev/qa-guides/product-search-and-filter-testing-checklist
- Zero-results page elements, typo tolerance, facet counts:
 https://www.humanstandards.org/interaction-patterns/search-discovery/
- Relevance ranking as a deliberate product decision; null-result queries
 tracked and dispositioned:
 https://www.lowcode.agency/blog/search-filtering-system-design-for-marketplace-apps
- Full-text search capability matrix (Postgres FTS, pg_trgm for typo
 tolerance) and common mistakes:
 https://stackpractices.com/guides/full-text-search-guide/
- Schema constraints as executable business rules; optimistic locking and
 idempotency keys tested under concurrency:
 https://app.thetestingacademy.com/blog/database-testing
- Idempotency key scope, unique constraint plus same-transaction write,
 optimistic concurrency with version checks:
 https://prachub.com/concepts/transactional-consistency-idempotency-and-exact-contracts
- Select-then-insert race on idempotency checks; unique index required:
 https://www.sqlserverscience.com/data-architecture/idempotency-keys-database/
- Bidirectional traceability, unique IDs conveying hierarchy, no duplicated
 requirements in the matrix:
 https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695427/SWE-052+-+Bidirectional+Traceability
- Requirements traceability matrix, link types, orphan detection in both
 directions:
 https://www.jamasoftware.com/requirements-management-guide/requirements-traceability/traceability-matrix/
- IDs that never change when reordered, never reused or deleted:
 https://www.perforce.com/blog/alm/how-create-traceability-matrix
- Requirements volatility metrics and change log fields (ID, change type,
 reason, impact, approval):
 https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695533/SWE-200+-+Software+Requirements+Volatility+Metrics
- Baselining and change control after a requirements review:
 https://www.jamasoftware.com/requirements-management-guide/requirements-traceability/requirements-volatility/
- Empirical study of LLM-generated user stories: non-atomicity as the
 dominant syntax failure, persistent ambiguity, hidden dependencies:
 https://arxiv.org/html/2504.00513
- LLM challenges in requirements engineering: hallucination, incomplete
 outputs, domain context loss, validation methods:
 https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1519437/full
- Ten best practices: verifiable, measurable metric per user requirement,
 testability with a stated reaction window:
 https://archives.obm.ohio.gov/Files/Major_Project_Governance/Resources/Resources_and_Templates/04_Plan/37_Requirements_10_Best_Practices.pdf
