#!/usr/bin/env bash
# PURPOSE: Print the standard JS/TS diagnostic pattern: one logger
# module (pino in Node services, a tiny leveled logger in the browser),
# refusals and verdicts emitted through it with structured fields, and
# an error surface (window.onerror / process handlers) routed into it.
# MODIFY PER PROJECT: browser bundles use the tiny logger (no deps);
# Node services may use pino. Never log secrets or tokens.
# USAGE: js-ts/debug-add.sh
# EXIT: 0.
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
