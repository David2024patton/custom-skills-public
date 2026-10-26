---
name: domain-fanout
description: "Use to spawn a fresh agent when the domain changes."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
  hermes:
    tags: [delegation, context-partitioning, subagents, fanout, handoff, isolation]
    related_skills: [hermes-harness, persona-sdlc-builder, language-knowledge, qa-loop, exec-scripts]
---

# Domain Fan-Out: one clean context per domain

## When to Use

The moment a task crosses into a new domain whose knowledge is heavy (a language library digest, a big research brief, a whole new stack) and the current context no longer needs what it is carrying, do NOT load the new domain into THIS window. Spawn a fresh agent for it, hand it only what it needs, and bring back the result. This is what keeps one window from stacking Rust + Mojo + marketing digests until it blows the 1M budget.

Trigger: "I now need <language/domain> work and it is not what this context is for." Load `language-knowledge` to see the digest sizes; anything that does not fit with headroom is a spawn, not a load.

## The lean-orchestrator rule

The orchestrator (the agent that owns the whole task) holds the PLAN, the INTERFACES, and the DECISIONS. It never holds a domain digest or a full research brief. Heavy knowledge lives in the child that needs it, and dies with the child. This is the entire point: the orchestrator's window stays small no matter how many domains the job touches.

## How to spawn (the contract)

Use `delegate_task`. The brief must be self-contained because the child sees NONE of this conversation:

**Send (the brief):**
- Goal, stated in the user's terms and the outcome wanted.
- File/scope boundary the child must not leave.
- Frozen interfaces it builds against: API schemas, types, contracts, so it integrates without guessing.
- Decisions already made, so it does not re-litigate them.
- The ONE domain skill/digest to load in ITS own window (e.g. "load `rust` knowledge digest", "load `mojo` skill").
- The exact output shape expected.

**Get back (the return):**
- The result itself: the code, the findings, or the decision.
- Evidence: commands run with real output, sources cited, tests executed. Never a claim without proof.
- Anything it learned that the parent does not know.
- Open questions and what it could not do (so gaps do not hide).

Return a structured JSON result (output_schema) when the parent needs to merge or count findings; plain prose when it does not.

## The chain (domain shift: Rust, then Mojo, then marketing)

One domain at a time, each in its own child:

1. Orchestrator holds the plan, not the digests.
2. Needs Rust? Spawn child A; A loads the `rust` digest in ITS window, does the Rust work, returns a compact result.
3. Now needs Mojo? Spawn child B with A's relevant output in the brief; B loads the `mojo` skill in ITS window, does the Mojo work, returns.
4. The orchestrator integrates A + B, then continues or spawns the next.

Results pass THROUGH the orchestrator (hub-and-spoke), carrying only the relevant slice forward. A's Rust digest never enters the orchestrator's window; B's Mojo digest never enters A's. Each is born, works, hands off, and is discarded.

## Sharing context back and forth

- **Transient domain work:** hub-and-spoke as above. The child returns, the parent relays the slice to the next child. This is the default.
- **Persistent peers:** for two persona BOTS that need to talk back and forth live (skeptic ↔ builder, researcher ↔ ideator), use Bot Mode group chats or kanban comments. Bots are profiles and message each other natively; that is true peer-to-peer, unlike transient subagents.
- **Durable handoff:** anything that must survive the session goes to a file or a kanban card (QA-LOOP artifacts), not to chat alone.

## The constraint, stated plainly

A transient subagent CANNOT spawn its own children and CANNOT message a peer directly (Hermes limits `delegate_task` to the orchestrator). So when a child discovers it needs another domain, it reports that need in its return, and the orchestrator spawns the next child. Do not design a pattern that assumes nested spawning; design every brief so the orchestrator can chain them.

## The rule that keeps quality

Every spawned agent still runs its own gates: the critic checklist, execution-first, evidence-with-proof (see `qa-loop` and `exec-scripts`). Fan-out partitions CONTEXT, never ACCOUNTABILITY. The orchestrator still verifies each return before integrating it; a child's completion report is a claim until re-checked.

## Example

Build a feature that touches a Go API and a Mojo GPU kernel:

1. Orchestrator: plan + the Go/Mojo interface contract. No digests loaded.
2. Spawn Go child: "Implement the API handler in <files>; load the `go` digest; return the diff + `go test` output."
3. Spawn Mojo child: "Implement the kernel behind this seam: <contract>; load the `mojo` skill; return the kernel + run output."
4. Orchestrator re-runs both evidences itself, integrates, then spawns the critic for the full slice.

Neither digest reached the orchestrator. Both children proved their own work. The orchestrator's window is still small enough to hold the whole plan.
