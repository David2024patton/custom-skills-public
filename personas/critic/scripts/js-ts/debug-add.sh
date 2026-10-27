#!/usr/bin/env bash
# PURPOSE: Print the standard JS/TS diagnostic pattern: one logger
# module (pino in Node services, a tiny leveled logger in the browser
# or in plain ESM projects with no logger dependency), refusals and
# verdicts emitted through it with structured fields, and an error
# surface (window.onerror / process handlers) routed into it. The
# printed file name matches the target repo's language: diag.js for
# plain JavaScript repos (no tsconfig, no typescript dependency),
# diag.ts when the repo is TypeScript.
# MODIFY PER PROJECT: browser bundles and plain-JS repos use the
# tiny logger (no deps); Node services may use pino. Never log
# secrets or tokens.
# USAGE: js-ts/debug-add.sh [dir]
# EXIT: 0.
set -u
cd "${1:-.}" 2>/dev/null || true
ext=js
if [ -f tsconfig.json ] || node -e "const p=require('./package.json');process.exit((p.dependencies&&p.dependencies.typescript)||(p.devDependencies&&p.devDependencies.typescript)?0:1)" 2>/dev/null; then ext=ts; fi
if [ "$ext" = ts ]; then
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
else
cat <<'EOF'
PATTERN:
  // lib/diag.js
  export const diag = {
    refusals: 0,
    emit(event, fields = {}) {
      if (event === 'refusal') this.refusals++;
      console.info(JSON.stringify({ diag: event, ...fields }));
    },
  };
  Every refusal path calls diag.emit('refusal', {why}) exactly once.
  Global error handlers forward into diag.emit('error', ...).
EOF
fi
