#!/usr/bin/env bash
# Publish a sanitized SINGLE-COMMIT snapshot of custom-skills to the public
# mirror (David2024patton/custom-skills-public). Fail-closed: any blocked
# identifier, any license-integrity violation, or any gitleaks finding
# outside the documented baseline aborts the push.
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
PYTHON="python3"
command -v "$PYTHON" >/dev/null 2>&1 || PYTHON="python"
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

echo "==> gate 0: license integrity (identical bodies need a LICENSE or an alias entry)"
# Runs against the private tree before staging; set -e aborts the publish
# if check_license_integrity.py exits nonzero.
"$PYTHON" "$REPO_ROOT/scripts/check_license_integrity.py" "$REPO_ROOT"

echo "==> gate 1: redact map + blocked-identifier scan + new-file review"
# The known-files list is hash pinned: list_mirror_files.py emits
# path<TAB>sha256 per file from the mirror clone. The sanitizer grants
# baseline treatment for generic scans only when a snapshot file's bytes
# still hash to its pin; an edited known file is scanned as new.
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

# Tag state is reported truthfully: created and pushed, already on the
# mirror (left as is), or push failure (hard error). TAG_SUFFIX adds a
# step suffix, for example TAG_SUFFIX=step2b gives snapshot-2026-10-26-step2b.
TAG="snapshot-$(date -u +%Y-%m-%d)"
if [ -n "${TAG_SUFFIX:-}" ]; then
  TAG="$TAG-$TAG_SUFFIX"
fi
if git ls-remote --exit-code mirror "refs/tags/$TAG" >/dev/null 2>&1; then
  echo "==> tag $TAG already exists on the mirror, left as is"
else
  git tag "$TAG" pub
  if git push --quiet mirror "refs/tags/$TAG"; then
    echo "==> tagged: $TAG (created and pushed; consumers: pin a tag, never main)"
  else
    echo "ERROR: failed to push tag $TAG to the mirror" >&2
    exit 1
  fi
fi

echo "==> published: $MIRROR_URL"
