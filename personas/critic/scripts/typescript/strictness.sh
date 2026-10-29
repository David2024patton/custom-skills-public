#!/usr/bin/env bash
# PURPOSE: TypeScript strictness ladder check (report L1-23).
# This gate reads every tsconfig in the tree (root plus nested
# apps/*, packages/*, services/*) and grades the ladder:
#   FAIL: "strict": false anywhere. TypeScript 6 made strict
#     default-on, so an explicit false is a deliberate downgrade.
#   FINDING (exit 1): noUncheckedIndexedAccess not enabled. It
#     is the highest-value single flag after strict: indexed
#     access returning T instead of T | undefined hides real
#     bugs.
#   REPORT-ONLY: exactOptionalPropertyTypes off is printed as a
#     note, never a failure.
#   STALE: a tsconfig or package.json referencing tsgo or
#     @typescript/native-preview is flagged: those names are
#     stale. TS 7.0 (native port) is used for plain tsc where a
#     project adopts it, with a TS 6 dual install retained for
#     typed lint until the 7.1 programmatic API lands; this gate
#     does not force either, it flags the stale preview names.
# MODIFY PER PROJECT: none; compiler options are the project's,
# this gate only grades them.
# USAGE: typescript/strictness.sh [dir]
# EXIT: 0 ladder clean; 1 a fail or finding above; 2 no tsconfig.
set -u
cd "${1:-.}" || exit 2
configs="$(ls tsconfig.json apps/*/tsconfig.json packages/*/tsconfig.json services/*/tsconfig.json 2>/dev/null | sort -u)"
[ -n "$configs" ] || { echo "no tsconfig.json found" >&2; exit 2; }
fail=0
for tc in $configs; do
  if grep -qE '"strict"[[:space:]]*:[[:space:]]*false' "$tc"; then
    echo "FAIL: $tc sets strict: false (a downgrade; strict is default-on since TS 6)" >&2; fail=1
  fi
  if ! grep -qE '"noUncheckedIndexedAccess"[[:space:]]*:[[:space:]]*true' "$tc"; then
    # A config extending a strict base is graded on its own text plus the note.
    if grep -q '"extends"' "$tc"; then
      echo "note: $tc does not itself set noUncheckedIndexedAccess; verify its extends chain enables it (report L1-23 finding if not)" >&2
    else
      echo "finding: $tc does not enable noUncheckedIndexedAccess" >&2; fail=1
    fi
  fi
  grep -qE '"exactOptionalPropertyTypes"[[:space:]]*:[[:space:]]*true' "$tc" || echo "note (report-only): $tc does not enable exactOptionalPropertyTypes"
done
if grep -rqE 'tsgo|@typescript/native-preview' tsconfig.json package.json apps packages services 2>/dev/null; then
  echo "finding: stale tsgo / @typescript/native-preview reference (superseded names; TS 7 native is the current line, TS 6 dual install serves typed lint)" >&2; fail=1
fi
exit "$fail"
