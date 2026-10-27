# Search Playbooks: Cross-Repo Sweeps

Route here for work that spans repos: stale PR sweeps, usage sweeps,
org triage. Single repo work stays in its own reference file.

## Hard rules

- Counts first, then the list. Report how many results a sweep found
  before presenting items, so the reader knows the shape of the whole
  before the parts.
- Never act across repos without a per repo plan. A sweep produces a
  read-only report; any write happens repo by repo, each under that
  repo workflow's own rules and confirmations.
- Search results rank within one query only. State the query text with
  the results, so the sweep can be rerun and compared.

## Patterns

```bash
# Stale PR sweep: open PRs untouched for 30 or more days, across an org
gh search prs --owner <org> --state open -- "updated:<$(date -d '30 days ago' +%F)" --json repository,number,title,updatedAt --limit 100
# Usage sweep: where is a string, symbol, or workflow used
gh search code "<term>" --owner <org> --json repository,path --limit 100
# Org triage: open issues with a label, grouped by repo
gh search issues --owner <org> --label "needs-triage" --state open --json repository,number,title --limit 100
# API form, when the porcelain lacks a qualifier
gh api -X GET search/issues -f q='org:<org> is:pr is:open' -f per_page=100
```

## Sweep shape

1. Run the count form of the query (or count the returned list with a
   capped limit and say the cap).
2. Present the list grouped by repo, oldest or most severe first.
3. Close with the per repo plan the sweep implies, as a proposal. The
   sweep itself changed nothing, and the report says so.

## Done

Counts and list come from the same query in the same session, queries
are quoted verbatim, and no cross-repo write is claimed or performed.
