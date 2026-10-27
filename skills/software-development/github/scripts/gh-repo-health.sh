#!/usr/bin/env bash
# gh-repo-health.sh: read-only repo health audit (bash form).
# Usage: gh-repo-health.sh <owner>/<repo>
# Checks auth context, default branch, protection or ruleset state, CI
# presence and recent conclusions, code scanning, secret scanning,
# Dependabot enablement, templates, and LICENSE. Prints one line per
# check with its evidence. Exit 0 when the audit ran, regardless of
# findings; 2 on auth or usage errors. Diagnostics on stderr.
set -u

fail() { echo "gh-repo-health: $1" >&2; exit 2; }

[ $# -eq 1 ] || fail "usage: gh-repo-health.sh <owner>/<repo>"
case "$1" in */*) : ;; *) fail "expected <owner>/<repo>, got: $1" ;; esac
command -v gh >/dev/null 2>&1 || fail "gh CLI not found"
gh auth status >/dev/null 2>&1 || fail "gh is not authenticated; run gh auth login"

owner="${1%/*}"; repo="${1#*/}"
line() { echo "CHECK $1: $2 (evidence: $3)"; }

user=$(gh api user --jq .login 2>/dev/null) || fail "gh api user failed"
line "auth context" "authenticated as $user" "gh api user"

view=$(gh repo view "$owner/$repo" --json defaultBranchRef,licenseInfo 2>/dev/null) \
  || fail "gh repo view failed for $owner/$repo"
branch=$(printf '%s' "$view" | sed -n 's/.*"defaultBranchRef":{"name":"\([^"]*\)".*/\1/p')
[ -n "$branch" ] || branch="main"
line "default branch" "$branch" "gh repo view defaultBranchRef"
if printf '%s' "$view" | grep -q '"licenseInfo":null'; then
  line "LICENSE" "MISSING" "gh repo view licenseInfo is null"
else
  line "LICENSE" "present" "gh repo view licenseInfo"
fi

if gh api "repos/$owner/$repo/branches/$branch/protection" >/dev/null 2>&1; then
  line "branch protection" "present on $branch" "GET branches/$branch/protection returned 200"
else
  line "branch protection" "ABSENT on $branch" "GET branches/$branch/protection returned an error"
fi
rulesets=$(gh api "repos/$owner/$repo/rulesets" --jq 'length' 2>/dev/null || echo "?")
line "rulesets" "$rulesets ruleset(s)" "GET repos/$owner/$repo/rulesets"

workflows=$(gh workflow list --repo "$owner/$repo" 2>/dev/null | grep -c . || true)
line "CI workflows" "$workflows workflow(s)" "gh workflow list"
runs=$(gh run list --repo "$owner/$repo" --branch "$branch" --limit 20 --json conclusion --jq '[.[] | select(.conclusion=="success")] | length' 2>/dev/null || echo "?")
line "CI recent success" "$runs of last 20 runs on $branch concluded success" "gh run list"

if gh api "repos/$owner/$repo/code-scanning/alerts" >/dev/null 2>&1; then
  line "code scanning" "enabled (alerts endpoint answers)" "GET code-scanning/alerts"
else
  line "code scanning" "not enabled or not permitted" "GET code-scanning/alerts failed"
fi
if gh api "repos/$owner/$repo/secret-scanning/alerts" >/dev/null 2>&1; then
  line "secret scanning" "enabled (alerts endpoint answers)" "GET secret-scanning/alerts"
else
  line "secret scanning" "not enabled or not permitted" "GET secret-scanning/alerts failed"
fi
if gh api "repos/$owner/$repo/dependabot/alerts" >/dev/null 2>&1; then
  line "Dependabot" "alerts endpoint answers" "GET dependabot/alerts"
else
  line "Dependabot" "not enabled or not permitted" "GET dependabot/alerts failed"
fi
if gh api "repos/$owner/$repo/contents/.github/ISSUE_TEMPLATE" >/dev/null 2>&1; then
  line "issue templates" "present" "GET contents/.github/ISSUE_TEMPLATE"
else
  line "issue templates" "absent" "GET contents/.github/ISSUE_TEMPLATE failed"
fi

echo "AUDIT COMPLETE: read only, nothing was changed"
exit 0
