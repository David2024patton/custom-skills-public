#!/usr/bin/env bash
# gh-pr-ready.sh: read-only PR merge readiness check.
# Usage: gh-pr-ready.sh <PR number or PR URL>
# Prints READY or NOT READY plus one line per blocker with evidence.
# Exit 0 ready, 1 not ready, 2 auth or usage errors. Diagnostics on stderr.
set -u

fail() { echo "gh-pr-ready: $1" >&2; exit 2; }

[ $# -eq 1 ] || fail "usage: gh-pr-ready.sh <PR number or PR URL>"
command -v gh >/dev/null 2>&1 || fail "gh CLI not found"
gh auth status >/dev/null 2>&1 || fail "gh is not authenticated; run gh auth login"

arg="$1"
num="${arg##*/}"
case "$num" in ''|*[!0-9]*) fail "cannot parse a PR number from: $arg" ;; esac

json=$(gh pr view "$num" --json state,isDraft,reviewDecision,mergeable,mergeStateStatus,title 2>/dev/null) \
  || fail "gh pr view failed for PR $num"

blockers=0
add_blocker() { echo "BLOCKER: $1"; blockers=$((blockers+1)); }

state=$(printf '%s' "$json" | sed -n 's/.*"state":"\([A-Z]*\)".*/\1/p' | head -1)
draft=$(printf '%s' "$json" | grep -o '"isDraft":[^,}]*' | head -1)
review=$(printf '%s' "$json" | sed -n 's/.*"reviewDecision":"\([A-Z_]*\)".*/\1/p' | head -1)
mergeable=$(printf '%s' "$json" | sed -n 's/.*"mergeable":"\([A-Z_]*\)".*/\1/p' | head -1)

[ "$state" = "OPEN" ] || add_blocker "PR state is ${state:-unknown}, not OPEN (evidence: gh pr view state)"
[ "$draft" = '"isDraft":true' ] && add_blocker "PR is still a draft (evidence: isDraft=true)"
[ "$review" = "APPROVED" ] || add_blocker "review decision is ${review:-none}, not APPROVED (evidence: gh pr view reviewDecision)"
[ "$mergeable" = "MERGEABLE" ] || add_blocker "mergeable state is ${mergeable:-unknown} (evidence: gh pr view mergeable)"

checks=$(gh pr checks "$num" 2>/dev/null)
if [ -z "$checks" ]; then
  add_blocker "no CI checks reported (evidence: gh pr checks returned nothing)"
elif printf '%s' "$checks" | grep -qiE 'fail|pending'; then
  while IFS= read -r line; do
    add_blocker "check not passing: $line (evidence: gh pr checks)"
  done <<EOF
$(printf '%s' "$checks" | grep -iE 'fail|pending')
EOF
fi

owner_repo=$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null) \
  || fail "cannot resolve the current repo; run inside a repo checkout"
owner="${owner_repo%/*}"; repo="${owner_repo#*/}"
threads=$(gh api graphql -f query="query { repository(owner: \"$owner\", name: \"$repo\") { pullRequest(number: $num) { reviewThreads(first: 100) { nodes { isResolved } } } } }" --jq '[.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved | not)] | length' 2>/dev/null || echo "")
if [ -n "$threads" ] && [ "$threads" != "0" ]; then
  add_blocker "$threads review thread(s) unresolved (evidence: GraphQL reviewThreads read)"
fi

if [ "$blockers" -eq 0 ]; then
  echo "READY: PR $num is open, approved, mergeable, checks passing, threads resolved"
  exit 0
fi
echo "NOT READY: PR $num has $blockers blocker(s)"
exit 1
