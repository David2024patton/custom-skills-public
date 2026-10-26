#!/usr/bin/env bash
# gh-ci-diagnose.sh: read-only CI failure diagnosis.
# Usage: gh-ci-diagnose.sh <run ID or PR number>
# Prints failed jobs, the failed step log tail per job (last 100 lines),
# and a first classification per failure (infra, flaky suspect, real)
# with the evidence line that drove it.
# Exit 0 on a completed diagnosis, 2 on auth or usage errors.
set -u

fail() { echo "gh-ci-diagnose: $1" >&2; exit 2; }

[ $# -eq 1 ] || fail "usage: gh-ci-diagnose.sh <run ID or PR number>"
command -v gh >/dev/null 2>&1 || fail "gh CLI not found"
gh auth status >/dev/null 2>&1 || fail "gh is not authenticated; run gh auth login"

arg="$1"
case "$arg" in *[!0-9]*) fail "expected a numeric run ID or PR number, got: $arg" ;; esac

run_id="$arg"
if ! gh run view "$run_id" --json databaseId >/dev/null 2>&1; then
  run_id=$(gh pr view "$arg" --json headRefName --jq .headRefName 2>/dev/null) \
    || fail "argument is neither a run ID nor a PR in this repo"
  branch="$run_id"
  run_id=$(gh run list --branch "$branch" --limit 1 --json databaseId --jq '.[0].databaseId' 2>/dev/null)
  [ -n "$run_id" ] && [ "$run_id" != "null" ] || fail "no workflow run found for PR $arg"
  echo "PR $arg: latest run on branch $branch is $run_id" >&2
fi

echo "Run: $run_id"
gh run view "$run_id" --json status,conclusion,workflowName,headBranch \
  || fail "gh run view failed for run $run_id"

log=$(gh run view "$run_id" --log-failed 2>/dev/null | tail -100)
if [ -z "$log" ]; then
  echo "No failed step logs: the run has no failed jobs, or logs have expired."
  exit 0
fi

echo "--- failed step log tail (last 100 lines) ---"
printf '%s\n' "$log"
echo "--- classification ---"
class="real"; evidence="failure output maps to code or test behavior"
if printf '%s' "$log" | grep -qiE 'runner has received a shutdown|No space left on device|Could not resolve host|connection timed out|API rate limit'; then
  class="infra"; evidence=$(printf '%s' "$log" | grep -iE 'runner has received a shutdown|No space left on device|Could not resolve host|connection timed out|API rate limit' | head -1)
elif printf '%s' "$log" | grep -qiE 'flaky|timed out waiting|race condition detected'; then
  class="flaky suspect"; evidence=$(printf '%s' "$log" | grep -iE 'flaky|timed out waiting|race condition detected' | head -1)
fi
echo "classification: $class"
echo "evidence: $evidence"
echo "note: a first classification only; a second identical failure reclassifies flaky suspect as real"
exit 0
