#!/usr/bin/env bash
# PURPOSE: Check that this Rust tree HAS its debugging built in: a
# diagnostic seam exists (a diag module, defmt, tracing, or log usage)
# and kernel-style trees route refusals through it. Heuristic: reports
# what it found for a human or agent to confirm.
# MODIFY PER PROJECT: bare-metal projects name the seam in .gates-extra
# (one regex per line), for example itak_kernel::diag.
# USAGE: rust/debug-check.sh [dir]
# EXIT: 0 seam found; 1 none found.
set -u
cd "${1:-.}" || exit 2
pat='mod diag|diag::|defmt|tracing::|log::'
[ -f .gates-extra ] && pat="$pat|$(cat .gates-extra)"
if grep -rEq "$pat" --include='*.rs' .; then
  echo "rust debug check: diagnostic seam found"
  exit 0
fi
echo "rust debug check: NO diagnostic seam found. See debug-add.sh" >&2
exit 1
