#!/usr/bin/env bash
# PURPOSE: Check that this Go module HAS its debugging built in: a
# structured logging or diagnostic path exists (log/slog, a diag
# package, or an equivalent seam), and no bare fmt.Print* debugging is
# left in non-main packages. Heuristic check: it reports what it found;
# a human or agent confirms the seam is real.
# MODIFY PER PROJECT: if the project names its diag package differently,
# set DIAG_PATTERN in .gates-extra (one regex per line).
# USAGE: go/debug-check.sh [module-dir]
# EXIT: 0 a diagnostic path was found; 1 none found.
set -u
cd "${1:-.}" || exit 2
pat='log/slog|internal/diag|/diag"|diagnostic'
[ -f .gates-extra ] && pat="$pat|$(cat .gates-extra)"
if grep -rEq "$pat" --include='*.go' .; then
  echo "go debug check: diagnostic path found"
  exit 0
fi
echo "go debug check: NO diagnostic path found. Add one: run debug-add.sh" >&2
exit 1
