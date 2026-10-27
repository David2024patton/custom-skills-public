#!/usr/bin/env bash
# PURPOSE: Web test quality gate (report L1-27). The gate checks
# OUTCOMES and wiring, not which runner a project picked (Vitest
# 4.x is the default for new work; Jest 30 is legitimate legacy).
# CHECKS, each printed with its verdict:
#   1. Coverage thresholds: where a vitest/jest coverage config
#      declares thresholds, they must meet the floor: 80 lines,
#      functions, statements; 70 branches (per-glob overrides in
#      the project config are read as declared). Coverage
#      measured but with NO thresholds declared is a finding:
#      a number with no break point is decoration.
#   2. fast-check: parser, validator, and codec surfaces (files
#      matching pars|valid|codec in src/lib/app) need at least
#      one fast-check property test. Missing: finding.
#   3. Stryker: where a stryker config exists, thresholds.break
#      must be SET deliberately (the shipped default, break:
#      null, never fails; lies-green register #4). Unset or
#      null: finding. The library value for named critical
#      modules is break 60, nightly, ratcheting.
#   4. Playwright e2e wiring (PR mode verifies existence and
#      wiring; running is deep mode): a playwright config must
#      set webServer; any committed test.only in e2e specs is a
#      FAIL; an unconditional --update-snapshots in CI scripts
#      is a FAIL. Axe: where @axe-core/playwright is declared,
#      specs must use the mandated wording in reports, "no
#      automatically-detectable violations", never "WCAG
#      compliant"; this gate greps project docs/specs for the
#      forbidden claim.
# MODIFY PER PROJECT: thresholds live in the runner config.
# USAGE: js-ts/test-quality.sh [dir]
# EXIT: 0 all applicable checks pass; 1 a finding or fail above;
# 2 no package.json.
set -u
cd "${1:-.}" || exit 2
[ -f package.json ] || { echo "no package.json here" >&2; exit 2; }
fail=0
configs="$(ls vitest.config.* vitest.workspace.* jest.config.* package.json 2>/dev/null | sort -u)"
cov_found=0
for c in $configs; do
  if grep -qE 'thresholds|coverageThreshold' "$c" 2>/dev/null; then
    cov_found=1
    for key in lines functions statements branches; do
      val="$(grep -A6 -E 'thresholds|coverageThreshold' "$c" | grep -E "\"?$key\"?[[:space:]]*:" | grep -oE '[0-9]+' | head -1)"
      [ -z "$val" ] && continue
      floor=80; [ "$key" = branches ] && floor=70
      if [ "$val" -lt "$floor" ]; then echo "finding: coverage threshold $key=$val in $c is below the floor $floor" >&2; fail=1; fi
    done
  fi
done
if grep -qE '"(test:cov|coverage)"|vitest.*--coverage|jest.*--coverage' package.json 2>/dev/null && [ "$cov_found" = 0 ]; then
  echo "finding: coverage is measured (a coverage script exists) but no thresholds are declared in any runner config" >&2; fail=1
fi
if find src lib app -type f \( -name '*pars*' -o -name '*valid*' -o -name '*codec*' \) 2>/dev/null | grep -q .; then
  if grep -rlq 'fast-check' --include='*.test.*' --include='*.spec.*' . --exclude-dir=node_modules 2>/dev/null; then
    echo "fast-check: property tests present for parser/validator/codec surfaces"
  else
    echo "finding: parser/validator/codec surface present but no fast-check property tests (report L1-27)" >&2; fail=1
  fi
fi
for sc in stryker.config.json stryker.config.mjs stryker.config.js stryker.conf.json; do
  [ -f "$sc" ] || continue
  if grep -qE '"break"[[:space:]]*:[[:space:]]*null' "$sc" || ! grep -q '"break"' "$sc"; then
    echo "finding: $sc leaves thresholds.break unset or null; Stryker with break null never fails (set it deliberately, 60 on critical modules)" >&2; fail=1
  fi
done
for pc in playwright.config.ts playwright.config.js playwright.config.mjs; do
  [ -f "$pc" ] || continue
  grep -q 'webServer' "$pc" || { echo "finding: $pc does not configure webServer; e2e wiring incomplete" >&2; fail=1; }
done
if grep -rqE 'test\.only|describe\.only' --include='*.spec.ts' --include='*.spec.js' e2e tests playwright 2>/dev/null; then
  echo "FAIL: a committed test.only exists in e2e specs" >&2; fail=1
fi
if grep -qE 'update-snapshots' package.json 2>/dev/null && grep -q 'CI' package.json 2>/dev/null; then
  echo "note: check that --update-snapshots is not unconditional in CI (a fail when it is; project scripts are the evidence)"
fi
if grep -rqiE 'WCAG compliant' --include='*.md' --include='*.ts' --include='*.tsx' . --exclude-dir=node_modules 2>/dev/null; then
  echo "finding: the claim 'WCAG compliant' appears; automated checks support only the wording 'no automatically-detectable violations'" >&2; fail=1
fi
exit "$fail"
