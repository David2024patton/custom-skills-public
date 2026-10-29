#!/usr/bin/env bash
# PURPOSE: Prisma build-proof gate: client generation, then tests.
# STEPS:
#   1. Locate the Prisma CLI: node_modules/.bin/prisma first, else
#      a prisma binary on PATH; neither means exit 2.
#   2. Discover the schema exactly as the lint gate does (the
#      prisma/schema/ folder, prisma/schema.prisma, schema.prisma,
#      then prisma/*.prisma or ./*.prisma). None found: exit 2.
#   3. Supply dummy values for unset env("VAR") datasource names,
#      exactly as the lint gate does, for this process only.
#   4. Run `prisma generate --schema <schema>` for every schema.
#      Generate is the Prisma analogue of a compile step: it proves
#      the schema drives its generators. It NEVER connects to a
#      database; it writes only generated code, to the output the
#      schema's generator block declares (a project that wants gate
#      output kept apart points its generator output at a scratch
#      directory in the schema itself).
#   5. If generation passed and package.json defines a test script,
#      run `npm test`; no test script is stated, not hidden.
# PROHIBITION (every script in this set):
#   - NEVER prisma migrate (dev, deploy, reset, resolve, status).
#   - NEVER prisma db push, db pull, db execute, or db seed.
#   - NEVER prisma studio.
#   Nothing in this set touches a live database, ever.
# MODIFY PER PROJECT: nothing here; generator blocks and outputs
# live in the project's schema.
# USAGE: prisma/test.sh [dir]
# EXIT: 0 generate (and tests, when declared) pass; 1 generate or tests fail; 2 prisma CLI not installed or no schema found.
set -u
cd "${1:-.}" || exit 2
PRISMA_CMD=""
if [ -x node_modules/.bin/prisma ]; then PRISMA_CMD="./node_modules/.bin/prisma"
elif command -v prisma >/dev/null 2>&1; then PRISMA_CMD="prisma"
else echo "prisma CLI not installed (declare prisma as a devDependency and run npm install)" >&2; exit 2; fi
schemas=""
if [ -d prisma/schema ]; then schemas="prisma/schema"
elif [ -f prisma/schema.prisma ]; then schemas="prisma/schema.prisma"
elif [ -f schema.prisma ]; then schemas="schema.prisma"
else
  for f in prisma/*.prisma ./*.prisma; do [ -f "$f" ] && schemas="$schemas $f"; done
fi
# shellcheck disable=SC2086
set -- $schemas
[ "$#" = 0 ] && { echo "no Prisma schema found (prisma/schema.prisma, schema.prisma, or prisma/*.prisma)" >&2; exit 2; }
fail=0
for s in "$@"; do
  provider=""
  if [ -d "$s" ]; then provider="$(grep -rh -A4 'datasource' "$s" 2>/dev/null | grep -m1 'provider' | sed 's/.*=[[:space:]]*"\([^"]*\)".*/\1/')"
  else provider="$(grep -A4 'datasource' "$s" 2>/dev/null | grep -m1 'provider' | sed 's/.*=[[:space:]]*"\([^"]*\)".*/\1/')"; fi
  varnames=""
  if [ -d "$s" ]; then varnames="$(grep -rhoE 'env\("[A-Za-z_][A-Za-z0-9_]*"\)' "$s" 2>/dev/null | sed 's/env("//; s/")//' | sort -u)"
  else varnames="$(grep -oE 'env\("[A-Za-z_][A-Za-z0-9_]*"\)' "$s" 2>/dev/null | sed 's/env("//; s/")//' | sort -u)"; fi
  for v in $varnames; do
    if [ -z "${!v:-}" ]; then
      case "$provider" in
        sqlite) export "$v=file:./prisma-gate-scratch.db" ;;
        postgresql|postgres) export "$v=postgresql://gate:gate@localhost:5432/gate" ;;
        mysql) export "$v=mysql://gate:gate@localhost:3306/gate" ;;
        mongodb) export "$v=mongodb://localhost:27017/gate" ;;
        *) export "$v=file:./prisma-gate-scratch.db" ;;
      esac
      echo "note: $v unset; supplied a dummy $provider value for generate only (no connection is made)"
    fi
  done
  "$PRISMA_CMD" generate --schema "$s" || fail=1
done
if [ "$fail" = 0 ] && [ -f package.json ] && command -v npm >/dev/null 2>&1; then
  if node -e "process.exit(require('./package.json').scripts&&require('./package.json').scripts.test?0:1)" 2>/dev/null; then
    npm test || fail=1
  else
    echo "note: no test script in package.json; generate above is this gate's proof (stated, not hidden)"
  fi
fi
exit "$fail"
