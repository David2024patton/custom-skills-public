#!/usr/bin/env bash
# PURPOSE: Prisma lint gate: the schema is the code, so the checks
# are the Prisma CLI's own schema checks, run read-only.
# STEPS:
#   1. Locate the Prisma CLI: node_modules/.bin/prisma first, else
#      a prisma binary on PATH; neither means exit 2 (declare prisma
#      as a devDependency and run npm install).
#   2. Discover the schema, in order: the prisma/schema/ folder
#      (multi-file), prisma/schema.prisma, schema.prisma, then any
#      prisma/*.prisma or ./*.prisma file. None found: exit 2.
#   3. For each env("VAR") name the schema reads that is unset in
#      this environment, supply a provider-shaped dummy value (a
#      file: path for sqlite, a localhost URL otherwise) for this
#      gate's process only, and state that it did so. `prisma
#      validate` needs the variable present; it makes no connection.
#   4. Run `prisma format --check --schema <schema>`: the --check
#      flag is the CLI's documented CI mode and fails on unformatted
#      schema (plain `prisma format` rewrites in place; a gate never
#      rewrites).
#   5. Run `prisma validate --schema <schema>`: syntax, relations,
#      generator and datasource configuration.
# PROHIBITION (every script in this set):
#   - NEVER prisma migrate (dev, deploy, reset, resolve, status).
#   - NEVER prisma db push, db pull, db execute, or db seed.
#   - NEVER prisma studio.
#   Nothing in this set touches a live database, ever.
# MODIFY PER PROJECT: nothing here. Dummy env values live only
# inside this gate's process; never copy them into a real .env.
# USAGE: prisma/lint.sh [dir]
# EXIT: 0 schema formatted and valid; 1 findings; 2 prisma CLI not installed or no schema found.
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
  # Supply dummy values for env("VAR") names the schema reads, only when unset.
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
      echo "note: $v unset; supplied a dummy $provider value for validation only (no connection is made)"
    fi
  done
  "$PRISMA_CMD" format --check --schema "$s" || fail=1
  "$PRISMA_CMD" validate --schema "$s" || fail=1
done
exit "$fail"
