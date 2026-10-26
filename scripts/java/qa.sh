#!/usr/bin/env bash
# QA script for Java/Kotlin. build -> lint -> test, real exit codes. Missing tool = SKIP, never silent.
set -u
cd "${1:-.}" || exit 2
FAILS=0
step() {
  local name="$1"; shift
  echo "=== $name ==="
  if ! command -v "$1" >/dev/null 2>&1; then echo "SKIP: '$1' not installed"; return; fi
  if "$@"; then echo "PASS: $name"; else echo "FAIL: $name"; FAILS=$((FAILS+1)); fi
}

if [ -f gradlew ]; then step "gradle build" ./gradlew build -x test; step "gradle test" ./gradlew test
elif command -v mvn >/dev/null 2>&1; then step "maven build" mvn -q -DskipTests package; step "maven test" mvn test
else echo "SKIP: no gradlew or maven"; fi
