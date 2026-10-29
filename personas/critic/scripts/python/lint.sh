#!/usr/bin/env bash
# PURPOSE: Python lint and type gate (report L1-19).
# STEPS:
#   1. Ruff with an EXPLICIT select list, never the default floor
#      (defaults are only E4/E7/E9/F). The list: E,F,W,I,UP,B,SIM,
#      C4,RET,ARG,PTH,ERA,PL,RUF,S,TRY,EM,LOG,G (pycodestyle,
#      pyflakes, warnings, import order, pyupgrade, bugbear,
#      simplify, comprehensions, return style, unused args, path
#      handling, eradicate, pylint-lite, ruff rules, bandit-style
#      security S, tryceratops TRY, error messages EM, logging
#      LOG/G). A project pyproject may extend, never narrow, this
#      list through its own [tool.ruff] extend-select.
#      Ruff format check runs too. Ruff missing is exit 2: the
#      old pyflakes fallback is DELETED (lies-green register
#      #10); a weaker tool does not wear this gate's name.
#   2. Type gate, UNCONDITIONAL (the old "no config, no check"
#      shape was a design defect):
#      - Checker choice per repo: BasedPyright when the project
#        declares it (pyrightconfig.json or [tool.basedpyright]),
#        at typeCheckingMode recommended, ratcheting to strict;
#        otherwise mypy --strict where the project can bear it,
#        plain mypy otherwise.
#      - The chosen checker's binary missing is exit 2, stated:
#        TYPE CHECK DID NOT RUN. No config is required for the
#        gate to run; defaults apply.
#      - ty is advisory only (beta, pinned) when present: its
#        output prints, it never decides. Pyrefly is a watch
#        item, not run.
# MODIFY PER PROJECT: rule tuning lives in pyproject.toml, the
# checker choice in the project's own config, never here.
# USAGE: python/lint.sh [dir]
# EXIT: 0 clean; 1 findings; 2 ruff or the type checker missing.
set -u
cd "${1:-.}" || exit 2
command -v ruff >/dev/null 2>&1 || { echo "ruff not found; lint gate DID-NOT-RUN (no fallback; install ruff)" >&2; exit 2; }
fail=0
SELECT="E,F,W,I,UP,B,SIM,C4,RET,ARG,PTH,ERA,PL,RUF,S,TRY,EM,LOG,G"
ruff check --select "$SELECT" . || fail=1
ruff format --check . || fail=1
if [ -f pyrightconfig.json ] || grep -q '\[tool.basedpyright\]' pyproject.toml 2>/dev/null; then
  if command -v basedpyright >/dev/null 2>&1; then
    mode="recommended"
    grep -q 'typeCheckingMode[[:space:]]*=[[:space:]]*"strict"' pyproject.toml pyrightconfig.json 2>/dev/null && mode="strict"
    echo "type gate: basedpyright (mode $mode; recommended ratchets to strict)"
    basedpyright . || fail=1
  else
    echo "TYPE CHECK DID NOT RUN: project declares BasedPyright but the binary is not installed" >&2; exit 2
  fi
elif command -v mypy >/dev/null 2>&1; then
  if grep -q 'strict[[:space:]]*=[[:space:]]*true' pyproject.toml mypy.ini setup.cfg 2>/dev/null; then
    echo "type gate: mypy --strict (project declares strict)"
    mypy --strict . || fail=1
  else
    echo "type gate: mypy (unconditional; project has not declared strict)"
    mypy . || fail=1
  fi
elif command -v basedpyright >/dev/null 2>&1; then
  echo "type gate: basedpyright recommended (no mypy present)"
  basedpyright . || fail=1
else
  echo "TYPE CHECK DID NOT RUN: neither mypy nor basedpyright installed; the type gate is unconditional, so this is exit 2, not a skip" >&2
  exit 2
fi
if command -v ty >/dev/null 2>&1; then
  echo "advisory only (beta): ty check output follows; it never decides this gate"
  ty check . || echo "note: ty reported findings (advisory)"
fi
exit "$fail"
