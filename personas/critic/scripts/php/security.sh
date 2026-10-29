#!/usr/bin/env bash
# PURPOSE: PHP security layer. Three halves, all stated:
#   1. Runtime signal (SIG-PHP-2026-001): when a php binary is
#      available, its CLI version is compared against the
#      signature's fixed releases (8.2.35, 8.3.36, 8.4.27, 8.5.12;
#      no project fix exists for 8.1 and older). The signature is
#      explicit that the serving SAPI runtime is the primary
#      check and the CLI binary is a weak signal only: a CLI below
#      its branch floor is a finding (verify the serving runtime),
#      a CLI at or past the floor prints NO pass claim.
#   2. Dependency audit: composer audit over composer.lock when
#      composer and a lock file both exist. composer.json present
#      but no composer.lock is a finding (dependencies not locked,
#      cannot be audited). A lock file present but composer
#      missing is DID-NOT-RUN for this half, exit 2: a partial
#      pass never wears the full name (the Python set's exit law).
#   3. Sink greps, no tooling needed, every hit printed with
#      file:line for a human verdict:
#      - unserialize() call sites (object injection class; the
#        gate flags every site outside vendor/ and the verdict
#        turns on whether the bytes crossed a trust boundary)
#      - include, include_once, require, require_once lines
#        containing a variable (variable path includes)
#      - eval() call sites
#      - echo, print, or short-echo (<?=) of request superglobals
#        ($_GET, $_POST, $_REQUEST, $_COOKIE, $_FILES), and echo
#        of $_SERVER request values (PHP_SELF, REQUEST_URI, HTTP_*)
# EXIT LAW: findings are exit 1. A blocked dependency half (lock
# present, composer missing) is exit 2 and outranks findings,
# because the gate did not fully run.
# MODIFY PER PROJECT: none normally. A call site a human has
# proven safe is recorded in the project's own review notes; this
# script keeps flagging it, stated, rather than growing a silent
# allowlist.
# USAGE: php/security.sh [dir]
# EXIT: 0 clean; 1 findings; 2 dependency half DID-NOT-RUN.
set -u
cd "${1:-.}" || exit 2
fail=0
blocked=0
# Half 1: runtime version signal.
echo "runtime signal: SIG-PHP-2026-001 floors (8.2.35, 8.3.36, 8.4.27, 8.5.12); serving SAPI is the primary check, CLI version is a weak signal only"
if command -v php >/dev/null 2>&1; then
  ver="$(php -r 'echo PHP_VERSION;' 2>/dev/null || true)"
  if [ -n "$ver" ]; then
    echo "cli version observed: $ver"
    maj="$(printf '%s' "$ver" | cut -d. -f1)"; min="$(printf '%s' "$ver" | cut -d. -f2)"; pat="$(printf '%s' "$ver" | cut -d. -f3 | grep -oE '^[0-9]+')"
    floor=""
    case "$maj.$min" in
      8.2) floor=35 ;; 8.3) floor=36 ;; 8.4) floor=27 ;; 8.5) floor=12 ;;
    esac
    if [ -n "$floor" ]; then
      if [ "${pat:-0}" -lt "$floor" ]; then
        echo "finding: CLI PHP $ver is below the SIG-PHP-2026-001 fixed release for its branch ($maj.$min.$floor); weak signal, verify the serving runtime's version and worker state" >&2
        fail=1
      else
        echo "note: CLI at or past its branch floor; no pass is claimed from the CLI (the serving runtime decides)"
      fi
    elif [ "$maj" = 8 ] && [ "${min:-9}" -le 1 ] || [ "${maj:-9}" -lt 8 ]; then
      echo "finding: CLI PHP $ver is on a branch with no project fix per SIG-PHP-2026-001 (8.1 and older); weak signal, verify the serving runtime" >&2
      fail=1
    else
      echo "note: branch $maj.$min is not in the signature floor table (stated; no verdict from the CLI)"
    fi
  else
    echo "note: php present but its version could not be read (stated; no verdict from the CLI)"
  fi
else
  echo "note: php not found; runtime version signal DID-NOT-RUN (stated; grep half still runs)"
fi
# Half 2: dependency audit.
if [ -f composer.lock ]; then
  if command -v composer >/dev/null 2>&1; then
    echo "dependency audit: composer audit over composer.lock"
    composer audit || fail=1
  else
    echo "composer not found but composer.lock exists; dependency audit DID-NOT-RUN" >&2
    blocked=1
  fi
elif [ -f composer.json ]; then
  echo "finding: composer.json present but no composer.lock; dependencies are not locked and cannot be audited" >&2
  fail=1
else
  echo "note: no composer.json or composer.lock; dependency audit not applicable (stated)"
fi
# Half 3: sink greps.
scan() {
  label="$1"; pattern="$2"
  hits="$(grep -rnE "$pattern" --include='*.php' . 2>/dev/null | grep -v '/vendor/' || true)"
  if [ -n "$hits" ]; then
    echo "finding: $label" >&2
    printf '%s\n' "$hits" >&2
    fail=1
  fi
}
scan "unserialize() call site(s): object injection class; every site must prove its bytes never crossed a trust boundary" 'unserialize[[:space:]]*\('
inc_hits="$(grep -rnE '\b(include|include_once|require|require_once)\b' --include='*.php' . 2>/dev/null | grep -v '/vendor/' | grep '\$' || true)"
if [ -n "$inc_hits" ]; then
  echo "finding: include or require with a variable path" >&2
  printf '%s\n' "$inc_hits" >&2
  fail=1
fi
scan "eval() call site(s)" '\beval[[:space:]]*\('
scan "echo or print of request superglobals" '(echo|print)[[:space:]]+[^;]*\$_(GET|POST|REQUEST|COOKIE|FILES)'
scan "short echo of request superglobals" '<\?=[^?]*\$_(GET|POST|REQUEST|COOKIE|FILES)'
scan "echo of request-derived server values (PHP_SELF, REQUEST_URI, HTTP_ headers)" '(echo|print)[[:space:]]+[^;]*\$_SERVER\[[^]]*(PHP_SELF|REQUEST_URI|HTTP_)'
[ "$blocked" = 1 ] && exit 2
[ "$fail" = 0 ] && echo "php security: no findings"
exit "$fail"
