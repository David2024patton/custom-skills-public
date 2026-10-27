#!/usr/bin/env bash
# PURPOSE: Check that this Mojo tree HAS its debugging built in: a
# diagnostic seam exists (a diag module or an emit/logger call the
# refusals route through). Heuristic check, same as the rust and go
# versions: it reports what it found; a human or agent confirms the
# seam is real. Mojo also ships `mojo debug` (an LLDB debugger), but
# that is a tool you run, not a seam built into the module, so it
# does not satisfy this check on its own.
# MODIFY PER PROJECT: if the project names its seam differently, set
# DIAG_PATTERN in .gates-extra (one regex per line).
# USAGE: mojo/debug-check.sh [dir]
# EXIT: 0 a diagnostic seam was found; 1 none found.
set -u
cd "${1:-.}" || exit 2
pat='diag|Diag|emit\(|logger|Logger'
[ -f .gates-extra ] && pat="$pat|$(cat .gates-extra)"
if grep -rEq "$pat" --include='*.mojo' .; then
  echo "mojo debug check: diagnostic seam found"
  exit 0
fi
echo "mojo debug check: NO diagnostic seam found. Add one: run debug-add.sh" >&2
exit 1
