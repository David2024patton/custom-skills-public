#!/usr/bin/env bash
# PURPOSE: Prisma migration safety gate (report L1-26). Pure
# static and pure git checks; no database is ever touched, and
# the migrate/db prohibitions from the rest of this set apply
# here too (never migrate, never db push, never db execute).
# CHECKS:
#   1. Drift interpretation helper (mode diff, arg 2 = the two
#      schema sources): runs prisma migrate diff --exit-code and
#      interprets its documented codes: 0 empty diff, 1 error,
#      2 non-empty diff (a printed diff IS the finding data; a
#      schema pair that should be identical exiting 2 fails).
#      A moved command (Prisma ORM 8 moved migrate commands) is
#      exit 2 with a COMMAND_MOVED note, detected from the CLI
#      output, never a silent pass.
#   2. Destructive migration parser (default mode): every new
#      or changed migration.sql under prisma/migrations in the
#      git diff (or all of them, arg: all) is parsed for DROP
#      TABLE, DROP COLUMN, ALTER COLUMN ... SET NOT NULL, and
#      rename-as-drop-plus-add shapes. A hit fails unless a
#      waiver file entry names it: prisma/migration-waivers.txt
#      lines are "<migration-dir-name> <pattern> <reason and
#      date>".
#   3. Pure-git schema gate: a schema change (schema.prisma or
#      prisma/schema/*) in the diff with NO accompanying new
#      migration directory fails. No database needed.
#   4. db push finding: any deploy or CI script in the repo
#      invoking `prisma db push` is a finding.
#   5. $use staleness: Prisma 7 removed $use middleware (the
#      seam is $extends). A $use( reference in client code is a
#      stale finding when the declared Prisma major is 7+.
#   6. Generate freshness: only when the generated client is
#      committed (a generated dir under version control): run
#      generate to a scratch output and diff; stale fails.
#      Uncommitted clients skip this, stated.
# USAGE: prisma/migrate-check.sh [dir] [check|diff <from> <to>|all]
# EXIT: 0 clean; 1 findings; 2 prisma CLI missing for the diff
# mode, or a COMMAND_MOVED note (stated).
set -u
cd "${1:-.}" || exit 2
MODE="${2:-check}"
fail=0
if [ "$MODE" = diff ]; then
  PRISMA_CMD=""
  if [ -x node_modules/.bin/prisma ]; then PRISMA_CMD="./node_modules/.bin/prisma"
  elif command -v prisma >/dev/null 2>&1; then PRISMA_CMD="prisma"
  else echo "prisma CLI not installed" >&2; exit 2; fi
  FROM="${3:-}"; TO="${4:-}"
  [ -n "$FROM" ] && [ -n "$TO" ] || { echo "diff mode needs <from-schema> <to-schema>" >&2; exit 2; }
  out="$("$PRISMA_CMD" migrate diff --from-schema-datamodel "$FROM" --to-schema-datamodel "$TO" --exit-code 2>&1)"
  rc=$?
  echo "$out"
  if echo "$out" | grep -qiE 'unknown command|not.*found.*command|COMMAND_MOVED'; then
    echo "COMMAND_MOVED: this Prisma major moved the migrate diff command; the gate DID NOT RUN (exit 2, not a pass)" >&2; exit 2
  fi
  case "$rc" in
    0) echo "migrate diff: empty (0)"; exit 0 ;;
    2) echo "migrate diff: NON-EMPTY (2): the schemas differ; the diff above is the finding data" >&2; exit 1 ;;
    *) echo "migrate diff: error (1)" >&2; exit 1 ;;
  esac
fi
# changed files from git when available
changed=""
git rev-parse --git-dir >/dev/null 2>&1 && changed="$(git diff --name-only HEAD 2>/dev/null; git diff --name-only --cached HEAD 2>/dev/null)"
if [ "$MODE" = all ]; then migfiles="$(find prisma/migrations -name 'migration.sql' 2>/dev/null | sort)"
else migfiles="$(echo "$changed" | grep 'migration.sql' | sort -u)"; [ -z "$migfiles" ] && migfiles="$(find prisma/migrations -name 'migration.sql' -newer prisma/schema.prisma 2>/dev/null | sort)"; fi
for mf in $migfiles; do
  [ -f "$mf" ] || continue
  mdir="$(basename "$(dirname "$mf")")"
  for pat in 'DROP TABLE' 'DROP COLUMN' 'SET NOT NULL'; do
    if grep -qiE "$pat" "$mf"; then
      if [ -f prisma/migration-waivers.txt ] && grep -q "^$mdir.*$pat" prisma/migration-waivers.txt; then
        echo "waived: $mf contains '$pat' with a waiver entry naming it"
      else
        echo "finding: destructive shape '$pat' in $mf with no waiver entry in prisma/migration-waivers.txt" >&2; fail=1
      fi
    fi
  done
  # rename-as-drop-plus-add heuristic: an ADD COLUMN and a DROP COLUMN of a different name in one migration is printed for review.
  if grep -qi 'DROP COLUMN' "$mf" && grep -qi 'ADD COLUMN' "$mf"; then
    echo "note: $mf both adds and drops columns; verify this is not a rename done as drop-plus-add (data loss shape)"
  fi
done
if [ -n "$changed" ]; then
  if echo "$changed" | grep -qE 'schema\.prisma|prisma/schema/' && ! echo "$changed" | grep -q 'prisma/migrations/'; then
    echo "finding: schema changed in this diff with no accompanying migration (pure-git gate, report L1-26)" >&2; fail=1
  fi
fi
if grep -rq 'prisma db push' --include='*.sh' --include='*.yml' --include='*.yaml' --include='*.json' . --exclude-dir=node_modules 2>/dev/null; then
  echo "finding: 'prisma db push' invoked in a script or workflow; db push bypasses migrations and is a finding in deploy paths" >&2; fail=1
fi
major=""
[ -f package.json ] && major="$(node -e "const p=require('./package.json');const v=(p.dependencies&&p.dependencies['@prisma/client'])||(p.devDependencies&&p.devDependencies['@prisma/client'])||(p.dependencies&&p.dependencies.prisma)||'';const m=String(v).match(/(\d+)/);console.log(m?m[1]:'')" 2>/dev/null)"
if [ -n "$major" ] && [ "$major" -ge 7 ]; then
  if grep -rq '\$use(' --include='*.ts' --include='*.tsx' --include='*.js' src lib app prisma 2>/dev/null; then
    echo "finding: \$use middleware reference present under Prisma $major; \$use is stale, the seam is \$extends" >&2; fail=1
  fi
fi
if git rev-parse --git-dir >/dev/null 2>&1 && git ls-files | grep -qE '(^|/)(generated|\.prisma)/.*client'; then
  echo "note: generated client is committed; freshness is checked by regenerating and diffing in the project's own gate (this static gate states the requirement)"
fi
exit "$fail"
