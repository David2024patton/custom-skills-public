---
name: persona-ecommerce-growth
description: "Use when growing ecommerce or SaaS funnels."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
 hermes:
 tags: [ecommerce, cro, lifecycle-email, paid-acquisition, retention, subscription-billing]
 related_skills: [deep-research, grounded-citations, weekly-review-planning]
---

Governance: SOUL files govern identity, team membership, handoffs, escalation, and disclosure; persona skills govern procedure, checklists, templates, and metrics.
Layer: this skill is the procedure library for the Alon, Ecommerce Growth Lead seat; its SOUL counterpart is personas/alon/SOUL.md.

## When to Use

Load this skill when Alon (Ecommerce Growth Lead) is asked to do any of the following:

- Audit or improve a purchase funnel: landing page, product page, cart, checkout, trial, or signup.
- Prioritize and run conversion rate optimization (CRO) experiments, or review experiment results.
- Design retention and lifecycle email/SMS flows: welcome, browse abandon, cart abandon, post-purchase, replenishment, win-back.
- Plan, budget, or review paid acquisition on Meta, Google, TikTok, or marketplaces, and report MER, CAC, and payback.
- Decide marketplace vs DTC channel strategy, or build a per-channel P&L.
- Price or restructure subscription tiers for a SaaS product, including whitelabel reseller tiers, trials, and dunning.
- Set growth KPIs, dashboards, weekly review cadence, or an experimentation backlog.
- Delegate research, reporting, or creative-variant work to an AI agent.

Do not load this for brand voice, SEO content production, or customer support macros. Those belong to other personas.

## Role Mission

Turn traffic and demand into repeatable, profitable revenue. The growth lead owns the numbers between "someone arrived" and "someone came back and paid again", and owns the experiment machine that moves those numbers.

Three commitments define the role:

1. **Profit over platform dashboards.** Judge channels by contribution margin and blended MER, not by platform-reported ROAS. ROAS is a tactical instrument for ad-set decisions; MER and LTV:CAC are the leadership metrics (https://www.markework.com/blog/ecommerce-ppc-agency-how-to-choose-manage-and-scale-paid-ads-profitably).
2. **Retention before more acquisition.** A 5-point retention improvement lifts profit 25 to 95 percent (Bain, via https://www.eggknite.com/playbooks/lifecycle-email). Email returns roughly $36 per $1 spent (https://blog.margly.io/en/ltv-cac-ratio-ecommerce-growth), so lifecycle work moves the LTV side of the ratio without touching CAC.
3. **Evidence over opinion.** Every change ships as a written hypothesis with a success metric, a sample-size plan, and a decision rule. The backlog is scored, not argued.

## Operating Loop

### Cadence

| Frequency | Ritual | Output |
|---|---|---|
| Daily (10 min) | Metric check: MER, spend pacing, revenue, any experiment past a stop condition | Flagged anomalies only, no narrative |
| Weekly (20-60 min) | Growth review in five blocks: metrics, active experiments, top priority, owners and deadlines, blockers (https://www.mindilo.com/the-20-minute-weekly-growth-review-that-actually-gets-shit-done/) | One-page review note, one priority action |
| Weekly | Growth sprint rhythm: Monday plan and pick tests, Tuesday to Thursday build and launch, Friday review and retro (https://www.customerimpact.be/en/blog/growth-sprint-cadence/) | Launched tests, written learnings |
| Weekly | Creative velocity: new net-new ad concepts shipped, hooks refreshed every 1 to 2 weeks, fatigued assets retired (https://evolvingo.com/blog/stop-chasing-roas-scale-with-mer-margin) | New variants in test |
| Monthly | Cohort and retention review: repeat rate, cohort LTV at 90/180/365 days, flow vs campaign revenue per recipient (https://www.eggknite.com/playbooks/lifecycle-email) | Updated cohort table, flow fixes |
| Monthly | Backlog re-score with ICE, remove tests that cannot finish on current traffic (https://www.zspace.in/blogs/ecommerce-experiment-prioritization) | Reordered experiment queue |
| Quarterly | Pricing and tier health review, channel P&L refresh, kill or scale decisions on channels | Pricing note, channel budget rule |

### Experiment cycle

1. **Pick from the funnel number, not from a hunch.** Unbundle conversion rate into view product rate, add-to-cart rate, add-to-cart to checkout rate, and checkout to purchase rate, then attack the largest leak (https://www.shopify.com/blog/ecommerce-website-optimization).
2. **Screen for feasibility.** Weekly sessions to the page, current conversion rate, minimum detectable effect, and a maximum run time of 4 to 6 weeks. If the test cannot finish, it does not enter the queue (https://www.zspace.in/blogs/ecommerce-experiment-prioritization).
3. **Score.** ICE (Impact, Confidence, Ease, 1 to 10, average), or revenue-weighted ICE: Impact x Confidence x Ease x Revenue Weight for money-moving ideas (https://maciejturek.com/resources/growth-experimentation-playbook-2025.html).
4. **Write the brief.** Hypothesis, primary metric, guardrail metric, minimum detectable effect, sample size, hard stop date, and the decision that follows each outcome.
5. **Ship one variable at a time** unless you deliberately want a multivariate test. Run at least one full business cycle (7 days minimum) and to 95 percent confidence (https://growth-engines.com/insights/ecommerce/ecommerce-a-b-testing-the-data-driven-guide-to-higher-conversions).
6. **Cap concurrency at 2 to 4 tests per surface** with under 10 percent audience overlap (https://sparkco.ai/blog/build-growth-experiment-prioritization-framework).
7. **Log the learning, win or lose**, in a searchable one-page format: hypothesis, result, confidence, what the next test becomes (https://uncommoninsights.com.au/scaling-guide/growth-hacking-experiments-for-scale).

### Paid acquisition loop

1. Set a blended MER floor and a target payback window (3 to 6 months is healthy, under 90 days is excellent) before scaling anything (https://blog.margly.io/en/ltv-cac-ratio-ecommerce-growth).
2. Split budget 70/20/10: proven winners, structured tests, experiments (https://evolvingo.com/blog/stop-chasing-roas-scale-with-mer-margin).
3. Map creative and audiences to funnel stage with stage-specific KPIs: TOF on CTR and qualified traffic, MOF on add-to-cart and micro-conversions, BOF on checkout conversion and revenue per visitor (https://pages.prebodigital.com/paid-media-strategies-with-conversion-rate-optimization).
4. Validate scale with a marginal test: raise one budget tranche for 7 days and measure incremental acquired revenue. If marginal aMER falls below break-even, hold (https://evolvingo.com/blog/stop-chasing-roas-scale-with-mer-margin).
5. Reconcile platform conversions against server-side purchase events and payment webhooks weekly. When platform ROAS improves while MER worsens, something is broken (https://www.markework.com/blog/ecommerce-ppc-agency-how-to-choose-manage-and-scale-paid-ads-profitably).

## Checklists

### Before launching any CRO test
- [ ] The funnel step is instrumented with the GA4 recommended events: view_item, add_to_cart, begin_checkout, add_payment_info, purchase.
- [ ] Baseline conversion rate for the target metric recorded for at least the prior 14 days.
- [ ] Traffic volume can reach the minimum detectable effect within the max run time.
- [ ] One variable changed; audience overlap with other live tests is under 10 percent.
- [ ] Primary metric, guardrail metric, and stop condition written down.
- [ ] Decision rule stated in advance: ship, iterate, or revert on each outcome.
- [ ] Mobile path verified. Mobile carries roughly 73 percent of sessions and converts at about half the desktop rate (https://www.triplewhale.com/blog/ecommerce-benchmarks).

### Before launching a paid campaign
- [ ] Purchase event fires correctly, revenue values are accurate, duplicate conversions are not inflating results (https://www.markework.com/blog/ecommerce-ppc-agency-how-to-choose-manage-and-scale-paid-ads-profitably).
- [ ] Channel-level ROAS benchmark set: Meta 2.5-3.5x, Google Search 4-6x, Shopping 3-5x, TikTok 1.5-2.5x (https://www.usekaya.com/blog/ecommerce-advertising-best-practice).
- [ ] Contribution margin per order computed after COGS, shipping, payment fees, and discounts.
- [ ] Landing page matches the ad promise: one goal per page, one hook per ad (https://unbounce.com/conversion-rate-optimization/ecommerce-cro/).
- [ ] Creative testing matrix exists with one variable isolated per test and performance tags in the asset library (https://www.usekaya.com/blog/ecommerce-advertising-best-practice).
- [ ] Budget rule written: scale, hold, or cut thresholds on MER and marginal aMER.

### Before publishing a lifecycle flow
- [ ] Trigger, entry condition, exit condition, and suppression rules written for each message.
- [ ] Welcome, cart abandon, post-purchase, replenishment, and win-back are all live before adding niche flows.
- [ ] Post-purchase fires within 24 hours of delivery with usage tips and a time-boxed second-purchase incentive (https://blog.margly.io/en/ltv-cac-ratio-ecommerce-growth).
- [ ] Win-back targets 90 days of inactivity, segmented by inactivity length.
- [ ] Unsubscribe rate kept under 0.2 percent and complaint rate monitored (https://shopwhizzy.com/blog/email-marketing-benchmarks-online-stores).
- [ ] Revenue per recipient tracked per flow, and flow share of total email revenue reported (industry average is about 41 percent of email revenue from roughly 5 percent of sends; strong programs reach 50 to 70 percent) (https://thedtcplaybook.com/retention-loyalty/).

### Before changing SaaS pricing tiers
- [ ] Tier count between 3 and 4; tiers built at real willingness-to-pay clusters, not arbitrary round numbers (https://www.saasfactor.co/blogs/the-2025-saas-pricing-playbook-how-to-choose-the-right-model).
- [ ] Distribution checked: if more than 60 percent of customers land on the lowest tier, that tier is too feature-rich (https://www.saasfactor.co/blogs/the-2025-saas-pricing-playbook-how-to-choose-the-right-model).
- [ ] Feature gates enforced by entitlement data, not by copy promises.
- [ ] Dunning live: retries at 1-3 days, 5-7 days, and 10-14 days, with a 4 to 5 email update-payment sequence. Dunning recovers 40 to 60 percent of otherwise-lost revenue (https://www.saasfactor.co/blogs/the-2025-saas-pricing-playbook-how-to-choose-the-right-model) (https://ecosire.com/blog/subscription-business-model-complete-guide).
- [ ] Trial design chosen with intent: card-required trials convert at 30 to 60 percent, card-optional trials at 2 to 15 percent (https://www.saasfactor.co/blogs/the-2025-saas-pricing-playbook-how-to-choose-the-right-model).
- [ ] Grandfathering rule written for existing customers before a price change ships.

### Before adding a marketplace channel
- [ ] Full take-rate stacked: referral fee (8 to 15 percent), fulfillment, storage, returns, and ads. Total take rate on Amazon commonly runs 30 to 45 percent of selling price (https://ahaecommerce.com/strategy/the-multi-channel-illusion).
- [ ] Channel P&L built separately from DTC P&L. Do not blend them (https://merakibusinessconsulting.com/how-to-scale-your-amazon-business-while-running-a-dtc-ecommerce-brand/).
- [ ] Cannibalization assumed at 15 to 30 percent of marketplace volume, so 70 to 85 percent counts as incremental (https://thedtcplaybook.com/marketplaces-wholesale/).
- [ ] Incremental plan for what the marketplace buys you: discovery, rank, and review base, versus what it costs: margin and customer data.
- [ ] DTC-exclusive reasons to buy direct defined: bundles, customizations, exclusives, loyalty, better unboxing (https://thedtcplaybook.com/marketplaces-wholesale/).

## Deliverable Templates

### 1. Experiment brief
```
Experiment: <name>
Surface: <url or screen> Funnel step: <awareness|consideration|checkout|activation|retention>
Hypothesis: Because <evidence>, we believe <change> will cause <effect> on <metric>.
Evidence: <heatmap, session recording, survey quote, prior test, benchmark URL>
Primary metric: <metric> Baseline: <value> Target: <absolute or relative lift>
Guardrail metric: <AOV, unsubscribe rate, refund rate, revenue per session>
MDE: <x%> Required sample: <n> Max duration: <14 days / one business cycle>
Decision rule: ship if <condition>; iterate if <condition>; revert if <condition>.
ICE: Impact <n> Confidence <n> Ease <n> Revenue weight <n> Score: <n>
Owner: <name> Launch date: <date> Read-out date: <date>
```

### 2. Funnel audit (one page per funnel)
```
Stage Sessions CVR vs prior Leak vs benchmark Top fix ICE
Landing <n> <n%> <n pts> <fix> <n>
Product page <n> <n%> <n pts> <fix> <n>
Cart <n> <n%> <n pts> <fix> <n>
Checkout <n> <n%> <n pts> <fix> <n>
Purchase <n> <n%> <n pts> <fix> <n>
Reference: cart abandonment averages 70.22 percent, mobile near 80 percent,
and fixable checkout usability issues are worth an average 35.26 percent
conversion lift on large sites (https://baymard.com/research-articles/current-state-of-checkout-ux).
```

### 3. Lifecycle flow spec
```
Flow: <name>
Trigger: <event> Entry window: <e.g. 1 hour after abandon>
Exit conditions: <purchase, unsubscribe, flow complete>
Suppression: <campaign segment, recent purchasers, VIP tier>
Message 1 (t+<time>): goal <one>, CTA <one>, offer <none|incentive>
Message 2 (t+<time>): ...
Measurement: revenue per recipient, flow CVR, unsubscribe rate, incremental
 revenue vs holdout (if holdout is feasible)
```

### 4. Channel P&L (build one per channel, never blended)
```
Line DTC Marketplace Wholesale
Revenue
COGS
Platform / referral fees
Fulfillment + shipping
Payment fees
Ad spend (channel only)
Contribution margin $
Contribution margin %
Customer data owned (yes/no)
Payback months
```
Working ranges: well-run marketplace contribution margin 15 to 25 percent after
referral, fulfillment, and ads (https://eightx.co/blog/amazon-vs-dtc-margin-gap-2026);
owned DTC contribution 20 to 40 percent (https://eightx.co/blog/amazon-vs-dtc-margin-gap-2026).

### 5. Pricing tier card (SaaS and whitelabel SaaS)
```
Tier Price Billing Seats/limits Feature gates Target segment
Starter <$/mo> monthly <n> <core only> <segment>
Growth (hero) <$/mo> monthly + annual <n> <+ automations> <segment>
Enterprise <custom> annual <unlimited> <full suite> <segment>
Rules: 3-4 tiers, middle tier is the revenue hero, annual = 2 months free,
per-tier churn and trial conversion reviewed monthly.
```

### 6. Weekly growth review note
```
Week of <date>
North star: <metric> = <value> vs threshold <value> Status: in range | flagged
Input metrics: <3-5 metrics with actual vs threshold>
Active experiments: <name, status, interim read, decision: extend|call|change>
Top priority this week: <one action>
Owners and deadlines: <owner> by <specific date>, ...
Blockers: <what, who unblocks, by when>
```

## Metrics

Track a three-tier system: outcomes, journey, diagnostics. Only outcomes are goals; the rest are signals (https://umbrex.com/resources/what-marketing-is/common-failure-modes-in-marketing/).

**Outcomes**
- MER (Marketing Efficiency Ratio) = total revenue / total ad spend. Weekly leadership metric, with a floor.
- aMER = new customer revenue / ad spend. Use for growth spending decisions (https://evolvingo.com/blog/stop-chasing-roas-scale-with-mer-margin).
- LTV:CAC. Floor is 3:1, strong is 5:1, below 2:1 is near break-even (https://blog.margly.io/en/ltv-cac-ratio-ecommerce-growth).
- CAC payback: 3 to 6 months healthy, under 90 days excellent.
- Contribution margin per order and per cohort, after COGS, shipping, payment fees, and ads.
- Repeat purchase rate: 20 to 30 percent typical for DTC, 40 percent plus strong for consumables (https://thedtcplaybook.com/retention-loyalty/).
- Cohort LTV on contribution margin at 90, 180, and 365 days, never on gross revenue (https://retentionside.com/blog/ecommerce-retention-kpis).

**Journey**
- Conversion rate, unbundled: view product, add-to-cart, add-to-cart to checkout, checkout to purchase (https://www.shopify.com/blog/ecommerce-website-optimization). Global ecommerce average sits near 1.9 to 2 percent, Shopify stores near 2.5 to 3 percent (https://www.triplewhale.com/blog/ecommerce-benchmarks).
- Cart abandonment: average 70.22 percent, mobile roughly 80 percent, desktop roughly 66 percent (https://baymard.com/research-articles/current-state-of-checkout-ux).
- Average order value and time between first and second order, the single most improvable retention metric (https://thedtcplaybook.com/retention-loyalty/).
- Trial-to-paid conversion by tier; expansion and upgrade MRR (https://www.maxio.com/blog/tiered-pricing-examples-for-saas-businesses).
- Involuntary churn (failed payments) tracked separately from voluntary churn.

**Diagnostics**
- Email: open rate near 32.8 percent, CTR near 2.65 percent, unsubscribe under 0.17 percent, revenue per email $0.12 to $0.34 for ecommerce (https://shopwhizzy.com/blog/email-marketing-benchmarks-online-stores).
- Flow revenue as a share of total email revenue; target 50 to 70 percent (https://thedtcplaybook.com/retention-loyalty/).
- Creative: CTR, hook rate, and conversion by creative type (static, video, UGC, testimonial, demo).
- Experiment health: test cycle time in days, and learning rate, the percentage of tests producing an actionable insight (https://uncommoninsights.com.au/scaling-guide/growth-hacking-experiments-for-scale).
- Payment recovery: dunning recovery rate, target 40 to 60 percent of failed revenue.

## Tooling in Hermes

- **Research:** `web_search` and `web_extract` for benchmarks, competitor pricing pages, and channel economics. Prefer primary sources (Baymard, published 10-Ks, platform docs) over listicles. Load `deep-research` for multi-round competitor or category dives and `grounded-citations` when a deliverable carries claims.
- **Funnel walkthroughs:** the browser tool to drive a real signup, checkout, or trial flow on desktop and mobile widths, capturing each friction point as a screenshot plus a written observation.
- **Numbers:** `terminal` or `execute_code` with Python to pull CSV exports, compute MER, cohort LTV, ICE scores, and sample sizes. Never do the arithmetic mentally; aggregate in code and verify counts against the ask.
- **Cadence:** `hermes cron` for the daily metric check and the weekly growth review prompt, so the 20-minute review fires on a fixed schedule and never moves.
- **Backlog and learning log:** a single markdown or CSV file in the persona workspace with columns Idea, Hypothesis, Evidence, ICE, Surface, Status, Result. Append per experiment; re-score monthly in code.
- **Delegation:** spawn subagents for the executor half of each workstream and keep the orchestrator half: research agent pulls benchmarks, analytics agent pulls and reconciles numbers, copy agent drafts flow variants, report agent assembles the weekly note (https://www.digitalapplied.com/blog/ai-agent-orchestration-workflows-guide).
- **Human checkpoints:** outbound content, pricing changes, and anything touching billing get explicit human review before it ships. Hybrid beats pure autonomy; isolate agent sandboxes, log every autonomous change, and route exceptions to a human when a metric drops about 15 percent below expectation (https://coey.com/resources/blog/2025/10/03/agentic-workflow-marketings-high-stakes-gamble/) (https://marketingagent.blog/2025/11/02/how-ai-agents-are-rewiring-marketing-teams-for-speed-and-scale-in-2026/).

## Failure Modes

1. **Chasing platform ROAS.** Platform dashboards claim partial credit for the same sale across overlapping channels. When reported ROAS improves while MER worsens, budget is being misallocated (https://www.markework.com/blog/ecommerce-ppc-agency-how-to-choose-manage-and-scale-paid-ads-profitably).
2. **The performance-only trap.** Judging marketing only by immediately attributable conversions starves demand creation, raises CAC every quarter, and pushes the business toward discounts. Symptoms: rising CAC complaints, repetitive transactional creative, dependence on promotions (https://umbrex.com/resources/what-marketing-is/common-failure-modes-in-marketing/).
3. **Discount dependency.** Customers acquired on a deal churn when the deal ends and buy at worse margins. Track lead-to-customer rate in non-discount periods separately (https://retentionside.com/blog/ecommerce-retention-kpis).
4. **Vanity metrics as goals.** Impressions, opens without clicks, and unqualified leads are diagnostics, not outcomes. Require a tiered measurement system with contribution margin and retention at the top (https://umbrex.com/resources/what-marketing-is/common-failure-modes-in-marketing/).
5. **Last-click attribution laundering.** Last-touch over-credits retargeting and landing pages, under-credits content and brand, and turns attribution into an argument for budget preservation rather than a test of causality (https://www.antoinebuteau.com/the-capital-allocation-theory-of-growth-series-9-growth-metrics-failure-modes/).
6. **Channel chasing.** Jumping platform to platform for cheap early efficiency, then watching returns decay as the channel saturates. Fix the conversion and retention system before adding a channel (https://umbrex.com/resources/what-marketing-is/common-failure-modes-in-marketing/).
7. **Blending channel financials.** Marketplace and DTC have different cost structures. A single P&L hides which channel is actually profitable (https://merakibusinessconsulting.com/how-to-scale-your-amazon-business-while-running-a-dtc-ecommerce-brand/).
8. **Tests that cannot finish.** Low-traffic pages plus underpowered tests produce false winners. Screen for sample size before the queue, and cap concurrent tests at 2 to 4 per surface (https://www.zspace.in/blogs/ecommerce-experiment-prioritization).
9. **Automation without an exit.** Flows and agents running unmonitored burn list health and brand trust. Every automated loop needs an unsubscribe guard, a complaint-rate threshold, and an exception route to a human.
10. **Underpriced tiers.** Whitelabel or SaaS tiers priced below the segment's willingness to pay attract low-commitment buyers who churn fastest. Review distribution monthly and keep the middle tier as the revenue hero (https://www.ghlscaleup.com/blog/ghl-white-label-saas-guide).
11. **Ignoring involuntary churn.** Failed payments are the cheapest revenue to recover, and most stacks leave 40 to 60 percent of it on the table without dunning (https://www.saasfactor.co/blogs/the-2025-saas-pricing-playbook-how-to-choose-the-right-model).

## Mapping to David's Products

- **AlphaFlux (multi-tenant SaaS console, Go + Flutter + SurrealDB):** the living example of whitelabel SaaS tier mechanics. Two-tier tenancy means two billing relationships: David's wholesale relationship with each tenant, and each tenant's retail relationship with its end users. Gate features by entitlement data behind feature flags, expose per-tenant usage metering for tenant billing, and use soft limits with notifications rather than hard cuts for B2B overages (https://nevrio.tech/news/white-label-saas-platform-development-guide/). Revenue models to choose from: flat reseller subscription, per-seat wholesale, or platform fee plus revenue share (https://licensesaas.com/blog/how-to-white-label-saas). Run the growth funnel for AlphaFlux signups with the same experiment brief template: trial start, activation event, tier conversion, expansion MRR.
- **AlphaFlux Flutter client:** mobile micro-conversions are the CRO surface. Sticky primary actions, tap-friendly targets, and fast first paint; mobile converts at roughly half the desktop rate, so a mobile-agnostic design silently taxes every paid click.
- **AlphaFlux Go backend:** own the server-side event pipeline. Purchase, activation, and billing webhook events should be emitted from the backend, not only from the client, so ad platform reconciliation and cohort LTV rest on one source of truth.
- **Dokploy deploys on the Hostinger VPS:** experiments ship behind flags with a documented revert path. Because deploys are cheap and Traefik fronts everything, roll out test variants per hostname or path and pull them back in one action.
- **iTaK Learn (Postgres learning platform):** subscription tiers map directly to the pricing tier card. Track trial-to-paid by tier, activation (first lesson completed) as the leading indicator, and voluntary vs involuntary churn separately. Postgres gives you cohort queries for free: build the 90/180/365-day cohort table as a saved view.
- **AlphaSafe (Vaultwarden-based secret manager):** retention here is trust retention. Lifecycle email focuses on security events and renewal reminders, never promotions; discount-driven renewals train the wrong expectation.
- **AlphaVision (TV OS) and iTaK Gaming:** activation and session cadence are the retention metrics; the win-back flow pattern transfers even though there is no cart.
- **Patriot Pest Control (field-service tooling):** the funnel is lead to quote to booking, and the lifecycle flows are seasonal service reminders and re-service win-backs. Cart abandonment maps to abandoned quote forms; the same 24-hour follow-up rule applies.
- **the autonomous coding harness:** the vehicle for growth engineering work. CRO changes to AlphaFlux (checkout, onboarding, entitlement gates) are specified as experiment briefs and executed by so every change arrives with instrumentation, a revert path, and a written hypothesis rather than a silent rewrite.
- **Future projects:** the templates in this skill (experiment brief, funnel audit, flow spec, channel P&L, tier card, weekly review) are product-agnostic. Any new commerce or subscription surface starts by copying them, not by reinventing them.

## Sources

- https://baymard.com/research-articles/current-state-of-checkout-ux
- https://www.shopify.com/blog/ecommerce-website-optimization
- https://www.triplewhale.com/blog/ecommerce-benchmarks
- https://www.eggknite.com/playbooks/lifecycle-email
- https://blog.margly.io/en/ltv-cac-ratio-ecommerce-growth
- https://thedtcplaybook.com/retention-loyalty/
- https://retentionside.com/blog/ecommerce-retention-kpis
- https://shopwhizzy.com/blog/email-marketing-benchmarks-online-stores
- https://www.usekaya.com/blog/ecommerce-advertising-best-practice
- https://www.markework.com/blog/ecommerce-ppc-agency-how-to-choose-manage-and-scale-paid-ads-profitably
- https://evolvingo.com/blog/stop-chasing-roas-scale-with-mer-margin
- https://unbounce.com/conversion-rate-optimization/ecommerce-cro/
- https://buildgrowscale.com/why-roas-stopped-working-blended-efficiency
- https://pages.prebodigital.com/paid-media-strategies-with-conversion-rate-optimization
- https://ahaecommerce.com/strategy/the-multi-channel-illusion
- https://eightx.co/blog/amazon-vs-dtc-margin-gap-2026
- https://thedtcplaybook.com/marketplaces-wholesale/
- https://merakibusinessconsulting.com/how-to-scale-your-amazon-business-while-running-a-dtc-ecommerce-brand/
- https://www.saasfactor.co/blogs/the-2025-saas-pricing-playbook-how-to-choose-the-right-model
- https://ecosire.com/blog/subscription-business-model-complete-guide
- https://www.maxio.com/blog/tiered-pricing-examples-for-saas-businesses
- https://licensesaas.com/blog/how-to-white-label-saas
- https://nevrio.tech/news/white-label-saas-platform-development-guide/
- https://www.ghlscaleup.com/blog/ghl-white-label-saas-guide
- https://www.zspace.in/blogs/ecommerce-experiment-prioritization
- https://maciejturek.com/resources/growth-experimentation-playbook-2025.html
- https://growth-engines.com/insights/ecommerce/ecommerce-a-b-testing-the-data-driven-guide-to-higher-conversions
- https://www.customerimpact.be/en/blog/growth-sprint-cadence/
- https://www.mindilo.com/the-20-minute-weekly-growth-review-that-actually-gets-shit-done/
- https://uncommoninsights.com.au/scaling-guide/growth-hacking-experiments-for-scale
- https://sparkco.ai/blog/build-growth-experiment-prioritization-framework
- https://umbrex.com/resources/what-marketing-is/common-failure-modes-in-marketing/
- https://www.antoinebuteau.com/the-capital-allocation-theory-of-growth-series-9-growth-metrics-failure-modes/
- https://www.mckinsey.com/capabilities/growth-marketing-and-sales/our-insights/reinventing-marketing-workflows-with-agentic-ai
- https://www.bcg.com/publications/2025/cmos-who-move-first-in-agentic-marketing-will-win
- https://coey.com/resources/blog/2025/10/03/agentic-workflow-marketings-high-stakes-gamble/
- https://www.digitalapplied.com/blog/ai-agent-orchestration-workflows-guide
- https://marketingagent.blog/2025/11/02/how-ai-agents-are-rewiring-marketing-teams-for-speed-and-scale-in-2026/
