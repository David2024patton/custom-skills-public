#!/usr/bin/env bash
# PURPOSE: React component test quality gate (report L1-24).
# CHECKS:
#   1. Enzyme present in dependencies is a FAIL: it is a dead
#      testing era and cannot test current React honestly.
#   2. Testing Library query priority, statically graded: in
#      component test files, count priority queries (getByRole,
#      getByLabelText, getByPlaceholderText, getByText,
#      getByDisplayValue) against getByTestId / queryByTestId.
#      A testId ratio above 0.5 is a MAJOR finding (exit 1):
#      tests coupled to test ids instead of what a user sees.
#      Playwright component tests are an accepted equivalent:
#      where the project runs them, this grading states that
#      and passes the grading half.
#   3. React Compiler-era lint: covered in react/lint.sh (the
#      react-hooks v7 recommended set gates as errors).
# MODIFY PER PROJECT: none.
# USAGE: react/test-quality.sh [dir]
# EXIT: 0 graded clean; 1 Enzyme present or testId ratio above
# 0.5; 2 not a React project or no component tests to grade
# (stated).
set -u
cd "${1:-.}" || exit 2
[ -f package.json ] || { echo "no package.json here" >&2; exit 2; }
has_dep() { node -e "const p=require('./package.json');process.exit((p.dependencies&&p.dependencies['$1'])||(p.devDependencies&&p.devDependencies['$1'])?0:1)" 2>/dev/null; }
has_dep react || { echo "not a React project" >&2; exit 2; }
fail=0
if has_dep enzyme || has_dep enzyme-adapter-react-16 || has_dep @wojtekmaj/enzyme-adapter-react-17; then
  echo "FAIL: Enzyme is present in dependencies (report L1-24)" >&2; fail=1
fi
testfiles="$(grep -rlE '@testing-library/react|testing-library' --include='*.test.*' --include='*.spec.*' . --exclude-dir=node_modules 2>/dev/null | sort)"
if [ -z "$testfiles" ]; then
  if ls playwright.config.* >/dev/null 2>&1 && grep -rlq 'toHaveScreenshot\|@playwright/test' --include='*.spec.*' . --exclude-dir=node_modules 2>/dev/null; then
    echo "component tests run as Playwright component tests (accepted equivalent); Testing Library grading not applicable (stated)"
    exit "$fail"
  fi
  echo "no Testing Library component tests found to grade (stated)" >&2
  [ "$fail" = 0 ] && exit 2
  exit "$fail"
fi
prio=0; tid=0
for f in $testfiles; do
  p="$(grep -oE 'getByRole|getByLabelText|getByPlaceholderText|getByText|getByDisplayValue' "$f" | wc -l)"; prio=$((prio+p))
  t="$(grep -oE 'getByTestId|queryByTestId|findByTestId' "$f" | wc -l)"; tid=$((tid+t))
done
total=$((prio+tid))
echo "testing library queries: priority $prio, testId $tid"
if [ "$total" -gt 0 ]; then
  python3 -c "
import sys
prio, tid = $prio, $tid
ratio = tid / (prio + tid)
print(f'testId ratio: {ratio:.2f}')
sys.exit(1 if ratio > 0.5 else 0)" || { echo "MAJOR finding: testId ratio above 0.5; tests are coupled to test ids instead of accessible queries" >&2; fail=1; }
fi
exit "$fail"
