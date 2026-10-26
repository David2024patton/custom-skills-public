#!/usr/bin/env bash
# Rebuild the Hermes persona pipeline from this package on a fresh install.
#
#   bash bootstrap.sh <hermes_home> [workspace]
#
#   hermes_home : Hermes data root (e.g. ~/.hermes or C:/Users/<you>/AppData/Local/hermes)
#   workspace   : where scripts/knowledge/docs are staged, default ./_workspace
#
# What it recreates (v2, closing the 6-critic audit gaps):
#   1. skills -> EVERY profile listed under personas/ (canonical package copy overwrites;
#      profile-only skills are preserved because cp -r merges, it never deletes)
#   2. personas -> SOUL.md into each profile dir (creates missing profiles via the
#      hermes CLI when available)
#   3. heartbeat watchdog -> orchestrator scripts/ + the cron-job creation command
#   4. workspace staging: scripts/ (language QA packs + security/web instruments),
#      knowledge/ digests, QA-LOOP.md build law, IDEA.md
#   5. verification: run heartbeat.py and expect SILENCE (empty output = healthy)
#
# What it deliberately does NOT move: credentials (enter them per install), git history,
# and live session state.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
hermes_home="${1:?usage: bootstrap.sh <hermes_home> [workspace]}"
workspace="${2:-$here/_workspace}"

echo "== 1/5 skills -> every persona profile"
count=0
for soul_dir in "$here/personas"/*/; do
  name="$(basename "$soul_dir")"
  prof="$hermes_home/profiles/$name"
  if [ ! -d "$prof" ]; then
    if command -v hermes >/dev/null 2>&1; then
      echo "   creating profile $name"
      hermes profile create "$name" --clone-from orchestrator || true
    else
      echo "   SKIP $name: hermes CLI not on PATH (create it, then re-run)"
      continue
    fi
  fi
  mkdir -p "$prof/skills"
  # Newest copy wins: never clobber a profile file that is NEWER than the package.
  # (Profile-side skill_manage patches must flow back to the package, not die here.)
  (cd "$here/skills" && find . -type f | while read -r rel; do
     src="$here/skills/$rel"; dst="$prof/skills/$rel"
     if [ -f "$dst" ] && [ "$dst" -nt "$src" ]; then
       echo "   KEEP newer profile copy: $prof/skills/$rel (sync it back to the package)"
     else
       mkdir -p "$(dirname "$dst")"; cp "$src" "$dst"
     fi
   done)
  cp "$soul_dir/SOUL.md" "$prof/SOUL.md"
  count=$((count+1))
done
echo "   $count profiles seeded (newest copy wins; newer profile files kept and flagged for sync-back)"

echo "== 2/5 heartbeat watchdog"
orch="$hermes_home/profiles/orchestrator"
mkdir -p "$orch/scripts"
cp "$here/scripts/cron/heartbeat.py" "$orch/scripts/heartbeat.py"
echo "   installed $orch/scripts/heartbeat.py"
if command -v hermes >/dev/null 2>&1; then
  if grep -q "hourly-stuck-heartbeat" "$hermes_home/profiles/orchestrator/cron/jobs.json" 2>/dev/null; then
    echo "   cron job already present"
  else
    echo "   CREATE the cron job once (adjust flags to your hermes version):"
    echo "     hermes cron create --name hourly-stuck-heartbeat --every 1h \\"
    echo "       --script heartbeat.py --no-agent --deliver bot-chat:orchestrator"
    echo "   (no_agent = zero tokens; bot-chat deliver needs the Bot Chat opened once:"
    echo "    hermes chat -c 'Bot Chat' --create-if-missing)"
  fi
else
  echo "   hermes CLI not on PATH: create the cron job manually after install"
fi

echo "== 3/5 stage workspace at $workspace"
mkdir -p "$workspace"
cp -r "$here/scripts"   "$workspace/scripts"
cp -r "$here/knowledge" "$workspace/knowledge"
cp    "$here/QA-LOOP.md" "$workspace/QA-LOOP.md"
cp    "$here/IDEA.md"    "$workspace/IDEA.md"

echo "== 4/5 verify"
if command -v python3 >/dev/null 2>&1; then py=python3; else py=python; fi
if out="$("$py" "$orch/scripts/heartbeat.py" 2>&1)"; then
  if [ -z "$out" ]; then
    echo "   heartbeat: SILENT (fleet healthy) - PASS"
  else
    echo "   heartbeat reported (read it, then fix):"
    echo "$out" | sed 's/^/     /'
  fi
else
  echo "   heartbeat failed to run - fix python/path before trusting the install"
fi

echo "== 5/5 done. Remaining manual steps:"
cat <<'EOF'
   1. Read QA-LOOP.md as build law (critic checklist, fix loop, dispatch rules).
   2. Enter credentials per install - never copied by this script.
   3. Knowledge digests load per language (context/README.md); never load them all.
   4. Prove the pipeline before trusting it: run one Mode-A critic on a real file and
      one scripts/<lang>/qa.sh against known code; both must reproduce a known result.
   5. git history and live session state stay behind; this rebuilds structure only.
EOF
