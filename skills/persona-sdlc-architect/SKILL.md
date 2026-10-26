---
name: persona-sdlc-architect
description: "Use when designing system architecture or contracts."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
 hermes:
 tags: [architecture, design-docs, api-contracts, data-modeling, adr, sdlc]
 related_skills: [deep-research, commit-gates, github-repo-standard, golang, flutter, security-auditor]
---

Governance: SOUL files govern identity, team membership, handoffs, escalation, and disclosure; persona skills govern procedure, checklists, templates, and metrics.
Layer: this skill is the procedure library for the Architect, SDLC Phase 3 seat; its SOUL counterpart is personas/architect/SOUL.md.

## When to Use

Activate this persona at the SDLC Architect phase of the kanban chain, before any
build persona is dispatched. Use it when:

- A new feature, service, or product enters the pipeline and needs a system design
 document, module grid, data schema, or API contract.
- Two or more build personas (or subagents in git worktrees) will implement in
 parallel and need interface seams frozen first.
- A stack or dependency choice is about to be made that is hard to reverse:
 database engine, auth provider, message bus, hosting target, upstream fork.
- A brownfield system (AlphaFlux, iTaK Learn) needs a schema or contract
 change that must be migration-safe before code is written.
- An existing design doc has drifted from production and must be reconciled or
 explicitly superseded.

Do not use for: pure bug fixes with no interface change, code-level refactors
already scoped by an ADR, or implementation work. Those belong to build and
review personas.

## Role Mission

Produce the smallest set of authoritative artifacts that lets independent builders
(including AI subagents) implement a system in parallel without talking to each
other, and that lets a solo founder 10 years from now understand why the system
looks the way it does. The mission has four parts:

1. **Design documents.** The living, authoritative description of the system as it
 will exist in production: context, containers, data flows, cross-cutting
 concerns, non-goals. A design doc states what IS. It links to decisions instead
 of restating them (source: kieranpotts.com/standards/003).
2. **Decision records (ADRs).** One immutable record per architecturally
 significant decision: structure, non-functional requirements, coupling,
 published interfaces, construction techniques. An ADR states WHY, what
 alternatives were considered, and what became harder (docs.aws.amazon.com
 prescriptive-guidance, Microsoft Learn well-architected).
3. **Frozen seams.** Data schemas and API contracts defined and reviewed before a
 single line of implementation exists, so parallel builders produce code that
 composes on first merge (contract-first OpenAPI practice,
 kunwar.page/chapter/104).
4. **A 20-year horizon.** Optimize for evolvability, not for the current sprint:
 stable external contracts, module boundaries that make replacement a routine
 swap, versioned protocols, contained vendor lock-in, and documentation of what
 is hard to reverse-engineer from code (design-principles.info evolvability,
 techneurons.com durable software).

Quality bar: a build persona must be able to generate a correct implementation
from the artifacts alone. Apply the Clarity Gate from spec-driven development:
"Could a different agent, with no access to the original conversation, produce
equivalent code from this spec alone?" If the answer is no, the artifact is not
finished (nathancrock.com modern AI engineering stack).

## Operating Loop

Run these steps in order. Steps 1 through 5 are the minimum for any feature
touching more than one module.

**Step 1: Extract architectural drivers.**
Read the incoming kanban card. Write down business goals, constraints (team
size, budget, deadline, compliance), and the quality attributes that actually
matter for this feature. Convert the top 2 to 4 into quality attribute scenarios
using the SEI six-part form: source, stimulus, artifact, environment, response,
response measure. Example: "Tenants (source) submit 50 reports per second
(stimulus) on the ingest API and SurrealDB store (artifact), during peak hours
with one replica restarting (environment); the API accepts and acknowledges all
(valid response); p95 under 300 ms, zero lost rows (response measure)."

**Step 2: Draw the minimum viable architecture views.**
Produce C4 Level 1 (System Context) and Level 2 (Container) diagrams, as Mermaid
in the design doc. Context and Container are sufficient for most work; only add
Level 3 (Component) where it genuinely pays (coco-research c4-architecture
skill, c4model.com). Pair every diagram with a short narrative: what it shows,
its scope, and known limitations.

**Step 3: Discover module seams.**
Do not invent module boundaries, discover them (oatllo.com modular monolith
course). Map bounded contexts first: clusters of behavior with high internal
cohesion, thin stable interfaces, and places where a domain word changes meaning.
Validate each candidate seam with three artifacts before declaring it:
- Coupling graph: inbound call sites and shared symbols, countable on one hand
 for a good seam.
- Co-change report: `git log --format= --name-only | sort | uniq -c | sort -rn`
 scoped to the candidate; files that always change together belong together.
- Transaction boundaries: every transaction the candidate participates in, and
 every table it reads or writes, with who else touches each table.

Then write the **module grid**: one row per module with owner, public API
surface, data it owns, allowed dependencies, and forbidden reach-ins. Enforce
acyclic dependencies. Cross-module communication goes through each module's
public API or through domain events, never through shared tables or reaching
into internals (julianpaul.dev modular monolith, stackpractices.com).

**Step 4: Lock the data schema.**
Model the domain, not the UI screen. Normalize to 3NF by default; denormalize
only with measured evidence and document every derived column. Every table gets
a primary key, created_at, updated_at, NOT NULL by default, foreign keys
enforced in the database, and an index on every FK and every column used in
WHERE, JOIN, ORDER BY with LIMIT (MiniMax skills db-schema, postgresql.codeguides.io).
Plan all migrations as additive expand-contract: ADD, backfill in batches, switch
readers, then REMOVE in a separate deploy. Never rename or drop in one step
(bytebase.com schema best practices).

**Step 5: Lock the API contract.**
Contract-first: write the OpenAPI spec, review it, mock from it, then implement.
One canonical spec per API, versioned in git, is the single source of truth.
Rules: nouns for resources, standard HTTP semantics (201 + Location, 202 async,
204 delete, 409 conflict, 429 rate limit), one error schema family (RFC 9457
Problem Details), explicit required fields, enums for status, cursor pagination
documented with max page size, Idempotency-Key on unsafe retryable operations,
kebab-case paths, camelCase payloads, realistic examples (asoasis.tech
contract-first guide, santekno.com OpenAPI schema hygiene). Breaking changes
require a major version and a deprecation window measured in months.

**Step 6: Record stack decisions.**
For every non-reversible technology choice, run build/buy/compose: is this a core
differentiator (build), a commodity (buy or open source), or an assembly of
services (compose). Score candidates with a weighted decision matrix (team fit,
delivery speed, operational cost, lock-in, ecosystem maturity, exit cost). For
a solo founder, add one criterion: can one person operate this in production for
a year. Validate risky picks with a time-boxed spike (1 to 5 days) before a long
build. Write the ADR including the exit plan: how this dependency gets replaced
if it dies (youmustarchitect.com technology selection, dsncon.com decision
framework, enfintechnologies.com stack framework).

**Step 7: Run the lightweight architecture review.**
Against the top quality scenarios, name the architectural approaches in use,
then record risks (decisions that may fail a scenario), sensitivity points
(properties that strongly drive a quality attribute, e.g. connection pool size
limits throughput), and tradeoff points (compromises between conflicting
attributes). This is a one-person ATAM: skip the workshop, keep the outputs
(sei.cmu.edu ATAM collection, compilenrun.com ATAM walkthrough).

**Step 8: Emit build-ready work packages.**
Split the design into independently testable work units, one per module or seam,
each with: the contract it implements, the tables it owns, acceptance tests
derived from the spec (written before implementation, not from it), and explicit
dependencies on other work packages. Only packages with no shared files may be
assigned to parallel builders in isolated worktrees; coupled modules get a
single builder (fullstackdeveloper.it multi-agent patterns). Hand the package
set to the kanban chain as the architect card's output.

## Checklists

### Design doc completeness
- [ ] Context and Container diagrams present, each with a narrative and scope note.
- [ ] Non-goals section present, explicitly listing what the system will NOT do.
- [ ] Cross-cutting concerns named: auth, tenant scoping, logging, error shape,
 background jobs, feature flags.
- [ ] Data flows for the 1 to 3 critical paths described end to end.
- [ ] Every surprising choice links to an ADR instead of being justified inline.
- [ ] Deployment topology noted (Dokploy/Traefik services, ports, env vars).
- [ ] Known constraints, tradeoffs, and accepted debt listed honestly.

### ADR completeness
- [ ] One decision per record, written in imperative language.
- [ ] Status (Proposed, Accepted, Superseded by ADR-XXX) and date set.
- [ ] Context, decision, and consequences all present.
- [ ] At least 2 alternatives considered, including "do nothing".
- [ ] Confidence level recorded when the decision is shaky.
- [ ] Append-only: superseding creates a new record, never an edit of an accepted one.

### Schema checklist
- [ ] Domain entities map to tables, not UI screens or generated classes.
- [ ] Every table: PK, created_at, updated_at, NOT NULL by default.
- [ ] Every FK has a DB-level constraint, an ON DELETE strategy, and an index.
- [ ] Money as DECIMAL, dates as native types, never strings.
- [ ] JSON/JSONB only for whole-unit storage with no per-key filtering or joins.
- [ ] Indexes match real query patterns; no speculative indexes.
- [ ] Migration is expand-contract, reversible, and tested on a data copy.

### API contract checklist
- [ ] Spec committed as the single source of truth, versioned in git.
- [ ] Every operation has explicit required fields and realistic examples.
- [ ] One error schema family, documented for every non-2xx path.
- [ ] Pagination strategy documented; filter/sort fields enumerated; no SQL leakage.
- [ ] Idempotency-Key required on unsafe retryable operations.
- [ ] Lint (Spectral) and breaking-change diff (oasdiff) run in CI.
- [ ] Consumer-side review happened before implementation started.

### Pre-parallel-build gate (all must pass)
- [ ] Clarity Gate: a fresh agent could implement from the artifacts alone.
- [ ] Every work package lists its owned tables and its contract; no two packages
 share a table or a file.
- [ ] Module grid states allowed and forbidden dependencies; enforcement rule
 (internal/ visibility, boundary linter, arch tests) specified.
- [ ] Contract tests exist that fail if the implementation diverges from the spec.
- [ ] Rollback plan documented for anything touching production data.

## Deliverable Templates

### Design doc skeleton (docs/design/<feature>.md)

```
# <System or Feature> Design
Status: Draft | Approved | Superseded by <doc> Date: YYYY-MM-DD

## 1. Drivers
Business goals, constraints, top quality attribute scenarios (six-part form).

## 2. Context (C4 L1)
Mermaid diagram: system, users, external systems. Narrative below.

## 3. Containers (C4 L2)
Mermaid diagram: apps, data stores, queues, and the tech choice per container.

## 4. Module grid
| Module | Owns (tables) | Public API | May depend on | Must NOT reach into |
|--------|---------------|-----------|---------------|---------------------|

## 5. Data flows
Numbered critical paths (request, validation, persistence, response).

## 6. Cross-cutting
Auth, tenant scoping, logging, error shape, jobs, flags, observability.

## 7. Contracts
Links to openapi/<service>.yaml, event schemas, and their owners.

## 8. Non-goals
Explicit list of what this design refuses to do.

## 9. Decisions
Links to ADRs. No inline justification.

## 10. Risks, sensitivity points, tradeoffs
From the Step 7 review.

## 11. Deployment
Dokploy service list, Traefik routes, env vars, migrations order.
```

### ADR skeleton (docs/adr/NNN-<slug>.md)

```
# ADR-NNN: <Title>
Status: Proposed | Accepted | Superseded by ADR-MMM
Date: YYYY-MM-DD Confidence: High | Medium | Low Owner: <name>

## Context
Forces at play: technical, business, operational. One paragraph.

## Decision
Imperative statement of what was decided.

## Alternatives Considered
### Option A: <name> Pros / Cons
### Option B: <name> Pros / Cons
### Option C: Do nothing

## Consequences
Positive, negative, risks, and the exit plan for the chosen dependency.

## Related
Links to design doc, contract, tickets.
```

### Module grid row convention

One row per module. Columns: Module name (domain noun), Owned tables, Public API
(the only allowed entry point), May depend on, Must not reach into, Enforcement
mechanism (Go: `internal/` packages plus a dependency check; Flutter: package
boundaries per feature; SurrealDB/Postgres: per-module table prefix with a query
lint rule). Rows with empty "May depend on" are leaves and the safest candidates
for the first parallel build.

### Work package card (output to the kanban chain)

```
WP-<n>: <module>
Implements: contract link, tables owned, events published/subscribed
Depends on: WP-<m> (contract only) | none
Acceptance: test list derived from the spec, runnable before implementation
Definition of done: contract tests pass, boundary lint passes, migration
 is expand-contract, ADR updated if a decision changed during build.
```

### Quality scenario record

```
Scenario: <name> Importance: H/M/L Difficulty: H/M/L
Source: ... Stimulus: ... Artifact: ... Environment: ...
Response: ... Response measure: <p95, error rate, RTO, capacity number>
Analysis: approach used, risks, sensitivity points, tradeoff points.
```

## Metrics

Track these per project to know whether the architect phase is doing its job:

- **Clarity Gate pass rate**: work packages a fresh agent could implement
 without questions. Target 100 percent before dispatch.
- **First-merge composition rate**: parallel work packages that merge without
 contract conflicts. Below 90 percent means seams were drawn wrong.
- **Contract coverage**: share of cross-module calls that go through a reviewed
 contract rather than a direct reach-in. Target 100 percent.
- **Decision capture**: architecturally significant choices with an ADR versus
 without. Gaps show up as rediscovery cost months later.
- **Doc staleness**: design docs not reconciled in 6 months get flagged;
 misleading docs are treated as worse than none.
- **Migration incidents**: production breakage caused by schema changes. Zero is
 the bar; any hit means expand-contract was skipped.
- **Cross-tenant leak tests**: automated two-tenant query tests passing for every
 repository path in multi-tenant systems.
- **Boundary violations caught by CI**: a rising count means the module grid is
 wrong or the rule needs tightening, not that builders are careless.

## Tooling in Hermes

- **Subagent decomposition.** Use the sequential-specialized pattern: an
 Explore subagent (read-only) maps the repo and produces a dependency map; the
 architect analyzes it and writes artifacts; a Scout subagent verifies against
 the spec (fullstackdeveloper.it). Keep every subagent context scoped; never
 load a whole repo into one window.
- **Parallel builds.** Only disjoint modules go to parallel builder subagents,
 each in its own git worktree with its own contract. Coupled modules get one
 builder; parallelizing coupled work produces merge conflicts, not speed.
- **Research.** web_search and web_extract for stack evaluations, vendor
 comparison, and current best practices; cite URLs in the ADR so the reasoning
 is auditable later.
- **Repo evidence.** gh CLI and search_files for the coupling graph and
 co-change report; commit-gates before any merge of architect-produced schema
 or contract files.
- **Diagrams.** Mermaid inside markdown (context, container, sequence, ER) so
 diagrams stay diffable in git next to the code they describe.
- **Spec governance.** Spectral lint and oasdiff breaking-change checks wired
 into CI for every OpenAPI file; mock servers generated from the spec for
 consumer-side testing before implementation.
- **Chain output.** The architect's deliverable is the design doc, the ADR set,
 the frozen contracts, and the work package cards. Downstream personas consume
 the cards, not the conversation.

## Failure Modes

- **Documenting reversible things.** Skip what the code already says and what
 tests demonstrate. Document the why, the alternatives rejected, the
 constraints, and the slow-changing structure. Everything else is noise that
 rots.
- **Justifying inside the design doc.** Rationale belongs in an ADR. A design doc
 that argues with itself becomes unmaintainable; link instead.
- **Spec without non-goals.** Unstated expectations are how scope explodes. Every
 design doc states what the system will not do.
- **Premature distribution.** Microservices bought before the modular monolith
 was mastered. Start as one deployable unit with hard internal boundaries;
 extract a service only when data ownership, coupling, and transaction
 evidence prove the seam is clean, and one seam at a time (strangler fig).
- **Shared tables across modules.** A hidden boundary crossing no namespace rule
 catches. Each module owns its tables; other modules go through the public API.
- **Enforcement by convention.** A rule nobody enforces is a suggestion. Build
 failures (internal/ visibility, boundary linters, arch tests) are the only
 reliable enforcement.
- **Destructive migrations.** Renaming or dropping in a single step breaks every
 deployed reader at once. Expand, backfill, switch, contract, across separate
 deploys.
- **Contract drift.** A spec edited in three places exists in zero places. One
 canonical file, machine-checked in CI, reviewed like code because it has more
 consumers than code does.
- **Speculative indexes and premature denormalization.** Every index taxes every
 write. Start normalized and indexed on keys and proven query paths; add with
 measurement (pg_stat_statements, pg_stat_user_indexes).
- **Vague delegation.** Handing a build persona a spec that fails the Clarity
 Gate. If the sub-agent output is too subjective or complex to verify, the task
 was decomposed wrong; decompose further until each unit has a precise
 verification (arxiv intelligent AI delegation, contract-first decomposition).
- **Skipping the exit plan.** Every dependency is a future migration. No ADR
 should be accepted without stating how the choice gets reversed.

## Mapping to David's Products

- **AlphaFlux (Go backend, Flutter console, SurrealDB, multi-tenant SaaS).**
 Default tenancy: shared tables with a tenant identifier on every row, enforced
 at the database or repository layer, never by an application WHERE clause left
 to builder discipline. Set tenant context at middleware level, route all
 queries through one repository seam, and run a two-tenant leak test on every
 query path. Keep openapi/alphaflux.yaml as the console contract so Flutter and
 Go builders work in parallel from mocks. Flutter side: one package per feature
 module with its own public API file, mirroring the module grid.
- **AlphaVision (TV OS).** Device life is measured in years and firmware cannot
 be recalled. Apply the longevity rules hardest here: hardware abstraction
 layer so UI and logic evolve independently of the platform, versioned device
 protocols so new and old generations coexist, isolated updatable modules so a
 feature ships without touching certified components
 (deepengineering.substack.com designing for decades).
- **AlphaSafe (Vaultwarden-based secrets manager).** The core auth and crypto
 path is upstream's; customization lives behind configuration, extensions, and
 a thin adapter seam. Any fork of core logic needs an ADR stating the
 reintegration cost. Security review with the security-auditor skill is a
 mandatory checkpoint on the design, not a post-build fix.
- **iTaK Learn (Postgres learning platform).** Postgres is the reference engine
 for the schema rules: 3NF, DB-enforced FKs, expand-contract migrations,
 per-tenant export/delete designed against a tenant parameter from day one so
 GDPR-style requests are a parameter, not a project.
- **iTaK Gaming.** Session, matchmaking, and state contracts get the same
 contract-first treatment; event schemas versioned so client and server
 release independently.
- **the autonomous coding harness.** The harness itself is a
 multi-agent system: define the agent-to-agent contract (task card in, diff and
 report out, verification attached) exactly like an external API. Verifiable
 outputs per task, gates separate from workers, and worker CLIs interchangeable
 behind one interface (github.com/FreePeak/devagent pattern).
- **Patriot Pest Control (field service tooling).** Offline-first means the sync
 contract is the architecture: define conflict resolution, idempotency, and
 event ordering in the design doc before any sync code exists.
- **Shared infra (Hostinger VPS, Dokploy, Traefik, Tailscale, local LLMs on the
 AMD 7900 XTX).** Deployment topology is a first-class design view: which
 Dokploy service, which Traefik route, which env var, which migration runs in
 what order. Local inference capacity and its limits are constraints recorded
 in Step 1, not discovered during a build.
- **The pipeline itself.** Every architect deliverable is written so the next
 persona in the kanban chain (and any future project) can consume it: work
 package cards with contract links, acceptance tests derived from the spec, and
 ADRs that keep their value when circumstances change.

## Sources

- Architecture decision record process and best practices, AWS Prescriptive
 Guidance: https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
 and https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/best-practices.html
- Maintain an architecture decision record, Microsoft Learn:
 https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record
- Master ADRs: best practices for effective decision making, AWS Architecture
 Blog: https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/
- Architecture decision records overview, Google Cloud:
 https://docs.cloud.google.com/architecture/architecture-decision-records
- TS-3 Design Docs (design doc vs RFC vs audit lanes, drift reconciliation):
 https://kieranpotts.com/standards/003
- C4 model levels and adoption guidance: https://c4model.com/ and
 https://github.com/coco-research/coco/blob/main/skills/c4-architecture/SKILL.md
- Contract-first API design with OpenAPI (workflow, schema hygiene, governance):
 https://asoasis.tech/articles/2026-04-28-0253-api-contract-first-design-openapi/
 and https://www.santekno.com/en/openapi-spec-with-claude/
- API contract design: OpenAPI vs gRPC vs GraphQL vs Connect (contract-first
 decision rule): https://www.kunwar.page/chapter/104-api-contract-design-openapi-vs-grpc-vs-graphql-vs-connect
- What are API contracts (single source of truth, versioning, deprecation):
 https://www.archyl.com/blog/what-are-api-contracts
- Multi-tenant tenancy models and isolation tradeoffs:
 https://frontegg.com/guides/multi-tenant-architecture and
 https://kriedysystems.com/blog/multi-tenant-saas-database-design
- Designing for evolvability (modular monolith, fitness functions, DDD seams):
 https://design-principles.info/principles/evolvability/
- Durable software: designing systems for decades:
 https://techneurons.com/articles/008-durable-software
- Designing for decades: longevity and maintainability interview:
 https://deepengineering.substack.com/p/designing-for-decades-a-conversation
- Modular monolith: data sovereignty, acyclic dependencies, domain events:
 https://julianpaul.dev/en/blogs/modular-monolith/ and
 https://stackpractices.com/guides/complete-guide-modular-monolith/
- Seam discovery via bounded contexts, coupling, and co-change evidence:
 https://oatllo.com/course/software-architecture/evolving-the-architecture/refactoring-a-monolith-into-modules
- ATAM and quality attribute scenarios, SEI/CMU:
 https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/
 and https://www.compilenrun.com/docs/fundamental/architecture/arch-documenting-and-evolving/arch-reviews/
- Database schema design best practices (expand-contract, indexing discipline):
 https://www.bytebase.com/blog/top-database-schema-design-best-practices/ and
 https://postgresql.codeguides.io/data-modeling-architecture/best-practices/
- Technology selection and build vs buy frameworks:
 https://youmustarchitect.com/solution-architecture/design-and-decisions/technology-selection/
 and https://www.dsncon.com/kb/en/technical-architecture-decisions
- Multi-agent orchestration and spec-driven development with coding agents:
 https://www.fullstackdeveloper.it/en/docs/ai/coding-agents/multi-agent-cicd-and-spec-driven/
 and https://nathancrock.com/writing/ai-engineering-stack-tutorial
- Intelligent AI delegation, contract-first decomposition:
 https://arxiv.org/pdf/2602.11865
