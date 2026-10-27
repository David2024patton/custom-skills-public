#!/usr/bin/env bash
# Regression test for scripts/security/secret-scan.sh.
# Bug covered: the scan wrapped both gitleaks and trufflehog in
# "|| true" and never propagated findings, so a reported leak still
# got exit 0 (Critic round 3, Critical 2).
# Cases:
#   1. a fake gitleaks that prints "leak found" and exits 1 must make
#      secret-scan.sh exit nonzero.
#   2. a fake gitleaks that exits 0 with no findings must make
#      secret-scan.sh exit 0.
# A clean trufflehog stub is installed alongside so the result is
# decided by the gitleaks stub alone, whatever the host has installed.
# USAGE: test_secret_scan.sh
# EXIT: 0 all assertions pass; 1 any assertion fails.
set -u
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCAN_SCRIPT="$SCRIPT_DIR/security/secret-scan.sh"
FAILURES=0

pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAILURES=$((FAILURES+1)); }

TMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TMP_ROOT"' EXIT
STUB_BIN="$TMP_ROOT/bin"
WORK_DIR="$TMP_ROOT/work"
mkdir -p "$STUB_BIN" "$WORK_DIR"

# Clean second engine stub: no findings, exit 0.
cat > "$STUB_BIN/trufflehog" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
chmod +x "$STUB_BIN/trufflehog"

# Case 1: gitleaks reports a leak and exits 1.
cat > "$STUB_BIN/gitleaks" <<'EOF'
#!/usr/bin/env bash
echo "leak found"
exit 1
EOF
chmod +x "$STUB_BIN/gitleaks"

LEAK_OUT="$(PATH="$STUB_BIN:$PATH" bash "$SCAN_SCRIPT" "$WORK_DIR" 2>&1)"
LEAK_CODE=$?
echo "$LEAK_OUT"
if [ "$LEAK_CODE" -ne 0 ]; then
  pass "leak case: secret-scan exit code is nonzero (got $LEAK_CODE)"
else
  fail "leak case: secret-scan exit code is 0, expected nonzero on findings"
fi
case "$LEAK_OUT" in
  *"leak found"*) pass "leak case: scanner output is shown" ;;
  *) fail "leak case: scanner output missing from scan output" ;;
esac

# Case 2: gitleaks runs clean and exits 0.
cat > "$STUB_BIN/gitleaks" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
chmod +x "$STUB_BIN/gitleaks"

CLEAN_OUT="$(PATH="$STUB_BIN:$PATH" bash "$SCAN_SCRIPT" "$WORK_DIR" 2>&1)"
CLEAN_CODE=$?
echo "$CLEAN_OUT"
if [ "$CLEAN_CODE" -eq 0 ]; then
  pass "clean case: secret-scan exit code is 0"
else
  fail "clean case: secret-scan exit code is $CLEAN_CODE, expected 0"
fi

if [ "$FAILURES" -gt 0 ]; then
  echo "TEST RESULT: FAIL ($FAILURES failing assertion(s))"
  exit 1
fi
echo "TEST RESULT: PASS"
exit 0
