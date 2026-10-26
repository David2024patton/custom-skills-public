# Source Quality Rubric

Score every source before it supports a claim in a report. Record the tier and the access status in the evidence table.

Access status is separate from tier: `full` (opened and read in full), `partial` (paywalled, blocked, dynamically rendered, or only partly accessible), or `snippet-only` (only a search snippet or summary was seen). A partial or snippet-only source may be Tier A by publisher and still may not solely support a material claim. When access is partial or snippet-only, seek the original document or an equivalent primary source elsewhere, and record the access status in the evidence table and the claim ledger.

## Tiers

**Tier A, primary or near primary.** The source is the thing itself or one step from it. Examples: the statute text, the agency program page, the peer reviewed paper, the official documentation plus the source code, a regulatory filing, the company's own published price list for its own prices, the user's own records for facts about the user.

**Tier B, independent secondary.** A credible source with no stake in the answer reporting on primary evidence. Examples: established journalism citing documents, independent research institutes, university summaries, professional association guidance, a review that opened and tested the thing itself.

**Tier C, interested or weak.** A source that profits from the answer, or that cannot show its method. Examples: vendor surveys, sponsored studies, agency pricing pages, affiliate listicles, press releases, AI generated summaries, unsourced statistics repeated across blogs. Tier C can support a claim about what the seller says or charges. It cannot carry a claim about what is true in the market.

## Scoring checks

Run these six checks and note failures in the evidence table.

1. Authority. Is the publisher the body that decides, measures, or built the thing, or are they repeating someone else?
2. Interest. Does the publisher make money if the reader believes this claim? If yes, tag the claim inline as vendor claim, vendor survey, sponsored study, or interested party.
3. Method. For any number, can you find who was measured, when, and how? A statistic with no findable method is decoration, not evidence.
4. Freshness. What date does the claim describe, not the date the page was crawled? Recheck before repeating any price, rate, rule, or version.
5. Corroboration. Does an independent source with different incentives report the same thing? Two pages repeating one press release are one source.
6. Access. Was the source opened and read in full, or only partially, or only as a snippet? Record full, partial, or snippet-only. Partial and snippet-only sources do not solely support material claims.

## Domain primary source map

- Law, benefits, eligibility: the statute, the regulation, and the administering agency's own program pages, in that order.
- Medicine and health: guidelines from the relevant specialty body, the drug label, peer reviewed trials, then patient facing summaries.
- Software and tools: official docs, the repository source, tests, releases, and issue tracker. Marketing pages last.
- Markets and pricing: published price lists, filings, and transaction data first. Surveys of what sellers say they charge are Tier C for market truth and Tier A for what that seller charges.
- News and events: the primary document or recording first, then at least two independent outlets that did their own reporting.

## Red flags that drop a source a tier

- The page cites a study that does not exist at the link given, or the study says something narrower than the claim.
- The same statistic appears everywhere with no original source, which usually means it was invented once and copied forever.
- The page was updated recently but the data inside is years old.
- The source is another AI's output. Treat it as an unverified draft to cross check, never as evidence.
- The source asks the reader to buy the thing the claim recommends.
6. Access. What did you actually read: the full source, or a snippet? A snippet-only source cannot solely support a material claim.
