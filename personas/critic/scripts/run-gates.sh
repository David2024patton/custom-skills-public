#!/usr/bin/env bash
# PURPOSE: Run every applicable commit gate for the repo in the current
# directory: per-language lint + tests + debug check for each language
# detected, then the common secret scan and vulnerability scan.
# MODIFY PER PROJECT: none normally. If the repo has its own gate script
# (for example tools/check.sh), prefer that and use this as the fallback.
# A project may list extra language folders in .gates-extra, one per line.
# USAGE: run-gates.sh [--quick]   (--quick skips tests and the vulnerability scan)
# EXIT: 0 all gates green; 1 a gate failed; 2 a required tool is missing.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
QUICK=0; [ "${1:-}" = "--quick" ] && QUICK=1
fail=0
run() { echo "== $*"; "$@" || fail=1; }

# Language detection
if ls go.mod >/dev/null 2>&1; then
  run "$HERE/go/lint.sh"; run "$HERE/go/debug-check.sh"
  [ "$QUICK" = 0 ] && run "$HERE/go/test.sh"
fi
if ls Cargo.toml >/dev/null 2>&1; then
  run "$HERE/rust/lint.sh"; run "$HERE/rust/debug-check.sh"
  [ "$QUICK" = 0 ] && run "$HERE/rust/test.sh"
fi
if ls ./*.mojo >/dev/null 2>&1 || [ -f mojoproject.toml ]; then
  run "$HERE/mojo/lint.sh"; run "$HERE/mojo/debug-check.sh"
  [ "$QUICK" = 0 ] && run "$HERE/mojo/test.sh"
fi
if ls pubspec.yaml >/dev/null 2>&1; then
  run "$HERE/dart-flutter/lint.sh"; run "$HERE/dart-flutter/debug-check.sh"
  [ "$QUICK" = 0 ] && run "$HERE/dart-flutter/test.sh"
fi
if ls package.json >/dev/null 2>&1; then
  # Stack dispatch for Node projects. A project gets its most
  # specific applicable sets:
  #   1. Language set (exactly one): typescript/ when a tsconfig.json
  #      exists or typescript is a declared dependency; javascript/
  #      when package.json declares "type": "module" (plain ESM);
  #      otherwise the js-ts/ set is the generic fallback.
  #   2. Framework/schema sets, ALONGSIDE the language set: react/
  #      when react is a declared dependency; nextjs/ when a
  #      next.config.* file exists or next is a declared dependency;
  #      prisma/ when a Prisma schema exists (prisma/schema.prisma,
  #      schema.prisma, the prisma/schema/ folder, or prisma/*.prisma)
  #      or prisma/@prisma/client is a declared dependency.
  # No set fails a project for tooling the project does not declare.
  pkg_dep() { node -e "try{const p=require('./package.json');process.exit((p.dependencies&&p.dependencies['$1'])||(p.devDependencies&&p.devDependencies['$1'])?0:1)}catch(e){process.exit(1)}" 2>/dev/null; }
  pkg_esm() { node -e "try{process.exit(require('./package.json').type==='module'?0:1)}catch(e){process.exit(1)}" 2>/dev/null; }
  lang=""
  if [ -f tsconfig.json ] || pkg_dep typescript; then lang="typescript"
  elif pkg_esm; then lang="javascript"
  fi
  if [ -n "$lang" ]; then
    run "$HERE/$lang/lint.sh"; run "$HERE/$lang/debug-check.sh"
    [ "$QUICK" = 0 ] && run "$HERE/$lang/test.sh"
  else
    run "$HERE/js-ts/lint.sh"; run "$HERE/js-ts/debug-check.sh"
    [ "$QUICK" = 0 ] && run "$HERE/js-ts/test.sh"
  fi
  if pkg_dep react; then
    run "$HERE/react/lint.sh"; run "$HERE/react/debug-check.sh"
    [ "$QUICK" = 0 ] && run "$HERE/react/test.sh"
  fi
  if [ -f next.config.js ] || [ -f next.config.mjs ] || [ -f next.config.ts ] || [ -f next.config.cjs ] || pkg_dep next; then
    run "$HERE/nextjs/lint.sh"; run "$HERE/nextjs/debug-check.sh"
    [ "$QUICK" = 0 ] && run "$HERE/nextjs/test.sh"
  fi
  if [ -d prisma/schema ] || [ -f prisma/schema.prisma ] || [ -f schema.prisma ] || find prisma -maxdepth 1 -name '*.prisma' 2>/dev/null | grep -q . || pkg_dep prisma || pkg_dep @prisma/client; then
    run "$HERE/prisma/lint.sh"; run "$HERE/prisma/debug-check.sh"
    [ "$QUICK" = 0 ] && run "$HERE/prisma/test.sh"
  fi
fi
if ls pyproject.toml >/dev/null 2>&1 || ls requirements.txt >/dev/null 2>&1; then
  run "$HERE/python/lint.sh"; run "$HERE/python/debug-check.sh"
  [ "$QUICK" = 0 ] && run "$HERE/python/test.sh"
fi
if find . -name '*.sh' -not -path './node_modules/*' | grep -q .; then
  run "$HERE/shell/lint.sh"
fi
run "$HERE/common/secrets-scan.sh"
[ "$QUICK" = 0 ] && run "$HERE/common/vuln-scan.sh"
[ "$fail" = 0 ] && echo "GATES: ALL GREEN" || echo "GATES: RED"
exit "$fail"
