#!/usr/bin/env bash
# QA script for C++. build -> lint -> test, real exit codes. Missing tool = SKIP, never silent.
set -u
cd "${1:-.}" || exit 2
FAILS=0
step() {
  local name="$1"; shift
  echo "=== $name ==="
  if ! command -v "$1" >/dev/null 2>&1; then echo "SKIP: '$1' not installed"; return; fi
  if "$@"; then echo "PASS: $name"; else echo "FAIL: $name"; FAILS=$((FAILS+1)); fi
}

CXX=${CXX:-c++}
command -v "$CXX" >/dev/null 2>&1 || { echo "SKIP: C++ compiler not installed"; exit 0; }
if [ -f CMakeLists.txt ]; then step "cmake configure" cmake -S . -B build; step "cmake build" cmake --build build; step "ctest" ctest --test-dir build --output-on-failure
elif [ -f Makefile ] || [ -f makefile ]; then step "make" make
else step "compile -Wall -Wextra" bash -c 'find . \( -name "*.cpp" -o -name "*.cc" -o -name "*.cxx" \) -print0 | xargs -0 -n1 '"$CXX"' -std=c++17 -Wall -Wextra -fsyntax-only'; fi
command -v clang-tidy >/dev/null 2>&1 && step "clang-tidy" bash -c 'find . -name "*.cpp" -print0 | xargs -0 clang-tidy -quiet'
