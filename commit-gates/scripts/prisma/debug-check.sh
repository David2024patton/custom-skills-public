#!/usr/bin/env bash
# PURPOSE: Prisma debug check, at the level a schema honestly has
# one. A schema has no runtime diagnostic seam, so there is no
# seam-presence analogue; the closest real checks are these
# schema-level diagnostics.
# STEPS:
#   1. Discover schema files exactly as the lint gate does.
#      None found: exit 2.
#   2. A generator block exists (the client can be generated and
#      its query/error logging wired; see debug-add.sh).
#   3. A datasource block exists.
#   4. At least one model exists.
#   5. Every model carries an @id or @@id (a model with no id is
#      the schema smell that surfaces later as a runtime mystery).
#   6. No datasource url is a literal carrying credentials
#      (user:password@host inside the schema file). Datasource urls
#      belong in env("..."), so a committed schema never carries a
#      live credential.
# NOTES:
#   - `prisma debug` prints CLI environment info for bug reports.
#     Like `mojo debug` in the mojo set, it is a tool you run, not a
#     seam built into the project, so it does not satisfy this check.
#   - This script only READs schema files.
# PROHIBITION (every script in this set): no migrate, no db push,
# pull, execute, or seed, no studio. Nothing touches a live
# database, ever.
# MODIFY PER PROJECT: a model that legitimately has no id (a pure
# join table keyed by @@unique) is recorded in the repo RULES page
# and this check is adjusted there, not silently skipped.
# USAGE: prisma/debug-check.sh [dir]
# EXIT: 0 schema-level diagnostics clean; 1 findings; 2 no schema found.
set -u
cd "${1:-.}" || exit 2
files=""
if [ -d prisma/schema ]; then files="$(find prisma/schema -name '*.prisma' | sort)"
elif [ -f prisma/schema.prisma ]; then files="prisma/schema.prisma"
elif [ -f schema.prisma ]; then files="schema.prisma"
else
  for f in prisma/*.prisma ./*.prisma; do [ -f "$f" ] && files="$files $f"; done
fi
# shellcheck disable=SC2086
set -- $files
[ "$#" = 0 ] && { echo "no Prisma schema found (prisma/schema.prisma, schema.prisma, or prisma/*.prisma)" >&2; exit 2; }
fail=0
# shellcheck disable=SC2086
grep -q 'generator ' "$@" 2>/dev/null || { echo "no generator block in schema (add one: see debug-add.sh)" >&2; fail=1; }
# shellcheck disable=SC2086
grep -q 'datasource ' "$@" 2>/dev/null || { echo "no datasource block in schema" >&2; fail=1; }
# shellcheck disable=SC2086
grep -q '^model ' "$@" 2>/dev/null || { echo "no model in schema" >&2; fail=1; }
# shellcheck disable=SC2086
cred="$(grep -nE 'url[[:space:]]*=[[:space:]]*"[a-z]+://[^"/]*:[^"@/]*@' "$@" 2>/dev/null || true)"
[ -n "$cred" ] && { echo "datasource url carries literal credentials (move it to env(...)): $cred" >&2; fail=1; }
# shellcheck disable=SC2086
noid="$(awk '/^model [A-Za-z_]+ \{/{name=$2; has=0; inblock=1; next} inblock && /@id|@@id/{has=1} inblock && /^\}/{if(!has) print FILENAME": model " name " has no @id or @@id"; inblock=0}' "$@")"
[ -n "$noid" ] && { echo "$noid" >&2; fail=1; }
[ "$fail" = 0 ] && echo "prisma debug check: schema-level diagnostics clean (generator, datasource, models with ids, no literal credentials)"
exit "$fail"
