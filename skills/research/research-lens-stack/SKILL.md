---
name: research-lens-stack
description: "Use when researching tech, libraries, or prior art."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
  hermes:
    tags: [research, tech-stack, libraries, prior-art, tool-selection]
    related_skills: [persona-research-specialist, deep-research, github-research]
---

# Research Lens: Tech Stack and Prior Art

## When to Use

Load alongside `persona-research-specialist` when the commission is a technology decision: which library, framework, database, service, or approach to use, or whether to build vs buy. Fires on "should we use X or Y", "is there prior art for this", "what's the best tool for Z".

## The intelligence requirement

Before searching, name: the decision this feeds, the candidate set (at least 3 where they exist), and the evaluation criteria that matter for David's context: performance, license terms, maintenance health, community size, Windows support, and a real machine-access path (not just a cloud API).

## Where to look

- **Prior art first: `github-research` skill.** For software behavior questions, run its gh CLI method: `gh search prs --merged` (highest signal), then maintainer comments, then closed issues with solutions, then open issues. Stars measure interest, not fitness.
- **Current docs, not training memory.** Read the vendor's live docs for version-specific behavior. Training data drifts.
- **Release logs and commit recency.** Is the project actively maintained. When was the last real push.
- **Benchmarks, then interrogate the methodology.** Who ran it, on what hardware, against what baseline.

## Output shape

- **Comparison matrix.** One row per candidate, columns for the criteria named in the intelligence requirement. Every cell cited or marked unknown.
- **Recommendation with tradeoffs.** The pick, why, what it costs you, and the exit path if it fails.
- **License and maintenance audit.** Read the real LICENSE file (the metadata `license` field is often null or `other` and can hide BUSL-style terms). Check for an `ee/` directory that signals a split license.
- **Prior-art summary.** What already exists, what it got right, what to avoid repeating.

## Gotchas this lens exists to catch

- Stars mistaken for fitness. A 40k-star repo can be abandoned; check push date.
- License metadata trusted over the actual LICENSE file.
- Benchmark methodology rigged or unstated.
- Docs describing shipped behavior that the released version does not have.
- Cloud-only tool recommended to David, who prefers local and self-hosted where it is viable.

## Mapping to David's stack

Default he reaches for: Go standard library first, Flutter for clients, SurrealDB for platform data, Docker and Dokploy to ship, local GPU inference over fragile SaaS. A recommendation that fights those defaults needs a stronger reason than novelty.
