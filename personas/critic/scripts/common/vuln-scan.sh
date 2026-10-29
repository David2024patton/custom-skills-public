#!/usr/bin/env bash
# PURPOSE: Check dependencies against known vulnerabilities (osv.dev
# data). Runs osv-scanner when installed; otherwise falls back to the
# native tool per ecosystem present. A known-vulnerable dependency
# blocks the commit until upgraded or explicitly accepted.
# MODIFY PER PROJECT: none. Suppressions belong in the scanner
# config in the repo, with a reason and a date, never here.
# LIES-GREEN NOTES (report L1-01, L1-08, L1-28):
# - govulncheck: the VERDICT comes from a TEXT mode run, because
#   its JSON, SARIF, and OpenVEX modes always exit 0. A second,
#   JSON mode run writes an artefact (govulncheck.json in the
#   current directory); its exit code is IGNORED on purpose and
#   the JSON is parsed for findings whose "affects" list is
#   non-empty. Go findings are deduplicated by GO-ID against the
#   osv-scanner output note (osv-scanner covers non-Go assets).
# - cargo audit runs with --deny warnings: without an explicit
#   --deny, cargo audit's warning classes (unmaintained, yanked,
#   unsound notices) do not fail the run.
# USAGE: vuln-scan.sh
# EXIT: 0 no known vulns found by the tools that ran; 1 vulns found;
# 2 no scanner available (states so; does not pretend to have scanned).
set -u
ran=0; fail=0
if command -v osv-scanner >/dev/null 2>&1; then
  ran=1; osv-scanner -r . || fail=1
fi
if [ -f go.mod ] && command -v govulncheck >/dev/null 2>&1; then
  ran=1
  govulncheck ./... || fail=1
  # Artefact run: exit code ignored BY DESIGN (JSON mode always
  # exits 0); findings are parsed, never trusted from the exit.
  govulncheck -format json ./... > govulncheck.json 2>/dev/null || true
  if command -v python3 >/dev/null 2>&1; then
    python3 - <<'PYEOF' || fail=1
import json, sys
# govulncheck -format json emits a stream of pretty-printed JSON
# objects (config, SBOM, progress, osv, finding), not JSON lines.
found = {}
try:
    text = open("govulncheck.json").read()
except FileNotFoundError:
    sys.exit(0)
dec = json.JSONDecoder()
idx = 0
while idx < len(text):
    while idx < len(text) and text[idx] not in "{":
        idx += 1
    if idx >= len(text):
        break
    try:
        obj, end = dec.raw_decode(text, idx)
    except json.JSONDecodeError:
        idx += 1
        continue
    idx = end
    f = obj.get("finding")
    if f and f.get("osv"):
        # A finding counts as reachable when its trace reaches a
        # called function (a frame carrying a function name), which
        # is govulncheck's symbol-level result.
        if any(t.get("function") for t in f.get("trace", [])):
            found[f["osv"]] = f
if found:
    print("govulncheck JSON artefact: reachable findings: " + ", ".join(sorted(found)))
    sys.exit(1)
print("govulncheck JSON artefact: no reachable findings parsed")
PYEOF
  else
    echo "note: python3 missing; govulncheck JSON artefact written but not parsed (text verdict above still gates)"
  fi
fi
if [ -f Cargo.toml ] && command -v cargo-audit >/dev/null 2>&1; then
  ran=1; cargo audit --deny warnings || fail=1
fi
if [ -f package.json ] && command -v npm >/dev/null 2>&1; then
  ran=1; npm audit --audit-level=high || fail=1
fi
if [ "$ran" = 0 ]; then
  echo "NO VULN SCANNER AVAILABLE: nothing was scanned" >&2
  exit 2
fi
exit "$fail"
