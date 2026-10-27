#!/usr/bin/env bash
# PURPOSE: Print the standard Next.js diagnostic pattern.
# STEPS:
#   1. Pick the pattern language from the target repo: .ts files
#      when it is TypeScript (tsconfig or typescript dependency),
#      else .js.
#   2. Print the pattern: one lib/diag module server and client
#      code emit through; the framework error surfaces (app/error
#      and app/global-error boundaries) forwarding render errors
#      into that same channel with a fallback UI and reset, never a
#      silent blank page.
#   3. The pattern's rule: every refusal path emits through diag
#      exactly once, with structured fields.
# MODIFY PER PROJECT: swap the sink inside the diag module (an
# error reporter the project declares), never at call sites.
# Never log secrets, tokens, or raw user content.
# USAGE: nextjs/debug-add.sh [dir]
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
  // app/error.tsx ('use client'): the boundary component calls
  // diag.emit('error', {error: String(error)}) in an effect and
  // renders a fallback with a reset button, never a blank page.
  // app/global-error.tsx does the same for root-layout failures.
  Every refusal path calls diag.emit('refusal', {why}) exactly once.
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
  // app/error.js ('use client'): the boundary component calls
  // diag.emit('error', {error: String(error)}) in an effect and
  // renders a fallback with a reset button, never a blank page.
  // app/global-error.js does the same for root-layout failures.
  Every refusal path calls diag.emit('refusal', {why}) exactly once.
EOF
fi
