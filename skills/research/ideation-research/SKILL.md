---
name: ideation-research
description: "Use to research and vet an idea before building it."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
 hermes:
 tags: [ideation, idea-vetting, competitor-research, product-strategy]
 related_skills: [persona-research-specialist, research-lens-market, research-lens-horizon, persona-startup-builder, deep-research]
---

# Ideation Research: Vet the Idea Before the Build

## When to Use

Run this on any of David's ideas before it reaches a Builder. It is the route between raw idea and buildable plan. For any SaaS feature or new market, competitor research is MANDATORY here, not optional.

## The route

1. **Researcher pass (mandatory for SaaS).** Load `research-lens-market` and `deep-research`. Produce the two sets: Set A the top 10 the CUSTOMER would compare, Set B the top 10 the PLATFORM is judged against (AlphaFlux, AlphaVision, AlphaSafe, iTaK, Patriot Pest Control, exact casing). Each with date-stamped pricing, capability notes, and a named parity target. For emerging-tech ideas, also run `research-lens-horizon` and label maturity: HYPE, EMERGING, or SHIPPING.

2. **Ideator pass (against what David already has).** With the researched landscape in hand, check the idea against David's existing stack and products. Answer:
 - Is this novel or a clone. He wants novel, with the feature gap named.
 - What is the BETTER route. Same job, less build, stronger differentiator.
 - What is missing that competitors have. Name the gap explicitly.
 - What to CUT. What in the idea does not earn its build cost.
 - Where it fits his stack: Go backend, Flutter clients, SurrealDB, Dokploy, local GPU inference. A route that fights those defaults needs a reason.

3. **The deliverable.** A vetted brief: the researched competitor sets, the parity targets, the ideator's better-route recommendation, the cut list, and a go / reshape / kill verdict with reasons. This brief is what the Builder receives, never the raw idea.

## Rules

- No SaaS feature reaches a Builder without the competitor sets in hand. An idea built without them is a clone by default.
- Novelty is checked against the researched set, not asserted.
- Every recommendation traces to a competitor finding or a gap, not a hunch.
- The ideator does not build. It names the route; the Builder walks it.

## Failure modes

- Building the idea as stated because it sounded good, without checking the field.
- Cloning an existing competitor and calling it a product.
- Ignoring David's stack defaults and recommending a foreign architecture.
- A parity target with no observable pass condition.
