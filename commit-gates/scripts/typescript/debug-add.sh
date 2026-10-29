#!/usr/bin/env bash
# PURPOSE: Print the standard TypeScript diagnostic pattern. The
# pattern file is diag.ts.
# STEPS:
#   1. Print the pattern: one typed lib/diag.ts logger module (a
#      tiny leveled logger, or pino in Node services that declare
#      it).
#   2. The pattern's rules: every refusal path emits through diag
#      exactly once with structured fields; global error handlers
#      forward into it.
# MODIFY PER PROJECT: swap the sink inside the diag module, never
# at call sites. Never log secrets or tokens.
# USAGE: typescript/debug-add.sh [dir]
# EXIT: 0.
set -u
cd "${1:-.}" 2>/dev/null || true
cat <<'EOF'
PATTERN:
  // lib/diag.ts
  export const diag = {
    refusals: 0,
    emit(event: string, fields: Record<string, unknown> = {}) {
      if (event === 'refusal') this.refusals++;
      console.info(JSON.stringify({ diag: event, ...fields }));
    },
  };
  Every refusal path calls diag.emit('refusal', {why}) exactly once.
  Global error handlers forward into diag.emit('error', ...).
EOF
