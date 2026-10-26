---
name: deep-research
description: "Use when researching competitors or topics deeply."
version: 1.1.1
license: MIT
author: Hermes Agent for David Patton
metadata:
 hermes:
 tags:
 - research
 - competitive-intelligence
 - searxng
 - citations
 - synthesis
 - github-corpus
 related_skills: [github-research, competitor-crawl-pipeline, crawl4ai-competitor-intel, domain-fanout, grounded-citations]
---

# Deep Research: SearXNG-First Competitive Intelligence

## When to Use

Any research task in David's work: competitor and market studies (the Set A /
Set B framing in section 1), fact-checking, price verification, prior art,
and bulk GitHub-repo mining (batch ingest + full-read verdicts against his
stack: see `references/github-repo-corpus.md`). SearXNG at <SEARXNG_HOST>
is the default search path whenever it is reachable; web tools are the
fallback, not the start.

Orchestration and synthesis layer; page-level collection belongs to the crawl
layer (section 4). Order of work: frame, search, verify, crawl, ground,
synthesize, review.

**Scope.** This skill is the default search method for ALL research in this
user's work, not only competitor studies: fact-checking a claim, verifying a
price, checking prior art, confirming version-specific behavior. The
SearXNG-first search layer (sections 2-3) and the provenance rules (section 5)
apply to every research task. Only the Set A / Set B competitor framing in
section 1 is specific to feature-field and market commissions; skip that
section for a plain fact-check, but still search via SearXNG and tag method
and date. Defaulting to the generic web search fallback when SearXNG is
reachable is a mistake; the fallback search tool is for when SearXNG is down, 5xx-ing, empty, off-topic
for the query class, or outside its engine mix (section 3).

## 1. The standing method: two top-10 sets before any design work

Trigger: every new feature field and every new market, BEFORE design work
starts. Not after, not alongside. Before.

- **Set A: top 10 competitors the CUSTOMER would compare.** Same buyer, same
 job, same budget band, same market track: what a real customer weighs when
 choosing. For customer-facing audit work such as Patriot Pest Control, the
 operators and services that customer shortlists.
- **Set B: top 10 competitors to the PLATFORM itself.** The products and
 vendors the platform is shortlisted against at platform level. Name the
 platform in the table header with exact casing: AlphaFlux, AlphaVision,
 AlphaSafe, iTaK.

Every entry in both sets carries a pricing note (plan, price, billing period,
source URL, observed date), capability notes (what it does and does not do
for the feature field, one source per claim), and a one-line relevance basis.

The exercise ends with a **named parity target**:

`Match <named competitor>'s <named capability> (test: <observable pass condition>)`

Competitor and capability are both named in that line. "Reach parity" is not
a parity target. Minimum one per feature field or market, written before
design work begins.

Gate: no design doc, spec, or build plan until both sets, pricing, capability
notes, and the parity target exist. Fewer than 10 credible candidates:
declare the shortfall in Gaps with the reason, never pad. Each field or
market gets its own pair: the customer's comparison and the platform's
comparison are different questions.

## 2. Search layer: own SearXNG first

Preferred engine: the operator's own SearXNG metasearch instance (its
endpoint is in the Local binding at the end of this file): multiple engines
per request, no single-engine bias by design, locale switching to see what
is popular in other regions.
A generic web search tool and a page extraction tool are the fallback only
(section 3). Sections 2.1 to 2.4 were live-probed on 2026-10-22; re-probe
after an instance upgrade via the `version` field of the instance's
`/config` page.

### 2.1 Verified request patterns

- `GET /search?q=<query>` returns HTTP 200 HTML: 20 result articles per page
 (`<article class="result`); `&pageno=2` returns the next 20 (pages 1, 2, 3
 verified).
- UA: a browser UA returns 200; so did python-urllib default, empty, curl,
 and bot-style UAs (`/config` reports `limiter.enabled: false`). Send a
 browser UA by default; UA is not the usual failure point here.
- `&format=json` **works since the 2026-10-26 settings fix** (`search.formats`
 gained json; it 403'd before). JSON is now the preferred path: clean
 `results[].url` arrays, verified 10 results for Tokyo and for the
 SOC2-pricing query class. `&format=rss` and others remain unconfigured:
 use json or parse HTML.
- `GET /preferences` returns 200 (form `method="post" action="/preferences"`).
- `GET /config` returns 200 JSON: `version` 2026.9.2+05cd77f71,
 `instance_name` SearXNG, `limiter.enabled` false, `public_instance` false,
 `safe_search` 0, `autocomplete` duckduckgo, 271 engines listed, 83 enabled.
- `GET /stats` returns 200 per-engine response stats (links like
 `/stats?engine=brave`).
- `GET /autocompleter?q=` returns 200 JSON, the only JSON endpoint that
 answered (q=pest returned "pest control near me" among its suggestions).
- Working parameters: `q`, `pageno`, `language`, `time_range` (empty = Anytime,
 `day`, `week`, `month`, `year`), `safesearch` (0 none, 1 moderate, 2
 strict), and 10 `category_*` buttons: general, images, videos, news, music,
 map, it, science, files, and `category_social media` (note the space in that
 last flag's name).
- Verified selectors: URLs via `<h3><a href="http...` (exactly 20 per page,
 matching `class="url_header"`); attribution via `<div class="engines">`
 then `<span>engine name</span>`; responders via `class="engine-name"` rows
 linking `/stats?engine=`; controls are selects `language`, `time_range`,
 `safesearch`. No region/country/location control exists on the results page
 (0 matches, 2026-10-22).

Working fetch pattern (verified shape):

```python
import re, urllib.request, urllib.parse
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
import json as _json, time
def sxng(q, **params):
 time.sleep(2.2) # suspension-safe pacing (429 recovery is 5 min, not instant)
 u = "https://<SEARXNG_HOST>/search?" + urllib.parse.urlencode(dict(q=q, **params))
 r = urllib.request.Request(u + "&format=json"); r.add_header("User-Agent", UA)
 try:
 d = _json.loads(urllib.request.urlopen(r, timeout=40).read().decode())
 urls = [x["url"] for x in d.get("results", []) if x.get("url")]
 if urls:
 return urls, None # JSON path; badges not needed when engines= scoping
 except Exception:
 pass
 r = urllib.request.Request(u); r.add_header("User-Agent", UA) # HTML fallback
 h = urllib.request.urlopen(r, timeout=40).read().decode("utf-8", "replace")
 urls = re.findall(r'<h3><a[^>]*href="(http[^"]+)"', h)
 eng = [re.findall(r'<span>([^<]*)</span>', b) for b in
 re.findall(r'<div class="engines">\s*((?:<span>[^<]*</span>\s*)+)', h)]
 return urls, eng
```

### 2.2 Location and region switching: exactly what works

1. **WORKS per query: `&language=xx-XX` on `/search`.** The preferences
 search-language select offers 112 options, 66 of them language-plus-region
 form (en-US, en-GB, en-AU, en-CA, en-IN, es-MX, es-AR, de-DE and more).
 Proof: query `football` with `language=en-US` returned floridagators.com,
 usafootball.com, bengals.com, colts.com; with `language=en-GB` it returned
 bbc.co.uk (x4), avfc.co.uk, britannica.com. Overlap: **1 of 20 URLs**. The
 results-page select shows `selected` equal to the parameter sent; a default
 request shows `auto` and matched en-US 20/20, so an unmarked query behaves
 as US.
2. **WORKS sticky: the preferences cookie.** POST
 `application/x-www-form-urlencoded` body `language=en-GB` to
 `/preferences` with a cookie jar; the server set 21 setting cookies
 (language, locale, categories, enabled_engines, disabled_engines, tokens,
 theme, and more). Later searches with that jar showed
 `selected=['en-GB']`, and 16 of the 20 URLs from the explicit en-GB run
 were present versus only 6 of the default run's 20. Use the cookie for
 multi-page work in one locale; cite the explicit parameter, since it
 appears in the URL. Quirk: cookie-mode pages returned larger link sets
 (165 and 338 h3 links), so compare by URL presence, not totals.
3. **DOES NOT WORK: `&region=` and `&gl=`.** `region=US-GB` and `gl=GB`
 overlapped the default set by 18 of 20, inside the jitter band, and
 neither appears in the results-page form; `/preferences` has zero
 occurrences of region, country, location, or geo as fields. Do not build
 a workflow on them.
4. **States and cities are query-derived, not engine-derived.** No
 state/city control exists and all 66 locale options are country-level, so
 "what is popular in <state/city>" means putting `city, state` into `q`
 (example: `best pest control company phoenix az`), optionally with an
 explicit locale pass. Record such findings as query-derived; never call
 them engine-reported.
5. **Locale effects are query-dependent.** On that local-service query,
 `language=en-GB` moved only 3 to 5 of 20 URLs versus default across two
 runs and `es-MX` moved 6 of 20, both within jitter; split-culture queries
 like `football` show the effect dramatically. When the market matters,
 pick a query whose results can differ by locale, twice per locale.

### 2.3 Jitter rule: one run is never enough

Four identical default runs of one query returned 20 URLs each with pairwise
overlaps of 19, 18, 15, 18, 15, 14: up to 6 of 20 URLs move by chance. Rule:
run every (query, locale) condition at least twice, compare sets as
intersections in code, and only report differences beyond the observed floor
(worst case 14 of 20, 2026-10-22). Single-run diffs are noise.

### 2.4 Engine reality check: multi-engine by design, verify by badge

- `/config` (2026-10-22): 271 engines listed, 83 enabled. General category
 holds 10 enabled entries: brave, duckduckgo, startpage, google cse,
 wikidata, wikipedia, currency, dictzone, lingva, mymemory translated.
 **Plain `google` and plain `bing` are not enabled**: the Google lane is
 `google cse`, and bing appears only as bing images, bing videos, bing news.
- Responders versus ranking: the sidebar listed 6 responding engines for
 general queries (brave, duckduckgo, startpage, wikidata, google+cse,
 wikipedia), yet eight tallies (five queries, one en-GB pass, pages 2 and 3)
 each came back **100% `google cse` badges, 20 of 20 articles** (2026-10-22).
- Other categories are genuinely mixed: one `category_news` query returned
 31 articles badged duckduckgo news 17, bing news 10, reuters 8, wikinews 5,
 some articles carrying multiple badges.
- Consequences, all mandatory: (a) tally badges on every cited page and
 publish attribution with the date; (b) never write "ranked on Google",
 `google cse` is not the consumer google.com SERP; (c) sidebar responders
 are not ranking engines, cite badges; (d) get breadth from paging, a second
 locale pass, a second category, or fallback tools.
- **`&engines=<name>` works since the 2026-10-26 settings fix** (it returned
 empty on 2026-10-22 because json format was off; the params were never the
 bug). Verified: `engines=mojeek,bing` returned 10 mojeek-first results. Use
 it to scope agent bursts to 2-3 engines and protect the instance; keep
 badge attribution on the HTML path.

## 3. Fallback layer

When <SEARXNG_HOST> is down, 5xx-ing, returns zero results for the query, or
returns mostly irrelevant/low-signal results for the query class (dev-tooling
queries have come back near-unusable; gh CLI plus web tools carried the load),
or a query needs a source outside its engine mix: a web search tool for discovery, then a page extraction tool for content (long
pages truncate to head and tail, full text on disk). Tag fallback claims
method `fallback-web-search`. Use `site:<domain> pricing` queries when the
backend supports operators. For software prior art, implementation patterns,
and maintainer decisions, use the github-research skill (gh CLI); 4.3 has the
essentials. For the product Hermes itself, or any tool whose source sits in a
local checkout, the ordering flips: local source plus the official docs index
(`/docs/llms.txt`) plus gh are the primary sources, and search engines are
discovery-only for that query class (they have returned near-pure noise for
it); tag such claims `[DOC]`/`[SRC]`/`[GITHUB]`, not `fallback-web-search`.

## 4. The crawl layer: credit these skills, do not contradict them

These three skills own page-level collection and validation; this skill
supplies query strategy, dedupe, and synthesis. Where this document and those
skills differ on crawling, those skills win.

- `skills/competitor-crawl-pipeline/SKILL.md` (in this collection)
- `skills/crawl4ai-competitor-intel/SKILL.md` (in this collection)
- `skills/github-research/SKILL.md` (in this collection)

### 4.1 From competitor-crawl-pipeline: curation, crawl master, dossier, validator

- Inputs: curated list of 10+ domains, split by market track when the client
 serves multiple markets; each entry: company, domain, market track, 1 to 3
 candidate URLs.
- Preflight: Crawl4AI container (unclecode/crawl4ai:latest, port 11235) Up in
 `docker ps`, `GET /health` 200; credentials from the operator credential store (see the Local binding)
 (`CRAWL4AI_API_TOKEN` Bearer, `CRAWL4AI_ENDPOINT`).
- Purge loop first: verify every domain live, then remove parked pages,
 ad-server login shells, and out-of-market operators before crawling.
- Crawl master: POST `{"urls":[...]}` to `{endpoint}/crawl` with Bearer token
 and 180s timeout; one raw JSON per domain in
 `CRAWL_RAW/{domain}.{STAMP}.json`; write `MASTER_{STAMP}.json`; 1s delay
 between URLs; retry failures against alternates (www prefix, `/prices`,
 `/pest-control`, market path).
- Evidence contract: arrays of `{text, source_url, evidence_method:"crawl"}`
 for services, pricing, guarantees, CTAs, plus digital_presence and
 per-domain threat_level. Keep the em-dash sweep hook counting U+2014 on
 competitor pricing pages: that is where an em dash leaks into a deliverable.
- Dossier: `data/competitors.json` as `{meta, competitors:[{id:COMP-NN, name,
 domain, market, threat_level, status, crawl_error, evidence,
 digital_presence}], gaps, wins}` with meta counts and validation_status.
- Validator gate, six rules: validated verdict, track coverage, crawl-ok
 floor 75 to 80 percent, claim coverage, source-domain integrity, no
 fabrication. Proven numbers recorded in that skill (run 2026-08-01): 40
 domains, entries COMP-01 through COMP-42, final gate WA 85.0, AZ 81.8,
 overall 83.3, PASS.
- Hazards: transport 200 proves nothing (parked and login shells pass TCP);
 blocked entries keep crawl_error plus manual fallback marker; nothing is
 dropped silently; no em dashes in shipped copy.

### 4.2 From crawl4ai-competitor-intel: extraction procedure and lessons

- Procedure: `docker ps --filter name=crawl4ai` (restart unless-stopped), POST
 `/crawl` with Bearer token, then extract per competitor: services, pricing
 and offers, guarantees, contact and booking paths, trust signals (reviews,
 licenses, BBB), on-page SEO (titles, keywords), anything we lack; diff
 against our own offerings; write `data/competitors.json` for the render
 layer.
- Lessons from its 2026-08-01 run: transport checks lie (GoDaddy parked page,
 ad-server login redirect, HugeDomains for-sale page at $4,895 all passed
 DNS plus HTTP 200; check raw markdown for those markers); Akamai 403 with
 "Blocked by anti-bot protection" is definitive: set crawl_status=blocked
 with the 403 evidence and evidence_method=manual, do not retry; verify
 every claim string verbatim (case-insensitive substring) against raw
 markdown, drop unverified claims, never infer; build data files as Python
 files because bash heredocs over about 8KB truncate silently; report honest
 per-track math even when a gate fails; manual fallback entries need a live
 http(s) source_url; the purge and replace loop re-crawls ONLY new domains,
 keeps existing evidence, drops gaps referencing purged competitors;
 markdown artifacts (line-broken stats, curly apostrophes, bold splits)
 break verbatim checks, so re-file the exact raw string instead of relaxing
 it; re-run `tools/validate_competitors.py` until it exits 0.

### 4.3 From github-research: prior art and implementation evidence

- Commands: `gh search issues`; `gh search prs --merged` (highest signal);
 `gh search code`; `gh issue view`; `gh pr view`. For landscape questions,
 run `gh search repos <kw> --sort stars --limit 15 --json
 fullName,stargazersCount,description,pushedAt,license` over several keyword
 queries, dedupe by fullName, aggregate programmatically, never by eyeball.
- Stars measure interest, not fitness: verify last push date, the real
 license (the `license` object is often null and key `other` can hide
 BUSL-style terms; read LICENSE and check for an `ee/` directory), and
 whether a machine-access path exists.
- Pitfalls: JSON field names differ per subcommand and older builds reject
 fields, trust the printed valid list; never pass a bare `--jq 'json'`;
 `gh repo view` can fail for repos that exist, fall back to
 `gh search repos "repo:owner/name"`.
- Rate limit: search API 30 requests per minute (`gh api rate_limit`).
- Signal ranking: merged PRs, then maintainer comments, then closed issues
 with solutions, then open issues. Report format: numbered findings, every
 item with its URL, and an explicit statement when nothing relevant exists.
- Bulk repo digests (a pasted batch of GitHub links, full ingestion, verdict
 per repo against his stack): `references/github-repo-corpus.md`.

### 4.4 Repo-to-text packs (PACK-1)

1. "For every repo studied at deep or exhaustive effort, write a repo-to-text pack into the run folder at repos/NN-owner-repo.md, numbered in fit order."
2. "A pack is plain Markdown, self-contained, and safe to hand to any agent: it contains no keys, tokens, credentials, or personal data, and no code text from the repo."
3. "Packs are evidence, not decoration: the report must name which pack techniques it used or rejected, and packs are filed with the run so a later run can ingest them instead of re-studying the repo."

The pack format is defined in `references/repo-to-text-pack.md`. Builder script spec (backlog S1, `scripts/repo_to_text.py`): inputs a repo URL or local clone path; refuses private repos; reads README, LICENSE, tree, and release metadata through public interfaces only; redacts anything matching common secret patterns; emits the pack skeleton with the technique inventory left as a fill-in section for the agent (technique extraction is judgment, not scraping).

## 4. Run mechanics: effort, ledger, stop rules

- Ask the user for one line of scope approval before a deep or exhaustive run, or any
 batch of lookups larger than a handful, and run quick and standard effort immediately
 without waiting. If no user is present, proceed at standard effort, record the
 assumption in the method note, and surface it in the deliverable.
- Choose an effort level by risk and ambiguity, where a hop means one deliberate
 information action that changes the picture: a search, a full source read, a citation
 followed, or a counterevidence check.
 - quick: low risk checks, 2 to 4 hops across at least 2 source classes.
 - standard: normal research, 5 to 8 hops across at least 3 source classes.
 - deep: broad synthesis and due diligence, 9 to 14 hops across at least 4 source classes.
 - exhaustive: contested or high stakes questions, 15 or more hops across at least 5 source classes.
 - Source classes (what each tier counts): **primary** (the document, statute, paper,
 official docs, or first-party price page itself), **secondary** (credible reporting
 or analysis of a primary source), **tertiary** (aggregators, wikis, directories),
 **community** (forums, issues, threads), **first-party-internal** (your own
 artifacts: code, ledgers, records).
- Treat hop counts as planning targets, not quotas, and stop when the high impact
 claims are supported or when more searching is unlikely to change the conclusion.
- Seed and deepen queries with [the query playbook](references/query-playbook.md).
- **Perspective panels before synthesis (flagship deep and exhaustive runs).**
 Before you outline the report, fan out three perspective outlines in parallel
 via subagent delegation, each a self-contained brief with the question, the evidence
 collected so far, and its stance: (1) the practitioner who does this work
 weekly, (2) the skeptic hunting the load-bearing flaw, (3) the adjacent-domain
 expert whose field solves the same shape of problem. Union the outlines by
 unique finding, then synthesize. Panels attack the measured synthesis gap:
 agents find sources fine and organize them badly (arXiv 2601.12369).
 - Context perspectives, chosen by audience, always in addition to the three:
 a **residential** deliverable (household, family, personal finance, home
 tech) adds the household-privacy perspective (what does this leak about the
 home, who else sees it); a **corporate** deliverable (B2B, regulated,
 enterprise sales) adds the buyer-and-compliance perspective (what does the
 economic buyer challenge, which control or regulation touches this). Name
 the audience and the context perspective you added in the method note.

### Gate G: mandatory GitHub step (top 10 studied repos per topic)

**Gate G: the GitHub step inside the gate.** Gate G is mandatory for deep and exhaustive runs, and for any run whose topic is software, a tool, a library, a method with public implementations, or a market with open-source competitors. Gate G runs inside the research loop, after broad seeding and before the counterevidence search, so repo findings can redirect queries. The claim ledger gains no new fields; repo claims are ordinary claims whose evidence items happen to be repos.

1. "Before synthesis, find the top related GitHub repositories for the topic: fit first (does this repo actually do the thing being researched), stars second, license always recorded from the repo's own LICENSE file. Target ten; if fewer than ten credible repos exist, declare the shortfall instead of padding."
2. "Study, do not just list: for each repo read the README, the license, the release or commit recency, and at least one structural element (tree, configuration, or core module description). A repo seen only as a search snippet is snippet-only evidence and cannot be the sole support for a material claim."
3. "Record each repo in the evidence ledger as its own evidence item, with fields: repo, URL, stars as of date, license, last activity, fit note, technique taken. Techniques and architecture only; never copy code text from any repo, whatever its license."
4. "A run that skips Gate G must say so in the method note and name why the topic has no GitHub prior art. Silence is a failed gate."

Skeptic probe (added to the skeptic pass for any run under Gate G): "Which studied repo most threatens the conclusion, and was it read beyond its README?"

- **Hierarchical delegation for wide questions.** When a question splits into
 more dimensions than one pass can hold, spawn one subagent per dimension with
 a shared output schema (findings with evidence IDs, gaps, per-dimension hop
 ledger), each writing into its own sub-ledger folder under the run folder;
 the parent merges ledgers by union and runs the skeptic pass over the merged
 set. This is the `domain-fanout` pattern with ledgers at every level. Coverage
 in the method note reads dimensions completed / planned.
- Keep the run on disk with this skill's ledger tooling, path relative to wherever the
 skill is installed: `python3 <skill-dir>/scripts/research_ledger.py init --question
 "the exact question"` (init requires `--question`), then `add-hop`, `add-evidence`,
 `add-claim`, `status`, and `lint` before delivery. lint blocks on warnings too; run
 `lint --allow-warnings` only when David accepts the disclosed warnings. lint is
 structural: it cannot detect an invented source, so verification against reality
 stays your step per the pre-ship review pass.

## 5. Grounding and provenance: every number carries its source

**Portability rule (standing, every deliverable):**

1. "Every instruction, example, and output of this skill must be runnable by an AI agent that has none of the author's accounts, keys, machines, or history. Name operations, not products or private endpoints. Where a step needs a credential in some environments, say 'use the search or repository access your environment provides' and never name a saved credential."
2. "Research outputs carry no secrets by construction: if a source contains a key, token, or personal data, the finding is recorded as 'a credential-shaped value was present' with its location, never the value."

- Score every source with [the source quality rubric](references/source-quality-rubric.md) and keep its tier in the evidence table.
- Per-claim citation: each sentence stating a fact gets its own source URL;
 one URL for a paragraph of five numbers is not a citation.
- Method tags on every claim: `[LIVE]` fetched by this skill's SearXNG or
 fallback pass, with fetch date; `[CRAWL]` extracted by the crawl layer from
 raw markdown with source_url; `[GITHUB]` gh CLI output with repo and
 issue/PR number; `[DOC]` vendor's own documentation; `[SECONDARY]` a named
 third-party publication; `[EST]` estimate with its method in the same
 bullet; `[UNVERIFIED]` unconfirmed, allowed only under Gaps, never in
 Findings.
- Live-verified versus estimated is always explicit. A figure without a
 source does not appear at all: the anti-fabrication floor (validator rule
 six, section 4.1).
- Pricing rows carry price, currency, billing period, plan name, source URL,
 observed date, method tag. Re-fetch prices observed more than 30 days before
 ship date and update the stamp (stale-pricing rule, section 7.5).
- Prices can differ by locale: capture them during the same
 `language=xx-XX` pass used for that market and record the parameter with
 the citation.

## 6. Synthesis structure for deliverables

- Write report files from [the report template](references/report-template.md).

1. **Findings**: what is true, each sentence cited with method tag, URL, and
 date, plus which engine produced the ranking evidence and how many runs
 agreed.
2. **Competitor tables**, one per set. Set A columns: rank, company, domain,
 why the customer compares it, date-stamped pricing, capability notes vs
 the feature field, threat level, source URLs. Set B columns: the same,
 with overlap surface replacing the customer-comparison column. Rows built
 and counted in code, deduped by domain; 10 rows each unless a shortfall is
 declared in Gaps with the reason.
3. **Pricing**: its own table, date-stamped provenance on every row (price,
 currency, period, plan, URL, observed date, method tag), regional
 variants listed per locale where captured.
4. **Gaps**: what the competitor sets have that we lack or do worse, what we
 do better (wins), plus research gaps: empty queries, blocked sources, every
 `[UNVERIFIED]` item.
5. **Parity targets**: the named targets from section 1, each with
 competitor, capability, observable pass test.
6. **Recommendations**: ordered actions, each traceable to a gap or finding
 above; no recommendation without a citation behind its premise.
7. **Appendix**: query log (query, parameters, locale, date, run count),
 engine attribution tallies, crawl summary (domains, method, dates),
 validator output.

## 7. Anti-bias checks and failure modes

### 7.1 Search-engine bias

- Listicles and "best X" roundups are ranking-manipulated: treat them as
 leads, not evidence, and convert every name into a crawl with a source_url
 before it enters a table.
- Single-instance bias: this instance's general ranking was 100% google cse
 on every page-1 tally of 2026-10-22. Report that attribution and
 cross-check any page-1 claim with a second pass (other locale, other
 category, or fallback tools).
- SearXNG order is not Google rank: never write "position N on Google" from
 these results, never treat position as market share.
- Jitter: up to 6 of 20 URLs moved between identical runs; two runs per
 condition minimum (section 2.3).
- Autocomplete is a separate signal (duckduckgo-configured per /config):
 anecdote unless collected systematically with counts.
- Query-framing bias: one phrasing surfaces one neighborhood. Run
 alternatives, pricing, comparison, and category phrasings per field, and
 log every query including the empty ones.

### 7.2 Stale pricing

- Every price carries an observed date; anything older than 30 days is
 re-fetched before shipping.
- Promo, trial, and "starting at" prices are labeled with their footnote
 conditions or not quoted.
- Crawl raw files are stamped `{domain}.{STAMP}.json`; when sources disagree,
 trust the newer verified fetch, not the cached one.

### 7.3 US-only assumptions

- The default locale behaved as en-US in probes (default matched en-US 20/20),
 so an unmarked query is effectively US. For other markets run the explicit
 `language=xx-XX` pass (66 country-locale options) and state the locale.
- Per region check currency, tax display, regional plan names, coverage or
 shipping limits, legal terms: a US price is not a global price.
- State and city claims are query-derived (no engine geo control exists);
 label them that way (section 2.2 rule 4).

### 7.4 Collection failure modes (crawl-layer lessons, kept alive)

- Transport 200 lies; anti-bot 403 is definitive (mark blocked with evidence
 plus evidence_method=manual, no retries). Verbatim checks fail on markdown
 artifacts: re-file the exact raw string, never relax it. Heredocs truncate
 builds: write Python files to disk, verify JSON parses first. Silent drops
 fail the validator: purged entries go through the purge and replace loop
 and their gaps are removed.
- Instance quirks: json and `engines=` fixed 2026-10-26; HTML parse and badge
 tally remain valid fallbacks. Rate limits: 1s between crawl URLs, gh search
 30 per minute, 2.2s between SearXNG queries.
- Engine-suspension failure mode (2026-10-25/26): all commercial engines
 suspended against the home IP (429/CAPTCHA; defaults were 1h/24h/15d/7d)
 while the instance itself stayed healthy. On 0 URLs, first fetch
 `/search?q=test&format=json` and read per-engine `error` fields; the fixed
 settings.yml recovers 429s in 5 min and CAPTCHAs in 30 min.
- Fabricated citations are the terminal failure: untraceable facts are
 deleted or moved to Gaps as `[UNVERIFIED]`.

### 7.5 Pre-ship review pass (all must pass; automate where possible)

- [ ] Set A and Set B present, 10 rows each or declared shortfall.
- [ ] Pricing table has date-stamped provenance on every row; nothing older
 than 30 days left un-rechecked.
- [ ] Every number carries a method tag plus URL; no `[UNVERIFIED]` item in
 Findings.
- [ ] Named parity target present (competitor, capability, test).
- [ ] Badge tallies reported for ranking claims; locale parameters recorded
 for market claims; run counts meet the jitter rule.
- [ ] Brand casing exact: AlphaFlux, AlphaVision, AlphaSafe, iTaK,
 Patriot Pest Control.
- [ ] ASCII only, zero em dashes (U+2014) including pasted competitor text;
 sweep it the way the crawl layer sweeps raw markdown.
- [ ] Counts (rows, overlaps, badges) computed in code, not by eye.
- [ ] Plan-changing (premise) claims spot-verified LIVE before synthesis: for each
 claim that changes the work, re-run the check yourself (the math, the gh api
 call, the raw source fetch) and record the verification, not just the tag.
 The 2026-10-25 emulator run verified 7 load-bearing claims this way; all held.
- [ ] Cited file paths and line numbers re-checked against the actual repo (raw
 fetch or gh api), because a correct claim with a wrong path still misleads the
 implementer: that run cited `core/hw/gdrom/descrambl.cpp` when the code lives
 in `core/reios/reios.cpp:60` (content verified, path wrong).
- [ ] Absence claims verified repo-wide before synthesis: "no such file/symbol in
 the repo" must come from a whole-repo check (`gh api "search/code?q=..."` or
 recursive grep), never a single-file grep: star re-exports hide symbols from
 text search and a version-skewed local checkout under-reports. When local
 grep and upstream code search disagree, report both and tag the skew.
- [ ] Validator mindset applied: no fabrication, claim coverage,
 source-domain integrity.
- [ ] "Every instruction, example, and output of this skill must be runnable by an AI agent that has none of the author's accounts, keys, machines, or history. Name operations, not products or private endpoints. Where a step needs a credential in some environments, say 'use the search or repository access your environment provides' and never name a saved credential."
- [ ] "Research outputs carry no secrets by construction: if a source contains a key, token, or personal data, the finding is recorded as 'a credential-shaped value was present' with its location, never the value."

## 8. Runbook

1. Frame: name the feature field or market; write Set A and Set B definitions
 before running a single query.
2. Candidate harvest on SearXNG: alternatives, pricing, comparison, category,
 and review-thread phrasings, explicit locale when the market is not US, two
 runs each, capturing URL, parameters, date, badge tally.
3. Location passes: repeat step 2 per market with `language=xx-XX`; for city
 or state questions add `city, state` to `q` and label query-derived.
4. Assemble the pool in code: dedupe by domain, join badge tallies, keep
 per-query provenance rows, count programmatically.
5. Cut to the top 10 per set with written rationale: Set A by customer
 comparability (same buyer, job, budget band, market track); Set B by
 platform overlap (same capability surface a shortlist weighs).
6. Capture pricing and capabilities through the crawl layer (4.1, 4.2):
 health check, curated live domains, purge loop, crawl, verbatim evidence
 with source_url and evidence_method, validator gate.
7. Pull software prior art through github-research (4.3) whenever the feature
 field is software behavior.
8. Write the named parity target (competitor, capability, observable test)
 into the Parity Targets section.
9. Synthesize in section 6 order, tagging every claim per section 5.
10. Run the section 7.5 review pass, fix findings, ship.
11. File the deliverable in the research repo (section 11): Markdown source plus
 the end-result PDF, under the proper category, then push.

## 9. Writing rules for this skill's outputs

- ASCII only. Zero em dashes (U+2014) anywhere; use a period, comma, or
 colon instead.
- Brand casing exact, never re-cased by tooling or paraphrase: AlphaFlux,
 AlphaVision, AlphaSafe, iTaK, Patriot Pest Control.
- No fabricated sources, numbers, or quotes; every figure carries a method
 tag and a URL (or a local file path for skill files and raw crawl JSON).
- Plain dated claims over adjectives: "pricing page fetched 2026-10-22 listed
 $X per month" beats "affordable".
- When research comes up empty, state the query and the date; an honest
 empty is a result.

## 10. Quick reference

- Search: `https://<SEARXNG_HOST>/search?q=<query>&language=<xx-XX>&pageno=N&time_range=<day|week|month|year>&safesearch=<0|1|2>&format=json`
 (json works since 2026-10-26; `engines=a,b` scopes bursts; rss still absent);
 `/autocompleter?q=` also JSON.
- Locale: `language` parameter (112 options, 66 country locales) or POST
 `/preferences` cookie (21 cookies); `region` and `gl` ignored.
- Attribution: per-result `<div class="engines">` badges plus sidebar stats;
 `engines=` is for scoping, not attribution. Runs: 2+ per (query, locale),
 jitter floor 14 of 20.
- Deliverable order: Findings, Competitor tables, Pricing (date-stamped),
 Gaps, Parity targets, Recommendations, Appendix (query log).

## 11. Delivery: PDF end result and the shown checklist

- **The end result of every deep or exhaustive run is a PDF.** Render the final
 report with the pdf skill (`pdf_create.py` from its `scripts/`), verify it with
 `pdf_read.py --meta` (page count and title must be real), and deliver the PDF
 as the artifact: file it next to its Markdown source in the research repo.
 The Markdown stays the editable source; the PDF is what the reader gets.
- **Every delivery ends with the checklist shown to the user.** Before you
 deliver, run this checklist and include the completed boxes IN the chat reply
 and as the report's final section, so the reader sees exactly what was gated:

 ```
 Delivery checklist (run and show; a missing box is a disclosed gap)
 - [ ] Scope approved or assumption recorded (method note)
 - [ ] Effort level and hop count recorded; stop condition named
 - [ ] Ledger on disk: hops, evidence with Access and Tier, claims with verdicts
 - [ ] Every high-impact claim has a Tier A source plus corroboration
 - [ ] Counterevidence search run; what survived and what died recorded
 - [ ] Skeptic pass run on the draft; fixes applied or claims cut
 - [ ] lint clean (or warnings accepted in writing by David)
 - [ ] Evidence IDs cited in the report all exist in the ledger
 - [ ] PDF rendered, page count verified, filed beside the Markdown
 - [ ] Gaps and unverified items listed, never hidden
 ```

- **Human gate.** Before writing any outcome to persistent memory, a repo, or
 production, if a load-bearing claim is WEAKENED or DIES, a critical control
 is GAP, or the benchmark score is under 7, emit HUMAN_GATE_REQUIRED with the
 assertion, evidence IDs, and proposed remediation, and wait for David. The
 system proposes; a person decides.

## 12. Filing: the research repo (standing order)

Every research run ends by filing its output in David's research archive:

- **Repo:** the operator's research archive (local clone path and remote in the Local binding; private).
- **Path shape:** `<category>/<topic>/YYYY-MM-DD-<slug>.md`. Categories: `gaming/`
 (incl. `gaming/emulation/`), `saas/` (incl. `saas/competitors/`), `marketing/`,
 `infrastructure/`, `ai/`, `security/`, `misc/`. New categories go in the repo
 README first, then get used.
- **The end-result synthesis also ships as a PDF** rendered next to its Markdown
 source through the pdf skill's shipped chain: `python scripts/md_to_pdf_spec.py
 report.md -o spec.json`, then `pdf_create.py spec.json -o out.pdf`, verified
 with `pdf_read.py --meta`. Never hand-roll a Markdown-to-spec converter; the
 shipped one escapes reportlab markup and normalizes dashes. Supporting detail
 reports file beside the master in the same dated folder.
- **Never silently edit filed findings.** Verification notes (like the 2026-10-25
 premise-check pass) are appended as an addendum or a sibling file; the original
 research text keeps its method tags and URLs as written.
- Filing to the research repo is the standing requirement; a report that exists
 only in chat or a home-directory temp file is not filed. Git push is opt-in: push only when the user asked for a push in this run.


## Sources

- Live probes of the operator's SearXNG instance (paths `/`, `/search`,
 `/preferences`, `/config`, `/stats`, `/autocompleter`), 2026-10-22.
- skills/competitor-crawl-pipeline/SKILL.md
- skills/crawl4ai-competitor-intel/SKILL.md
- skills/github-research/SKILL.md
- Instance-surfaced links: https://docs.searxng.org/ (config DOCS_URL) and
 https://searx.space (from the no-results page).

## Local binding (2026-10-26)

- Bound fact: the operator's SearXNG metasearch instance is at https://search.example.com/ (config page at https://search.example.com/config).
- Bound fact: the crawl-layer skills were first installed under a Windows user profile path on the operator's machine, inside that profile's local app-data skills folder for the original runtime; in this collection they live at the relative paths section 4 names.
- Bound fact: crawl credentials live in a file named CREDENTIALS.md in the operator workspace.
- Bound fact: the research archive is a local clone at G:/Business/research of the private GitHub repo github.com/David2024patton/research.
- Why it is bound: this method was built and live-probed against the operator's own search instance, crawl setup, and archive; those are the installs its standing orders point at.
- Portable assumption: any SearXNG instance (or a generic web search tool), any credential store, and any research archive repo work; the neutral text names the capabilities and the configuration keys, not the operator's values.
