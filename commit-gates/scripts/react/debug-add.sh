#!/usr/bin/env bash
# PURPOSE: Print the standard React diagnostic pattern.
# STEPS:
#   1. Pick the pattern language from the target repo: diag.ts when
#      it is TypeScript (tsconfig or typescript dependency), else
#      diag.js.
#   2. Print the pattern: one diag module components emit through,
#      plus an error boundary at the app root whose
#      componentDidCatch forwards render errors into the same
#      channel and renders a fallback instead of a blank subtree.
#   3. The pattern's rule: every refusal path emits through diag
#      exactly once.
# MODIFY PER PROJECT: swap the sink inside the diag module (an
# error reporter the project declares), never at call sites.
# Never log secrets, tokens, or raw user content.
# USAGE: react/debug-add.sh [dir]
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
  // components/ErrorBoundary.tsx: a class component whose
  // componentDidCatch(error, info) calls
  // diag.emit('error', {error: String(error)}), and whose render
  // shows a fallback instead of a blank subtree.
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
  // components/ErrorBoundary.jsx: a class component whose
  // componentDidCatch(error, info) calls
  // diag.emit('error', {error: String(error)}), and whose render
  // shows a fallback instead of a blank subtree.
  Every refusal path calls diag.emit('refusal', {why}) exactly once.
EOF
fi
