---
name: research-lens-horizon
description: "Use when researching trends or what's next for a domain."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
 hermes:
 tags: [research, trends, emerging-tech, ideation, horizon-scanning]
 related_skills: [persona-research-specialist, deep-research, arxiv, competitor-news-monitor]
---

# Research Lens: Horizon, Trends, and What's Next

## When to Use

Load alongside `persona-research-specialist` when the commission is forward-looking: what is emerging in a field, what is worth building next, where a technology is heading. Fires on "what's next", "what should we build", "what's the trend here", or when feeding IDEA.md.

This is David's ideation fuel. He generates product ideas from research papers, forums, competitor comparisons, and what's-next trends. He wants novel researched ideas over clones, with feature gaps called out against top competitors.

## The intelligence requirement

Name: the domain, the time horizon (this quarter, this year, multi-year), and the decision or ideation this feeds. A trend with no downstream decision is trivia.

## Where to look

- **Papers: `arxiv` skill.** For emerging technique signals. A paper is a hypothesis, not a product; label maturity honestly.
- **Hacker News, forums, community signal.** What practitioners are actually building and complaining about, not what vendors announce.
- **Vendor roadmap and release blogs.** Direction of travel. Distinguish shipped from announced.
- **Standards bodies and conference talks.** Where the floor is moving.
- **`competitor-news-monitor`** for material news on named companies in the field.

## Output shape

- **Trend list with evidence.** Each trend: what it is, the signal that surfaced it, a source URL, and a maturity label: HYPE (lots of talk, little shipping), EMERGING (early real use), or SHIPPING (production adoption).
- **What it means for David's products.** Per product, the opportunity or the threat, one line each. If a trend touches nothing he owns, say so.
- **Novel vs clone assessment.** For any buildable idea: is this a differentiated angle with a real feature gap, or a clone of an existing product. He wants the former.
- **Open questions.** What is unresolved and would need a deeper `deep-research` commission to answer.

## Gotchas this lens exists to catch

- Hype cycle mistaken for adoption. HYPE labeled as SHIPPING.
- Vendor announcement treated as shipped capability.
- Paper result treated as production-ready.
- A trend with no connection to anything David owns, presented as actionable.
- Recency bias: the newest thing treated as the most important without evidence.

## Mapping to David's products

Where horizon scanning actually pays off for him: local GPU inference and the llama.cpp / vLLM / Vulkan stack, multi-tenant AI SaaS patterns, Flutter on TV and web, autonomous coding harnesses (the harness), and the agentic AI threat landscape that feeds the security persona.
