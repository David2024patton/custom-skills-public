#!/usr/bin/env bash
# Regression test for the language QA packs under scripts/.
# Bug covered: every pack counted FAILS via step() but never exited with
# it, so a failing project still got exit 0 (Critic round 3, Critical 1).
# Assertions:
#   (a) static: each of the 12 packs contains a gate that exits 1 when
#       FAILS is greater than 0 and exits 0 otherwise.
#   (b) dynamic: the python pack exits nonzero and prints FAIL on a
#       syntax-broken .py file.
#   (c) dynamic: the python pack exits 0 on a clean .py file.
# USAGE: test_qa_packs.sh
# EXIT: 0 all assertions pass; 1 any assertion fails.
set -u
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FAILURES=0

pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAILURES=$((FAILURES+1)); }

# (a) Static gate check for all 12 packs.
LANGS="c cpp csharp flutter go java js mojo php python rust swift"
for lang in $LANGS; do
  pack="$SCRIPT_DIR/$lang/qa.sh"
  if [ ! -f "$pack" ]; then
    fail "static gate: $lang pack missing at $pack"
    continue
  fi
  if grep -Fq 'if [ "$FAILS" -gt 0 ]; then' "$pack" \
    && grep -Fq 'QA RESULT: FAIL' "$pack" \
    && grep -Fq 'exit 1' "$pack" \
    && grep -Fq 'QA RESULT: PASS' "$pack" \
    && grep -Fq 'exit 0' "$pack"; then
    pass "static gate: $lang pack exits 1 on nonzero FAILS and 0 on zero FAILS"
  else
    fail "static gate: $lang pack lacks the FAILS gate (nonzero FAILS must exit 1)"
  fi
done

# (b) and (c) Dynamic checks against the python pack.
PY_PACK="$SCRIPT_DIR/python/qa.sh"
TMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TMP_ROOT"' EXIT

BROKEN_DIR="$TMP_ROOT/broken"
mkdir -p "$BROKEN_DIR"
printf 'def broken(:\n    pass\n' > "$BROKEN_DIR/broken.py"
BROKEN_OUT="$(bash "$PY_PACK" "$BROKEN_DIR" 2>&1)"
BROKEN_CODE=$?
echo "$BROKEN_OUT"
if [ "$BROKEN_CODE" -ne 0 ]; then
  pass "dynamic broken python: exit code is nonzero (got $BROKEN_CODE)"
else
  fail "dynamic broken python: exit code is 0, expected nonzero"
fi
case "$BROKEN_OUT" in
  *FAIL*) pass "dynamic broken python: output contains FAIL" ;;
  *) fail "dynamic broken python: output does not contain FAIL" ;;
esac

CLEAN_DIR="$TMP_ROOT/clean"
mkdir -p "$CLEAN_DIR"
printf 'print("ok")\n' > "$CLEAN_DIR/clean.py"
CLEAN_OUT="$(bash "$PY_PACK" "$CLEAN_DIR" 2>&1)"
CLEAN_CODE=$?
echo "$CLEAN_OUT"
if [ "$CLEAN_CODE" -eq 0 ]; then
  pass "dynamic clean python: exit code is 0"
else
  fail "dynamic clean python: exit code is $CLEAN_CODE, expected 0"
fi

if [ "$FAILURES" -gt 0 ]; then
  echo "TEST RESULT: FAIL ($FAILURES failing assertion(s))"
  exit 1
fi
echo "TEST RESULT: PASS"
exit 0
