# Repo Health: The Read-Only Audit

Route here for "audit this repo", "how healthy is this repo", and the
health section of any larger review. This audit is read only. It
reports; it does not fix. Fixes route to their own workflows.

## What it checks

1. Auth context: `gh auth status` and `gh api user --jq .login`, the
   account this audit reads as.
2. Default branch: exists, is the branch protection and rulesets
   actually guard (`references/rulesets-protection.md`).
3. Protection and rulesets: present on the default branch, required
   checks and reviews in place.
4. CI: workflows present, and the recent pass rate over the last 20
   runs on the default branch (`references/actions-workflows.md`).
5. Security features: code scanning, secret scanning, and push
   protection states (`references/security-scanning.md`); Dependabot
   enablement (`references/dependabot.md`).
6. Templates and housekeeping: issue and PR templates present,
   LICENSE present and named, README present.
7. Repo structure: the structure audit from
   `references/repo-structure.md`, run as one section of this report,
   not a separate verdict.

## Commands

```bash
gh repo view --json nameWithOwner,defaultBranchRef,licenseInfo,description
gh api repos/{owner}/{repo}/branches/{branch}/protection
gh api repos/{owner}/{repo}/rulesets
gh run list --branch <default> --limit 20 --json conclusion,status
gh api repos/{owner}/{repo}/code-scanning/alerts --jq 'length'
python3 scripts/repo-structure.py audit --repo <path>
scripts/gh-repo-health.sh <owner>/<repo>    # the same checks, scripted
```

A 404 on the protection read is a finding (no protection), not an
error in the audit. Say which.

## Output

Use the health variant of `references/review-output-template.md`:
one line per check with its state and the read that proved it, then
findings ordered by severity, then the structure audit section. Every
line names its evidence; a check that could not run says why.

## Done

The report is complete when every check above has a state backed by a
read from this session, and the report states plainly that the audit
changed nothing.
