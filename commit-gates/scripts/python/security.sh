#!/usr/bin/env bash
# PURPOSE: Python security layer (report L1-18). This is the
# largest single hole the research found: the Python set had NO
# dependency vulnerability scan and NO SAST at all.
# STEPS:
#   1. pip-audit (PyPA, PyPI Advisory Database by default;
#      PIP_AUDIT_SOURCE=osv switches to -s osv). uv projects:
#      the lock is exported first (uv export) or the project
#      runs `uv audit --locked` itself; when uv.lock exists and
#      uv is installed, this gate runs uv audit --locked as the
#      dependency half and says so.
#   2. osv-scanner over the lock/requirements, for non-PyPI and
#      cross-ecosystem assets, where a lockfile exists.
#   3. SAST: Bandit at medium severity and confidence
#      (bandit -r -ll -ii on the source dirs), plus Semgrep
#      with --config p/python --config p/bandit, blocking on
#      ERROR findings. Semgrep CE is single-file depth; the
#      header of every run prints sast_depth: single-file.
#      CodeQL Python is the weekly deep layer where available;
#      it is not this per-commit gate.
#   `safety` is an optional Tier C supplement only, never the
#   foundation, and this gate never calls it.
# EXIT LAW: pip-audit and Bandit are the foundation; either one
# missing is exit 2 for this gate (DID-NOT-RUN, stated), never
# a partial pass wearing the full name. Semgrep missing is
# stated and also exit 2: the SAST half is two tools by spec.
# MODIFY PER PROJECT: Bandit skips and Semgrep ignores live in
# project config with reasons, never in this script.
# USAGE: python/security.sh [dir]
# EXIT: 0 clean; 1 findings; 2 a foundation tool missing.
set -u
cd "${1:-.}" || exit 2
echo "sast_depth: single-file (Semgrep CE); deep cross-file is the nightly CodeQL layer"
missing=0
command -v pip-audit >/dev/null 2>&1 || { echo "pip-audit not found; dependency scan DID-NOT-RUN" >&2; missing=1; }
command -v bandit >/dev/null 2>&1 || { echo "bandit not found; SAST half DID-NOT-RUN" >&2; missing=1; }
command -v semgrep >/dev/null 2>&1 || { echo "semgrep not found; SAST half DID-NOT-RUN" >&2; missing=1; }
[ "$missing" = 1 ] && exit 2
fail=0
if [ -f uv.lock ] && command -v uv >/dev/null 2>&1; then
  echo "uv project: uv audit --locked"
  uv audit --locked || fail=1
else
  if [ "${PIP_AUDIT_SOURCE:-pypi}" = osv ]; then pip-audit -s osv || fail=1
  else pip-audit || fail=1; fi
fi
if command -v osv-scanner >/dev/null 2>&1; then
  for lock in requirements.txt uv.lock poetry.lock Pipfile.lock pyproject.toml; do
    [ -f "$lock" ] && { osv-scanner --lockfile "$lock" || fail=1; break; }
  done
else
  echo "note: osv-scanner not installed; cross-ecosystem half skipped (stated; pip-audit above is the PyPI layer)"
fi
SRC="."
[ -d src ] && SRC="src"
bandit -r -ll -ii "$SRC" || fail=1
semgrep --config p/python --config p/bandit --error --quiet . || fail=1
exit "$fail"
