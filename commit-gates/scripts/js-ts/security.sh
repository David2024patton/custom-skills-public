#!/usr/bin/env bash
# PURPOSE: Web SAST layer (report L1-27).
# STEPS:
#   1. Semgrep per-PR, BLOCKING on ERROR severity findings
#      (semgrep --error exits non-zero on findings at or above
#      the configured severity): configs p/javascript,
#      p/typescript, p/security-audit as available. Semgrep CE
#      is single-file depth; every run prints
#      sast_depth: single-file. The deep layer is CodeQL
#      security-extended, nightly, where the repo enables it;
#      this gate states that instead of implying whole-program
#      coverage.
#   2. eslint-plugin-security, where the project declares it,
#      is a FLOOR only: it is run through the project's lint,
#      never treated as the SAST verdict (in one independent
#      benchmark it found 0 of 6 SQL injections).
#   Semgrep missing: exit 2, stated. Behavioural advisories for
#   NEW dependencies (Socket-style) are Tier C signals: they are
#   printed by the dependency tooling, never block alone, and
#   are not run by this gate.
# MODIFY PER PROJECT: extra Semgrep configs live in the project
# (.semgrep.yml), never here.
# USAGE: js-ts/security.sh [dir]
# EXIT: 0 clean; 1 ERROR findings; 2 semgrep missing.
set -u
cd "${1:-.}" || exit 2
command -v semgrep >/dev/null 2>&1 || { echo "semgrep not found; web SAST DID-NOT-RUN" >&2; exit 2; }
echo "sast_depth: single-file (Semgrep CE); deep layer is CodeQL security-extended nightly where enabled"
semgrep --config p/javascript --config p/typescript --config p/security-audit --error --quiet . 
