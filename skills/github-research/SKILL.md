---
name: github-research
description: "Search GitHub issues, PRs, and code using the gh CLI."
---

# GitHub Research

Search GitHub for prior art, implementation patterns, and maintainer decisions.

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

## Rate Limits

- Search API: 30 requests/minute
- Check with: `gh api rate_limit --jq '.resources.search'`

## Signal Ranking

1. Merged PRs — decisions that shipped
2. Maintainer comments — authoritative
3. Closed issues with solutions — problems solved
4. Open issues — current problems (lower signal)

## Report Format

```markdown
## Research: [Topic]

### Summary
- Key finding 1 [#123]
- Key finding 2 [PR #456]

### Findings
1. **#123: [Title]** — [summary]. URL: https://...
2. **PR #456: [Title]** — [what it changed]. URL: https://...

### Gaps
- [What you looked for but didn't find]
```

Always include URLs. If nothing relevant exists, say so.
