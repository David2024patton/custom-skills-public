#!/usr/bin/env bash
# Publish a sanitized SINGLE-COMMIT snapshot of custom-skills to the public
# mirror (David2024patton/custom-skills-public). Fail-closed: any blocked
# identifier or any gitleaks finding outside the documented baseline aborts
# the push.
#
# Why squash: the private repo's history predates the scrub (3d666aa) and may
# still carry old network identifiers. The mirror never receives that history;
# every publish is one fresh commit, so the gate IS the whole past.
#
# Usage: scripts/publish-public-mirror.sh
#   MIRROR_URL=... GITLEAKS=/path/to/gitleaks override as needed.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
MIRROR_URL="${MIRROR_URL:-https://github.com/David2024patton/custom-skills-public.git}"
export PATH="$HOME/.local/bin:$PATH"
GITLEAKS="${GITLEAKS:-gitleaks}"
BASELINE="$REPO_ROOT/scripts/gitleaks-baseline.json"

export PYTHONUTF8=1
PYTHON="python"
command -v "$PYTHON" >/dev/null 2>&1 || PYTHON=py

# Deterministic workdir OUTSIDE the repo as a native path: mktemp returns a
# POSIX /tmp path that native Windows git writes to a different location.
WORK="$REPO_ROOT/../.publish-snapshot"
rm -rf "$WORK"; mkdir -p "$WORK"
trap 'rm -rf "$WORK"' EXIT
echo "==> staging snapshot in $WORK"
git clone --quiet --depth 1 --branch main "$REPO_ROOT" "$WORK/snap"
cd "$WORK/snap"
git checkout --quiet --orphan pub
git add -A

# redact-map.json and public-exclude.json are the lists of what to hide: they
# must never leave this repo. Authoritative copies stay private; snapshots go
# without them (the publish tooling reads its config from the private copy).
rm -f scripts/redact-map.json scripts/public-exclude.json
git rm -q --cached scripts/redact-map.json scripts/public-exclude.json 2>/dev/null || true

echo "==> gate 1: redact map + blocked-identifier scan + new-file review"
"$PYTHON" "$REPO_ROOT/scripts/list_mirror_files.py" "$MIRROR_URL" > "$WORK/known-files.txt" 2>/dev/null || : > "$WORK/known-files.txt"
"$PYTHON" "$REPO_ROOT/scripts/sanitize_snapshot.py" "$WORK/snap" "$WORK/known-files.txt"

git add -A   # stage exclusions and index pruning from gate 1

echo "==> gate 2: gitleaks vs documented baseline (normalized diff)"
if ! command -v "$GITLEAKS" >/dev/null 2>&1; then
  echo "FAIL: gitleaks not found (set GITLEAKS= or install to ~/.local/bin)" >&2
  exit 1
fi
"$GITLEAKS" detect --source "$WORK/snap" --no-git \
  --report-format json --report-path "$WORK/leaks.json" --exit-code 0 --no-banner
"$PYTHON" "$REPO_ROOT/scripts/gitleaks_diff.py" "$WORK/leaks.json" "$BASELINE" "$WORK/snap"

echo "==> committing sanitized snapshot"
git -c user.name="custom-skills publisher" -c user.email="publisher@local" \
  commit --quiet -m "Sanitized public snapshot of David2024patton/custom-skills ($(date -u +%Y-%m-%d))"

echo "==> pushing to $MIRROR_URL (force: snapshot history replaces remote main)"
git remote remove mirror 2>/dev/null || true
git remote add mirror "$MIRROR_URL"
git push --quiet --force mirror pub:main

TAG="snapshot-$(date -u +%Y-%m-%d)"
git tag "$TAG" pub 2>/dev/null || true
git push --quiet mirror "refs/tags/$TAG" 2>/dev/null || echo "tag $TAG already exists on the mirror, left as is"
echo "==> tagged: $TAG (consumers: pin a tag, never main)"

echo "==> published: $MIRROR_URL"
