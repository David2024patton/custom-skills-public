---
name: research-lens-market
description: "Use when researching a market, competitors, or pricing."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
 hermes:
 tags: [research, competitors, market, pricing, positioning]
 related_skills: [persona-research-specialist, deep-research, competitor-crawl-pipeline, crawl4ai-competitor-intel]
---

# Research Lens: Market, Competitors, and Pricing

## When to Use

Load alongside `persona-research-specialist` when the commission is a market question: who the competitors are, what they charge, where the gaps are, whether a feature field or market is worth entering. Fires on "who are we up against", "what should we charge", "is this market worth it".

This lens is the COMMISSION BRIEF and the review gate. The execution mechanics live in `deep-research` and the crawl layer. Do not duplicate them here; hand the brief to those skills and gate the output.

## The intelligence requirement

Name before searching: the product, the feature field or market, the buyer, and the budget band. One Set A and Set B pair per field or market.

## What this commission demands

- **Set A: the top 10 the CUSTOMER would compare.** Same buyer, same job, same budget band, same market track. What a real shortlist weighs.
- **Set B: the top 10 competitors to the PLATFORM.** AlphaFlux, AlphaVision, AlphaSafe, iTaK, or the harness named in the header with exact casing. The capability surface the platform is shortlisted against.
- **Pricing with provenance.** Every row: price, currency, billing period, plan name, source URL, observed date, method tag. Anything older than 30 days re-fetched before ship.
- **A named parity target.** `Match <competitor>'s <capability> (test: <observable pass condition>)`. "Reach parity" is not a target.

## Where to look

- Hand execution to `deep-research`: SearXNG at https://search.itak.live/ first, 2+ runs per query per the jitter rule, badge tallies, method tags.
- `competitor-crawl-pipeline` and `crawl4ai-competitor-intel` for page-level evidence, pricing extraction, and the validator gate.
- Locale pass for non-US markets via the `language=xx-XX` parameter. State and city claims are query-derived, never engine-reported.

## Output shape

The `deep-research` deliverable order, gated by this lens: Findings, Set A table, Set B table, Pricing (date-stamped), Gaps, Parity targets, Recommendations, Appendix query log. Every number carries a method tag and URL.

## Gotchas this lens exists to catch

- Set A and Set B merged into one list. They answer different questions.
- Listicles and best-of roundups treated as evidence instead of leads to crawl.
- US price quoted as a global price. Locale never recorded.
- A parity target with no observable pass condition.
- Padding to 10 rows when only 6 credible candidates exist. Declare the shortfall instead.

## Mapping to David's products

- AlphaFlux: whitelabel SaaS console, priced against the multi-tenant admin tool market.
- AlphaVision: TV OS, compared against Android TV and Fire OS class platforms.
- iTaK Learn: Postgres learning platform, compared against the LMS field.
- Patriot Pest Control: field-service tooling, where the customer shortlist is the real comparison set.
