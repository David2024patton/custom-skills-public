---
name: ai-seo-aeo
description: "Use to get cited by AI search and answer engines."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
  hermes:
    tags: [aeo, geo, ai-search, answer-engine, llm-citation, llms-txt, eof]
    related_skills: [seo-reference, persona-content-marketing, persona-research-specialist, deep-research]
---

# AI SEO: Answer Engine Optimization (AEO) and Generative Engine Optimization (GEO)

## When to Use

When you want a page or product to be CITED by AI surfaces: Google AI Overviews, ChatGPT, Perplexity, Bing Copilot, Claude. This is the emerging discipline (the "new AI SEO"). It sits on top of classic `seo-reference`; AI engines cite the same trustworthy, well-structured, answer-first pages, plus a few things specific to how LLMs retrieve and attribute.

## How AI engines pick citations (the mental model)

AI answers are grounded in retrieved web content. To be cited you must be (1) retrievable, (2) a clean match for the question, and (3) a trustworthy, attributable source. Engines favor content that states a direct answer, carries structure they can parse, and comes from a recognizable entity.

## The AEO/GEO checklist

### Be retrievable
- [ ] Indexable, fast, and crawlable (same as classic SEO). If Google cannot index it, the assistant cannot cite it.
- [ ] Serve a crawlable text version. Heavy JS-only content is often missed; prerender or SSR.
- [ ] Ship an llms.txt at the site root: a concise, curated markdown map of your key pages and what each answers, so crawlers used by AI tools can parse intent without wading through HTML.
- [ ] Keep robots.txt from blocking AI crawler agents you WANT citing you (GPTBot, PerplexityBot, ClaudeBot, Google-Extended), decide that deliberately per site.

### Be a clean match for the question
- [ ] Answer-first: put a direct, quotable answer to the likely question in the first sentence or two of the section.
- [ ] Question-shaped headings (H2/H3 as the actual question) so the engine maps query to section.
- [ ] Concise, self-contained paragraphs an engine can lift without losing meaning.
- [ ] FAQ and HowTo structure with schema (feeds both classic and AI search).
- [ ] Named entities: your product, its category, its differentiators stated plainly, so the engine can attribute claims to you.

### Be trustworthy and attributable
- [ ] Clear authorship and an About/entity presence so the engine can resolve WHO is behind the claim.
- [ ] Original data, first-hand tests, and specific numbers (with sources) beat generic prose for citations.
- [ ] Consistent NAP/entity across your site and profiles so the engine's knowledge graph resolves you.
- [ ] Freshness: updated pages with visible dates get retrieved more for time-sensitive queries.

## Measuring it

- Periodically ask the engines your target questions ("best multi-tenant SaaS console for X") in Google AI Overviews, ChatGPT, Perplexity, and see whether you are cited and how you are characterized.
- Track branded + category queries where you want citation, not just classic rank.
- There is no official AI-citation console yet, so this is manual spot-checking plus your classic search analytics.

## The four layers of visibility (and the third-party gap most brands miss)

Modern AI-search visibility has four layers. The one most brands skip is the biggest:

1. **Technical discoverability** - the site can be crawled, understood, retrieved. (classic SEO)
2. **Entity clarity** - the brand, products, claims, prices, policies stated consistently everywhere.
3. **Independent corroboration** - THIRD parties (publishers, reviewers, communities, forums, retailers, affiliates) discuss the brand accurately. This is the layer brands neglect, and it dominates.
4. **Answer-level visibility** - the brand actually appears in the AI answers for important questions, accurately described.

The critical number (McKinsey 2025 AI Discovery Survey): a brand's OWN sites make up only 5% to 10% of the sources AI search cites. The other 90%+ is third-party. So AEO is NOT only about optimizing your own pages. It is mostly about the ecosystem that talks about you: getting reviewed, discussed, compared, and accurately described in the places AI actually reads from.

Context that makes this urgent (McKinsey, same survey): half of consumers now intentionally use AI search, 44% call it their primary source (ahead of traditional search at 31%), and $750B of US consumer spending could flow through AI search by 2028. Only 16% of brands systematically track AI-search performance, which is a real early-mover window.

### What to actually do for the third-party layer
- Monitor how AI engines describe you AND your competitors across engines, regions, and phrasings.
- Map which third-party sources get cited for your key questions, then cultivate those: reviews, roundups, comparison sites, community threads, affiliate and publisher coverage.
- Publish original evidence (data, specs, comparisons, expert guidance) that third parties can cite when they talk about you.
- Correct inaccurate info AT THE SOURCE (the review site, the listing, the forum), not only on your own page.
- Track citation share, sentiment, and recommendation position over time, not just rank.

## Examples

### llms.txt (site root, markdown)
```markdown
# AlphaFlux
> Multi-tenant SaaS console for whitelabel platform management.

## Key pages
- [What is AlphaFlux](/what-is): One-paragraph answer to "what is AlphaFlux".
- [Pricing](/pricing): Tier names, prices, what each includes.
- [Multi-tenant security](/security/tenancy): How tenant isolation is enforced.
```

### Answer-first section (question heading + quotable answer)
```html
<h2>How much does AlphaFlux cost?</h2>
<p>AlphaFlux starts at $29/month for the base tier and scales by tenant count; the whitelabel tier adds custom branding.</p>
<p>Full breakdown by tier, with what each includes, follows.</p>
```

### robots.txt decision (allow the AI crawlers you want)
```text
User-agent: GPTBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /
```


## Paid placement in AI search (the ads layer, distinct from organic AEO)

AEO/GEO above is the ORGANIC path to being cited. There is now a PAID path too: AI platforms are selling placement inside or alongside AI answers, the same way Google sells ads next to search results. Know both, and keep them separate in your head.

State of play (verify current before spending; this moves monthly):
- **ChatGPT / OpenAI: ads are live.** OpenAI has moved from testing to launched ad formats in ChatGPT, including visual ads shown alongside answers, with its own format and measurement. If you want paid reach in ChatGPT, this is the door.
- **Google: ads in and beside AI Overviews.** Google runs ads tied to AI Overviews / AI Mode; there is an official "ads and AI Overviews" product surface and a new ad generation for the AI era of Search.
- **Perplexity: pulled back.** It experimented with sponsored placements then stopped over trust concerns. Do not assume you can buy Perplexity placement today; re-check.
- **Emerging LLM ad marketplaces:** a new category of "LLM advertising" and "smart LLM ads" is appearing, plus tools that TRACK whether you got a sponsored placement or citation in AI answers (AI paid-ads tracking, LLM citation tracking, LLM visibility monitors).

How to think about it:
- Paid placement buys visibility; organic AEO buys citation credibility. The best position is BOTH: pay to appear where it converts, and earn the organic citations that make the paid spend stick.
- Paid AI placement is still young and prices/formats are not standardized. Treat it like early ad platforms: small test budget, measure, do not scale on faith.
- Because there is no standard reporting yet, use the emerging AI paid-ads / citation tracking tools to verify your placements and citations actually happen.

Decision rule for David: for any SaaS feature push, run organic AEO/GEO first (it compounds and is free), then test a small paid AI placement budget on the one platform where his buyers actually ask questions, and measure with a citation/ads tracker. Re-verify platform ad availability each time, because Perplexity's pullback shows this is not stable.

## Links (current 2026 sources)
- GEO/AEO enterprise guide (Writer): https://writer.com/blog/geo-aeo-optimization/
- How to get cited by AI (Omnius): https://www.omnius.so/blog/how-to-get-cited-by-ai
- LLM optimization, cited in AI answers (SEOptimer): https://www.seoptimer.com/blog/llm-optimization/
- Rank in Google AI Overviews (seo.com): https://www.seo.com/blog/ai-overview-ranking-factors/
- GEO practical guide (Equinet Academy): https://www.equinetacademy.com/blog/generative-engine-optimisation-geo
- AEO guide 2026 (PartnerStack): https://partnerstack.com/resources/guides/answer-engine-optimization-t

- OpenAI ads in ChatGPT (format and measurement): https://openai.com/index/new-chatgpt-ads-format-and-measurement/
- OpenAI testing ads in ChatGPT: https://openai.com/index/testing-ads-in-chatgpt/
- OpenAI visual ads launch (TechCrunch): https://techcrunch.com/2026/10/05/openai-launches-visual-ads-that-appear
- Google: ads and AI Overviews (Ads Help): https://support.google.com/google-ads/answer/16297775
- Google: a new generation of ads for the AI era of Search: https://blog.google/products/ads-commerce/google-marketing-live-search-a
- Perplexity advertising experiment, then pullback: https://www.perplexity.ai/hub/blog/why-we-re-experimenting-with-advertis and https://searchengineland.com/perplexity-stops-testing-advertising-469452
- AI paid-ads / LLM citation tracking tools: https://llmpulse.ai/features/ai-paid-ads-tracking and https://www.adthena.com/llm-visibility/
- McKinsey: New front door to the internet, winning in the age of AI search: https://www.mckinsey.com/capabilities/growth-marketing-and-sales/our-insights/new-front-door-to-the-internet-winning-in-the-age-of-ai-search
- LLM advertising agency category: https://foundationinc.co/services/llm-advertising/

## Rules

- AEO rides on real SEO and real value. There is no citation hack that beats being the best answer to the question.
- Never fabricate stats to look quotable. Engines and readers both punish it.
- This field moves fast: re-verify the checklist against fresh sources before a major push, and cite what you verify.
