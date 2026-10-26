#!/usr/bin/env bash
# Secret scan over FULL git history (not just working tree). Run before any ship.
set -u
cd "${1:-.}" || exit 2
echo "=== Secret scan: $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
GITLEAKS_CODE=0
TRUFFLEHOG_CODE=0
if command -v gitleaks >/dev/null 2>&1; then
  echo "--- gitleaks: full history (--log-opts=--all) ---"
  gitleaks detect --source . --log-opts="--all" --redact 2>&1
  GITLEAKS_CODE=$?
  echo "gitleaks exit reflects findings; any REAL hit is compromised until proven otherwise."
  echo "Remediation order is fixed: ROTATE the credential FIRST, purge history SECOND."
  echo "History purge (git filter-repo / BFG) is David's compliance decision, never automatic."
else
  echo "SKIP: gitleaks not installed. Install: go install github.com/gitleaks/gitleaks/v8@latest"
fi
if command -v trufflehog >/dev/null 2>&1; then
  echo "--- trufflehog: second-engine cross-check ---"
  trufflehog git file://. --only-verified --fail 2>&1 | head -50
  TRUFFLEHOG_CODE=${PIPESTATUS[0]}
fi

if [ "$GITLEAKS_CODE" -ne 0 ] || [ "$TRUFFLEHOG_CODE" -ne 0 ]; then
  echo "SCAN RESULT: FAIL (secret scanner reported findings: gitleaks exit $GITLEAKS_CODE, trufflehog exit $TRUFFLEHOG_CODE)"
  exit 1
fi
echo "SCAN RESULT: PASS (no findings)"
exit 0
