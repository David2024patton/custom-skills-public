#!/usr/bin/env bash
# QA script for PHP / Laravel. build -> lint -> test, real exit codes. Missing tool = SKIP, never silent.
set -u
cd "${1:-.}" || exit 2
FAILS=0
step() {
  local name="$1"; shift
  echo "=== $name ==="
  if ! command -v "$1" >/dev/null 2>&1; then echo "SKIP: '$1' not installed"; return; fi
  if "$@"; then echo "PASS: $name"; else echo "FAIL: $name"; FAILS=$((FAILS+1)); fi
}

command -v php >/dev/null 2>&1 || { echo "SKIP: php not installed"; exit 0; }
if [ -f artisan ] && [ -f composer.json ]; then
  [ -d vendor ] || step "composer install" composer install --no-interaction
  step "laravel test" php artisan test
  [ -f vendor/bin/pint ] && step "pint lint" vendor/bin/pint --test
else
  [ -d vendor ] || step "composer install" composer install --no-interaction
  if [ -f vendor/bin/phpunit ]; then step "phpunit" vendor/bin/phpunit
  elif [ -f vendor/bin/pest ]; then step "pest" vendor/bin/pest; else echo "SKIP: no phpunit/pest"; fi
  [ -f vendor/bin/phpstan ] && step "phpstan" vendor/bin/phpstan analyse
fi
step "php -l all" bash -c 'find . -name "*.php" -not -path "./vendor/*" -print0 | xargs -0 -n1 php -l 2>&1 | (! grep -v "No syntax errors")'

if [ "$FAILS" -gt 0 ]; then
  echo "QA RESULT: FAIL ($FAILS failing step(s))"
  exit 1
fi
echo "QA RESULT: PASS"
exit 0
