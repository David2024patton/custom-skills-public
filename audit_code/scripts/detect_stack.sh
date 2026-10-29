#!/usr/bin/env bash
# Thin shim (I-02): stack detection lives in the critic manifest detector.
# Preserves the legacy interface: lines "STACK <name> <path>" and
# "TOOL <name> <ok|missing>"; exit 0 on success.
# === CRITIC SCRIPT MANIFEST ===
# question: Which stacks and tools are present (legacy audit interface)?
# stackDetection: delegates to personas/critic/scripts/stack-detect.py reading critic.manifest.json.
# inputs: [project_dir]
# effects: read-only
# exits: 0 ok; 2 detector or manifest missing
# output: summary line first, then STACK and TOOL lines
# === END MANIFEST ===
set -u
ROOT="${1:-.}"
HERE="$(cd "$(dirname "$0")" && pwd)"
DET=""
for cand in "$HERE/../../personas/critic/scripts/stack-detect.py" "$HERE/../personas/critic/scripts/stack-detect.py"; do
  [ -f "$cand" ] && DET="$cand" && break
done
if [ -z "$DET" ] || ! command -v python3 >/dev/null 2>&1; then
  echo "SUMMARY: manifest detector unavailable (DID-NOT-RUN)"
  exit 2
fi
exec python3 "$DET" --root "$ROOT" --format legacy-audit
