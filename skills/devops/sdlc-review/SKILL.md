---
name: sdlc-review
description: Review Kanban handoffs and route verified outcomes.
version: 1.1.0
author: Jakub Wolniewicz (@frizikk) + Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, review, quality, verification]
    category: devops
    requires_toolsets: [kanban]
environments:
  - kanban
---

# SDLC Review Skill

Independently verify work handed from a Kanban implementation run to the review lane, then approve it, request changes, or escalate. This skill reviews the deliverable and its evidence; it does not take over the implementer's work.

## When to Use

Use this skill when all of the following are true:

- the dispatcher spawned you for a task claimed from the `review` lane;
- an implementer submitted a `review_requested` handoff;
- the task needs an independent verdict before it can be completed.

Do not use it for a separate downstream review card. A downstream card is ordinary implementation work with a review-oriented specification and completes through its own lifecycle.

## Prerequisites

- A Kanban worker context with the current task and run identifiers.
- Native Kanban tools: `kanban_show`, `kanban_comment`, `kanban_complete`, `kanban_request_changes`, and `kanban_block`.
- Workspace access through `read_file`, `search_files`, and `terminal` when the deliverable is code.
- The task's original specification, acceptance criteria, handoff summary, and prior run history must be available through `kanban_show`.

## How to Run

This skill is loaded automatically by the review dispatcher. Start with `kanban_show` before inspecting files or choosing a verdict.

1. Read the task specification and the latest `review_requested` handoff.
2. Inspect the actual deliverable and run relevant verification.
3. Choose exactly one verdict: approve, request changes, or escalate.
4. Record concrete evidence in the terminal Kanban transition.

## Quick Reference

| Verdict | When | Final action |
|---|---|---|
| Approve | Acceptance criteria and verification pass | `kanban_complete` |
| Request changes | Correctable implementation defects remain | `kanban_comment`, then `kanban_request_changes` |
| Escalate | A human decision or external prerequisite is required | `kanban_block` |

A requested-changes transition returns the task to its original implementer. When that implementer requests review again without naming a reviewer, the persisted reviewer provenance routes the re-review back to the same reviewer profile.

## Review Lenses

Vary how you look at the work on each round instead of repeating the same inspection. Decorrelated lenses catch different defect classes: a cold read of the artifact surfaces design and correctness problems that the implementer's narrative would have framed away, execution surfaces claims that do not reproduce, and a strict contract audit surfaces quiet scope drift. Repeating the round-1 lens on round 3 mostly re-finds what round 1 already found.

Determine the current round from the history the task record already gives you: count the `changes_requested` entries in the "Prior attempts on this task" section of your worker context (also visible as prior runs in `kanban_show`). The current review round is that count plus one. Round 1 therefore shows zero `changes_requested` attempts; round 2 shows one; and so on.

| Round | Lens | How to apply it |
|---|---|---|
| 1 | Artifact | Read the diff or deliverable cold, before the implementer's summary. Form an independent judgment, then compare it against the handoff narrative and investigate every mismatch. |
| 2 | Execution | Check out the work and actually run it via `terminal`: build, test, and exercise the reported behavior yourself. Verify each handoff claim empirically instead of re-reading the artifact. |
| 3+ | Contract | Re-read the ORIGINAL task body and acceptance criteria, then audit the deliverable strictly against them. Also verify that every item from every prior `kanban_request_changes` round actually landed. |

The baseline duties in the Procedure section still apply on every round; the lens sets which inspection you lead with and weight most heavily.

### Lens variation for ad-hoc review fan-outs

The same principle applies outside the Kanban review lane. When spawning multiple parallel reviewers via the delegation tool, give each reviewer a different lens - one diff-only brief, one full-context brief, one checkout-and-run brief - rather than identical briefs. Identical briefs produce correlated verdicts and duplicate findings; varied briefs cover more defect classes for the same review spend.

### The standing consensus critic (cross-cutting)

Lens variation is operationalized as a reusable gate: a `critic` profile that ANY phase's output can be routed to - a builder module, a tester QA pass, a researcher packet, an analyst SRS, an architect design, a marketing claim, a UX surface. It is not confined to the review lane; it is a cross-cutting critic that attaches to work wherever it lands.

Protocol it runs on every task: fan out exactly THREE independent critic subagents in one delegation batch, each attacking the SAME artifact through a DIFFERENT lens, then aggregate the three verdicts. Never give two critics the same lens; identical briefs defeat the point.

Aggregate into three buckets, and report them as such:
- **Unanimous** (all three found it): highest confidence, act first.
- **Majority** (exactly two of three): solid, act, note the one that missed it.
- **Lone-wolf** (exactly one): flag for human review, name which lens saw it, never drop it and never treat it as proven - a single lens can catch a real defect the others structurally cannot.
- Wild disagreement on whether the artifact is sound is itself the headline; surface it, let a human decide.

Lens selection by artifact type (route on the artifact, not the phase):

| Artifact | Three lenses |
|---|---|
| Code, API, schema, architecture, infra config | `critic-lens-code` + `critic-lens-claims` + `persona-skeptic` (sub `security-auditor` for a security-heavy diff) |
| Research, market, competitor claims, SRS, plan | `critic-lens-claims` + `critic-lens-growth` + `persona-skeptic` |
| UX, web, app, generated site, design | `critic-lens-ux` + `critic-lens-claims` + `persona-skeptic` |
| Marketing, ads, pricing, funnel | `critic-lens-growth` + `critic-lens-claims` + `persona-skeptic` |

To task it: `kanban_create(assignee="critic", ...)` with a body that names the artifact's location and states the artifact's own claims as the hypothesis to attack. The full execution protocol lives in the critic profile's SOUL.md; this section is the routing and aggregation contract for whoever tasks it. The critic reviews and reports only - it never edits the artifact, so role separation holds.

Pitfall: a "persona" the user says they created may be a SKILL, not a spawnable PROFILE. Kanban dispatches to a profile (the assignee must name a real profile directory with `config.yaml` + `SOUL.md`); skills are force-loaded into a run via `kanban_create`'s `skills` param. Before wiring a task to a new role, confirm the profile exists on disk; if only the skill exists, either assign an existing profile and force-load the skill, or build the profile (config cloned from a peer, plus a SOUL) first.

## Routing a red-gate NO-GO (orchestrator side)

When a phase hands back a NO-GO that blocked itself awaiting a fix-vs-accept call, route it on the board in this order. The fix-vs-accept decision rule itself (who may accept, and that a disclosed red is not an accepted one) lives in the commit-gates skill; this is the mechanics.

1. **Read the consensus before choosing.** If a critic panel adjudicated the findings, unanimous and majority findings justify the fix axis on their own. Lone-wolf findings go into the card as second-tier items to report on, never into the required scope: a single lens has not earned a mandatory fix.
2. **Card the fix pass.** `kanban_create(assignee="<implementer profile>")` with every required finding named by id plus its file:line, the regression test each fix must carry in its own commit, and the hard limits stated outright: no deploy, no push, do not touch the blocked card or the next phase, do not edit the review reports.
3. **Gate the downstream cards on it before unblocking anything.** `kanban_link(parent=fix_card, child=<re-test card>)` and `kanban_link(parent=fix_card, child=<deploy card>)`. The deploy card then needs BOTH the re-test and the fix done, so a red gate cannot be routed around.
4. **Unblock only after the link exists.** `kanban_unblock(re-test card)` moves it from `blocked` to `todo` while the fix parent is open, and it auto-promotes to ready when the fix lands. Unblock first and the re-test spawns immediately against unfixed code, burning a full run to re-report findings that are already on the card.
5. **Record the decision as a comment on the blocked card**: what was decided, the fix card id, and the corrections from review the re-test must carry (overstated sub-claims, mislabeled evidence) so the re-test verifies rather than repeats.
6. **Verify by re-reading, never by trusting the acks.** `kanban_show` the deploy card and confirm `unsatisfied_parents` actually lists both parents; `kanban_list` the re-test card and confirm the new parent id is present and the status is `todo`. A `link` or `unblock` returning ok only means the write was accepted, not that the gate holds.

Pitfall: leaving a completed re-test's predecessor in `blocked` with no new parent means nothing ever promotes it again, and the pipeline stalls silently at the same spot it just escaped. Every card you unblock needs its next parent linked first, or a follow-up scheduled to unblock it.

### Sequencing extra fix passes after one is already running

Authorized scope usually grows after the first fix card is dispatched. Carry it as cards, never as edits to a running card:

- **Same files get sequenced.** A follow-up pass over the same repo is created with `parents=[<running fix card>]` so it starts only after that pass lands. Two cards editing one tree at once produce conflicting edits and commits that fight.
- **The re-test gates on it too.** Link the follow-up as a parent of the re-test card as well. Gate only the first pass and the re-test fires while the rest of the findings are still in the tree, spends a full run, and reports them again as failures.
- **Different repos run in parallel.** Ownership is per repo and file tree, not per profile: two passes over two different repos never conflict even when both are assigned to the same profile.

```text
kanban_create(title="fix pass B: <remaining findings>", assignee="<implementer>", parents=["<running fix pass>"])
kanban_link(parent="<fix pass B>", child="<re-test card>")
kanban_show("<re-test card>")   # parents must list BOTH fix passes before you move on
```

Pitfall: do not extend a running card by comment for scope that has to land. A worker's context is built when the dispatcher spawns it, so a comment added mid-run is seen only if that worker happens to re-read its own card, which most never do. Comment before the card starts, or card a follow-up; when the next phase must act on the scope, the parent link is the only guarantee.

### Reading a broad authorization

When a narrow question comes back as "fix it all", split the backlog by reversibility rather than by size:

- **Card without asking again:** code fixes with their regression tests, repo-side dependency and base-image bumps, read-only scans and audits, and anything that can only reach production through a phase that is already gated.
- **Name for an explicit yes, one line and a recommendation each:** history rewrites, credential rotation, production data deletion, host changes that bounce every container, and anything touching the network edge. Broad wording is not authority for these.
- **State the axis you took.** When a decision is waiting on the user and one direction needs nothing from them, take that direction, then say plainly which one you took and how to reverse it.

## Procedure

### 1. Orient from the durable task record

Call `kanban_show` and identify:

- the original task body and acceptance criteria;
- the latest implementation summary and structured metadata;
- changed files, commit identifiers, and test evidence;
- comments and decisions from earlier runs;
- findings from prior review rounds.

Treat the handoff as a claim to verify, not as proof that the work is correct.

### 2. Compare requested behavior with delivered behavior

Map every acceptance criterion to concrete implementation or output evidence. Note omissions, changed semantics, and unrelated scope before deciding whether to run deeper checks.

For code work:

1. Use `read_file` and `search_files` to inspect the changed paths and their callers.
2. Use `terminal` to inspect the diff and run the project's existing focused tests, lint, type checks, or build commands.
3. Exercise the reported failure path and at least one ordinary control path when practical.
4. Check error handling, edge cases, concurrency boundaries, data preservation, security boundaries, and cross-platform behavior relevant to the change.
5. Confirm that tests assert behavior rather than merely snapshotting source text or constants.

For non-code work:

1. Inspect the complete deliverable rather than only its summary.
2. Check correctness, completeness, formatting, and provenance.
3. Validate referenced URLs or external facts with the appropriate native tools when they affect the verdict.

### 3. Choose one verdict

#### Approve

Approve only when the acceptance criteria are satisfied and the evidence is sufficient. Call:

```text
kanban_complete(
    summary="Reviewed and approved. <what was verified>",
    metadata={"review_outcome": "approved", "reviewer_checks": [...]}
)
```

Include the exact checks that passed and any bounded caveat that does not block acceptance.

#### Request changes

Use this for specific, correctable defects. First record actionable findings:

```text
kanban_comment(
    task_id="<current-task-id>",
    body="Changes requested:\n1. <file or artifact + defect>\n2. <required correction>",
)
```

Then return the same task to its implementer:

```text
kanban_request_changes(
    reason="<concise summary of the required corrections>"
)
```

State where the defect is, how it reproduces, why it violates the task, and what minimum outcome would resolve it. The transition does not use blocker recurrence accounting.

#### Escalate

Use escalation only when the reviewer and implementer cannot resolve the problem without a human decision or external prerequisite:

```text
kanban_block(
    reason="escalation: <decision or prerequisite required>"
)
```

Explain the blocked decision and the smallest information needed to continue.

### 4. Preserve role separation

Do not edit the implementation while acting as reviewer. Request changes and let the implementer produce the next candidate; then independently verify that candidate in the next review run.

## Pitfalls

- **Rubber-stamping:** A passing handoff summary is not independent evidence.
- **Reviewer implementation:** Editing the deliverable hides ownership and weakens the re-review boundary.
- **Vague findings:** “Needs work” does not give the implementer a reproducible correction target.
- **Style-only blocking:** Do not request changes for preference-level nits when behavior and repository standards are satisfied.
- **Skipping prior rounds:** Re-review must confirm both the requested corrections and preservation of previously passing behavior.
- **Using blockers for ordinary rework:** Correctable defects belong in `kanban_request_changes`; reserve `kanban_block` for genuine external blockers or human decisions.
- **Completing without evidence:** Every approval summary must name the checks or artifacts actually inspected.

## Verification

Before submitting the verdict, confirm:

- [ ] `kanban_show` was read for the current task and run.
- [ ] Every acceptance criterion was mapped to evidence.
- [ ] The actual deliverable was inspected.
- [ ] Relevant focused checks were run or an explicit reason was recorded when execution was impossible.
- [ ] Prior requested changes were re-tested on re-review.
- [ ] Unrelated regressions and scope changes were considered.
- [ ] The verdict uses exactly one terminal action.
- [ ] The summary contains concrete, non-secret evidence.
- [ ] No implementation files were edited by the reviewer.
