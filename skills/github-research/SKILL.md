---
name: github-research
description: "Search GitHub issues, PRs, and code using the gh CLI."
---

# GitHub Research

Search GitHub for prior art, implementation patterns, and maintainer decisions.

**Relationship to the github skill:** this skill does landscape and
prior-art research only: comparing options across repos, finding how
others solved a problem, identifying software from a quoted string.
Single-repo operations (issues, PRs, reviews, releases, settings, and
every other workflow on one named repo) route to the `github` skill,
not here. The repo structure workflow (applying the planned file
standard to a repo) is also the github skill's; the standard it applies
is the `github-repo-standard` skill's manifest,
`github-repo-standard/assets/repo-standard-manifest.json`.

If a research run concludes that a shortlisted repo needs the planned
file structure applied, it hands off to the github skill's repo
structure workflow and names the manifest above; it does not apply
the standard itself.

## Commands

```bash
# Search issues
gh search issues "topic" --repo owner/repo --limit 20 \
  --json number,title,state,url

# Search merged PRs (highest signal)
gh search prs "topic" --repo owner/repo --merged --limit 20 \
  --json number,title,url

# Search code (use query syntax for path filtering)
gh search code "pattern path:src/" --repo owner/repo --limit 20 \
  --json path,textMatches

# Get full issue or PR details
gh issue view 123 --repo owner/repo --json number,title,body,comments
gh pr view 456 --repo owner/repo --json number,title,body,reviews,files
```

## Repository Landscape Search (comparing alternatives)

When the question is "what are the best open-source options for X", survey
repositories with live data instead of trusting blog roundups:

```bash
gh search repos "secrets manager" --sort stars --limit 15 \
  --json fullName,stargazersCount,description,pushedAt,license
```

- Run several category keyword queries, dedupe by `fullName`, and aggregate
  programmatically (execute_code), not by eyeballing: results rank only
  within one query, and the best project often surfaces under an unexpected
  keyword ("bitwarden compatible" finds what "password manager self hosted"
  misses).
- Stars measure interest, not fitness. Before recommending a shortlisted
  repo, verify three things: last push date (maintained?), actual license
  (see gotchas below), and whether a programmatic/machine-access path exists
  for the user's automation clients.

### Batching discipline for landscape surveys

- **Per-query caps:** cap every query (default 15 results per query; raise
  the cap only when the shortlist is visibly thin). Uncapped surveys burn
  the search rate limit on duplicates.
- **Dedupe keys:** dedupe by `fullName` across all queries, and keep the
  list of queries that surfaced each repo. Provenance is part of the
  result: a repo found by three angles outranks one found by one.
- **Resume behavior:** when a rate limit or an auth failure stops a survey
  mid-run, record which queries completed and which one failed, and resume
  from the failed query instead of restarting. The helper
  `scripts/gh-landscape.py` (read-only; standard library plus the gh CLI)
  runs the queries, dedupes, and writes the sorted JSON shortlist; it
  exits 2 and names the failing query when a run stops early, and it
  refuses cleanly with a one-line message when `gh` is not installed.
  Check the remaining budget with `gh api rate_limit` between batches.

### gh CLI pitfalls
- JSON field names differ per subcommand, and some gh builds are old:
  `gh search repos` returns `stargazersCount`/`fullName`/`pushedAt`, while
  `gh repo view` returns `stargazerCount`/`licenseInfo`. Older builds reject
  fields like `topics` from `--json` and print the valid field list in the
  error; trust that list.
- `license` is an object and often null: parse with
  `(row.get("license") or {}).get("key")`.
- Never pass a bare `--jq 'json'` (jq has no `json` function); omit `--jq`
  and parse stdout in code, or use real jq field paths.
- `gh repo view owner/name` can fail with "not found" on repos that exist;
  fall back to `gh search repos "repo:owner/name" --json ...`. Never
  conclude a repo is missing from a repo-view failure alone.
- GitHub's license key is coarse: "other" covers both benign custom licenses
  and source-available ones (BUSL). Read the repo LICENSE, and check for an
  `ee/` (or similar) directory that signals an open-core split, before
  calling a project open source.

## Identify Software from a Quoted String

When the user posts a screenshot or quotes a fragment (UI label, config key,
error line) and asks what program it came from, search CODE, not the web:
app UI strings are not web-indexed, so a web search for them returns generic
articles about the feature instead of the program that displays it.

1. Grep any checkout you already have FIRST (`search_files`), one call. A
   clean miss is itself the finding: the UI belongs to a separate client repo.
2. Quote the string exactly; quoting matters because unquoted terms get
   tokenized and drown in noise:
   `gh search code '"Global Webhooks Status"' --limit 10`
3. Try several candidate strings in ONE terminal call with `echo` separators
   between queries, not one call per string.
4. Confirm the winner before naming it:
   `gh repo view owner/name --json description,stargazerCount,licenseInfo,primaryLanguage,updatedAt`
   plus `gh api repos/owner/name/readme --jq '.content' | base64 -d`.
5. Code-search hits cluster as an upstream plus forks of the same project;
   pick the upstream by stars and push date before citing a name.
6. Answer the actual question from that project's own README, docs, or
   source, not from the search snippet or memory.

## Repo Packs for Shortlisted Repos

When a shortlisted repo will be studied further or handed to another
agent, do not leave it as links and snippets. Produce a PACK-1 pack of
the repo and cite the pack path in the research report:

- Engine: Repomix, run through the program wrapper for this collection.
- Pack contents: a header naming the source repo and commit, the file
  tree, a file manifest, and the packed file contents.
- Omissions are listed in the manifest, never silent. Files flagged
  SECRET-SUSPECT are listed as omitted and are never redacted in place:
  the pack either excludes them by name or the survey stops and reports
  why, so no reader mistakes an edited file for the original.

A pack is a study artifact. Findings still cite the live repo (file
paths and line numbers at the packed commit), and the pack path travels
with the report so the next agent reads the same tree.

## Worked Examples

**EX-R1, landscape survey end to end.** Question: self-hosted secrets
managers. Four keyword queries ("secrets manager", "secret management
self hosted", "vault alternative", "bitwarden compatible"), each capped
at 15, deduped by `fullName` into one shortlist (the helper script above
produces it). Each shortlisted repo is then verified before any
recommendation: last push date read from the shortlist, license read in
the repo itself (not the search snippet), and the machine-access path
(API or CLI) confirmed from the repo README.

**EX-R2, quoted string identified.** A user quotes the UI label "Global
Webhooks Status" and asks which program shows it. Web search returns
generic articles, so search code instead:
`gh search code '"Global Webhooks Status"' --limit 10`. Hits cluster as
one upstream plus forks; the upstream (most stars, most recent push) is
confirmed with `gh repo view owner/name` and its README, and the answer
comes from that README, not from the search snippet.

## Rate Limits

- Search API: 30 requests/minute
- Check with: `gh api rate_limit --jq '.resources.search'`

## Signal Ranking

1. Merged PRs - decisions that shipped
2. Maintainer comments - authoritative
3. Closed issues with solutions - problems solved
4. Open issues - current problems (lower signal)

## Report Format

```markdown
## Research: [Topic]

### Summary
- Key finding 1 [#123]
- Key finding 2 [PR #456]

### Findings
1. **#123: [Title]** - [summary]. URL: https://...
2. **PR #456: [Title]** - [what it changed]. URL: https://...

### Gaps
- [What you looked for but didn't find]
```

Always include URLs. If nothing relevant exists, say so.
