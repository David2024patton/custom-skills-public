#!/usr/bin/env bash
# PURPOSE: Print the standard plain-JavaScript (ESM) diagnostic
# pattern. The pattern file is diag.js, always: this set has no
# TypeScript variant (TypeScript projects use the typescript set).
# STEPS:
#   1. Print the pattern: one lib/diag.js logger module (a tiny
#      leveled logger, or pino in Node services that declare it).
#   2. The pattern's rules: every refusal path emits through diag
#      exactly once with structured fields; process
#      uncaughtException/unhandledRejection handlers forward into it.
# MODIFY PER PROJECT: swap the sink inside the diag module (pino),
# never at call sites. Never log secrets or tokens.
# USAGE: javascript/debug-add.sh [dir]
# EXIT: 0.
set -u
cd "${1:-.}" 2>/dev/null || true
cat <<'EOF'
PATTERN:
  // lib/diag.js  (ESM)
  export const diag = {
    refusals: 0,
    emit(event, fields = {}) {
      if (event === 'refusal') this.refusals++;
      console.info(JSON.stringify({ diag: event, ...fields }));
    },
  };
  Every refusal path calls diag.emit('refusal', {why}) exactly once.
  process.on('uncaughtException') and 'unhandledRejection' forward
  into diag.emit('error', ...).
EOF
