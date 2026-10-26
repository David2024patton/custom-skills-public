# Dependabot: Alerts and Update PRs

Route here for Dependabot alerts, dependency review, and Dependabot
update PRs.

## Reading alerts

```bash
gh api repos/{owner}/{repo}/dependabot/alerts --jq '.[] | select(.state=="open") | {number, severity: .security_advisory.severity, package: .dependency.package.name, manifest: .dependency.manifest_path}'
gh api repos/{owner}/{repo}/dependabot/alerts/<ALERT_NUMBER>
```

Triage by severity and reachability: is the vulnerable function on a
path the project actually runs? An alert on a dev-only tool that never
ships is a different priority from the same alert in the request path.
State which one it is, with the manifest path as evidence.

## Update PRs

- Verify CI on the update PR yourself (`gh pr checks <PR>`), the same
  rule as any PR. A green badge in a list is not a check you ran.
- Prefer grouped updates where the repo's config offers them: one PR
  with a coherent set beats five racing PRs.
- Merge through the normal PR flow of this skill, confirmation rules
  included. Do not use deprecated Dependabot comment commands
  (`@dependabot merge` and friends) as the merge path.
- Read the dependency review before merging a version jump: what
  changed, license changes, and known vulnerabilities introduced or
  removed (queries in `references/github-api-cheatsheet.md`).

## Version update config basics

`.github/dependabot.yml` declares ecosystems, directories, schedules,
and grouping. Keep it minimal and real: one entry per ecosystem and
directory that actually exists, weekly cadence unless the project
says otherwise, groups named by purpose (for example `go-minor`).
Changes to this file go through the normal PR workflow.

## Done

The alert or update PR in question is read back after action, CI state
is quoted from a check run in this session, and the merge, if any,
followed the normal confirmation rules.

## Worked example EX-A3: a grouped update PR

```bash
gh pr view 88 --json title,state,mergeable
gh pr checks 88            # all green, run in this session
gh api repos/{owner}/{repo}/dependency-graph/compare/<BASE>...<HEAD>   # review read
```

The review shows one minor bump group, no license change, two alerts
closed by the update. The PR merges through the normal flow, and the
read-back is `gh pr view 88 --json state,mergedAt` plus a fresh alert
list showing the two alerts gone.
