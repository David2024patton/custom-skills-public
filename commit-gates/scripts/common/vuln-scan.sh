#!/usr/bin/env bash
# PURPOSE: Check dependencies against known vulnerabilities (osv.dev
# data). Runs osv-scanner when installed; otherwise falls back to the
# native tool per ecosystem present. A known-vulnerable dependency
# blocks the commit until upgraded or explicitly accepted by David.
# MODIFY PER PROJECT: none. Suppressions belong in the osv-scanner
# config in the repo, with a reason and a date, never here.
# USAGE: vuln-scan.sh
# EXIT: 0 no known vulns found by the tools that ran; 1 vulns found;
# 2 no scanner available (states so; does not pretend to have scanned).
set -u
ran=0; fail=0
if command -v osv-scanner >/dev/null 2>&1; then
  ran=1; osv-scanner -r . || fail=1
fi
if [ -f go.mod ] && command -v govulncheck >/dev/null 2>&1; then
  ran=1; govulncheck ./... || fail=1
fi
if [ -f Cargo.toml ] && command -v cargo-audit >/dev/null 2>&1; then
  ran=1; cargo audit || fail=1
fi
if [ -f package.json ] && command -v npm >/dev/null 2>&1; then
  ran=1; npm audit --audit-level=high || fail=1
fi
if [ "$ran" = 0 ]; then
  echo "NO VULN SCANNER AVAILABLE: nothing was scanned" >&2
  exit 2
fi
exit "$fail"
