# AlphaFlux Research

---
name: alphaflux-research
description: "Use for research that feeds an AlphaFlux decision: a new vertical or market, a feature area, pricing, or a competitor question."
---

## Relationship to the engine (precedence rule)

The canonical research engine is **`skills/deep-research`**: its SKILL carries the
effort tiers, the ledger tooling (`scripts/research_ledger.py`, same file, copied
here so this skill is self-contained), the source rubric, the query playbook, the
report template, the skeptic pass, and the research-repo filing law. This skill is
an OVERLAY: it adds the AlphaFlux layer and nothing else. For any research that is
not about AlphaFlux, load `skills/deep-research` instead and skip this file.

- Run the engine's full procedure (sections 4 to 11 of its SKILL) on every run from
  this overlay, then add the AlphaFlux layer below to the contract, the synthesis,
  and the report.

## The AlphaFlux layer (run on every run)

- TOP 10, TWO LISTS (David's standing rule, 2026-10-20). For any vertical, market,
  or feature area, research the top 10 competitors online in BOTH directions:
  1. Competitors to the CUSTOMER: the tools the businesses in that vertical already
     shop between.
  2. Competitors to ALPHAFLUX: the all-in-one platforms fighting for the same
     owner's wallet.
  Both lists ship with dated pricing (labeled vendor claim where the number comes
  from the seller) and capability notes. A run that names fewer than ten per side
  says why in Gaps, never pads.
- COMPARE AGAINST THE REAL PRODUCT. Map every researched capability against
  AlphaFlux's actual modules, verified in the alphaflux-console code or the current
  build plans, never from memory. Every mapped module gets HAVE / PARTIAL / GAP.
- SCENARIO MATRIX. Each AlphaFlux section (scheduling, billing, team, CRM, forms,
  payments, marketing) must bend to different business scenarios; the matrix makes
  sections universal across business types.
- PARITY VERDICTS. Every feature the report recommends names which researched
  competitor it matches or beats, with an observable pass test. No unnamed
  "industry standard" claims.
- BUILD IMPLICATIONS LAST. End the report with what AlphaFlux should build, change,
  or skip, ranked by value, each item tied to the module seam it touches.

## Privacy and consent (this fork handles business and competitor data)

- Save durable findings into notes or memory only after delivery, and only with the
  user's consent when the findings concern identifiable people, customers, or
  employees; business and market facts need no consent.
- Never put personal data, credentials, or customer records into a shared report or
  a repo file. Reports filed to the research repo carry company and market facts only.

## Portability (this skill never hardcodes another runtime)

- Every path here is relative to this skill's own directory; run
  `python3 <skill-dir>/scripts/research_ledger.py init --question "..."` from where
  the skill is installed. No `~/workspace/...`, no `/opt/muse/...`.
- Tool names in prose are examples from the original runtime: substitute the tools
  you actually have (web_search / web_extract / browser_exec for source reads,
  delegate_task for fan-out, the memory tool for notes). If a named tool is absent,
  mark the step UNAVAILABLE and continue: a coverage note, never a blocker.

## Panels and audience

Every flagship AlphaFlux run uses the engine's perspective panels with the
corporate context perspective ON: the buyer-and-compliance perspective covers
the economic buyer's challenge (pricing, parity, switching cost) and the control
or regulation touching the feature (SOC 2, GDPR, CCPA per the compliance lens).

## Stop rules

The engine's stop rules govern: every high-impact claim supported, or the picture
stops changing, or the named gaps cannot close. Budget spent alone is never a stop.
