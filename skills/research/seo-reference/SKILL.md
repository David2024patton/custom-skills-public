---
name: seo-reference
description: "Use when optimizing a site for search engines."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
  hermes:
    tags: [seo, search, technical-seo, on-page, ranking, content]
    related_skills: [ai-seo-aeo, persona-content-marketing, persona-content-creator, deep-research]
---

# SEO Reference: Technical and On-Page

## When to Use

When building or auditing any site for search visibility: AlphaFlux marketing pages, iTaK Learn, Patriot Pest Control, product landing pages. Pair with `ai-seo-aeo` for the AI-search layer, which is now coupled to classic SEO.

## The checklist (nothing skipped)

### Technical
- [ ] Crawlable and indexable: robots.txt allows the important paths; XML sitemap submitted; no accidental noindex on pages you want ranked.
- [ ] Core Web Vitals pass: LCP (loading), INP (interactivity), CLS (layout shift). Measure in real field data, not just Lighthouse.
- [ ] Mobile-first: fully responsive, no horizontal scroll, tap targets sized.
- [ ] HTTPS everywhere, no mixed content, no redirect chains.
- [ ] One canonical URL per page (rel=canonical, no duplicate/param variants competing).
- [ ] Structured data (schema.org JSON-LD) for the page type: Product, FAQ, HowTo, Article, LocalBusiness, Organization. Validate with Google's Rich Results Test.
- [ ] Clean semantic HTML: one H1, logical heading order, descriptive title tag and meta description.
- [ ] Internal links: every important page reachable within a few clicks; descriptive anchor text.

### On-page
- [ ] One primary keyword per page, in title, H1, first 100 words, and URL.
- [ ] Search intent match: informational, navigational, transactional, commercial. Give the searcher the format they expect.
- [ ] Answer the query up top (the 3-second rule), then go deep. scanners bounce, so lead with the answer.
- [ ] Original value: data, screenshots, first-hand experience. Thin aggregation does not rank.
- [ ] Freshness where it matters: dated content updated with a visible date.
- [ ] The 90-year-old readability rule applies: short sentences, plain words, scannable structure.

## The AI-search coupling

Classic SEO now feeds AI search. Pages that get cited by AI Overviews and assistants are the same pages that rank: clear answers, structured data, strong entities, trustworthy authorship. So do this checklist AND `ai-seo-aeo`.

## Examples

### JSON-LD FAQ block (paste into the page head)
```html
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage",
 "mainEntity":[{"@type":"Question","name":"What is AlphaFlux?",
 "acceptedAnswer":{"@type":"Answer","text":"AlphaFlux is a multi-tenant SaaS console for managing whitelabel platforms."}}]}
</script>
```

### Meta template
```html
<title>Primary Keyword - Brand</title>
<meta name="description" content="Answer the query in under 155 chars, with the brand and a reason to click.">
<link rel="canonical" href="https://example.com/canonical-url">
```

## Links (primary sources)
- Google Search Central (technical start): https://developers.google.com/search/docs/fundamentals/get-started
- Google Search Central (structured data): https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- Core Web Vitals: https://developers.google.com/search/docs/appearance/core-web-vitals
- Semrush SEO best practices (incl. AI search): https://www.semrush.com/blog/seo-best-practices/
- Google ranking factors overview: https://www.seo.com/basics/how-search-engines-work/ranking-factors/

## Rules

- No keyword stuffing, no cloaking, no bought links. It risks the domain, not just the page.
- Every recommendation ties to a measurable signal, not a hunch.
- For competitor SERP and keyword research, hand off to `deep-research` and `research-lens-market`.
