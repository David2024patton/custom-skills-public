#!/usr/bin/env bash
# PURPOSE: Run every applicable commit gate for the repo in the current
# directory: per-language lint + tests + debug check for each language
# detected, then the common secret scan and vulnerability scan.
# DETECTION: the single stack detector (stack-detect.py, I-02) decides
# which stacks are present and this script dispatches gate sets from its
# STACKS output. The inline marker detection below survives ONLY as a
# fallback for when the detector or python3 is unavailable, and the
# fallback announces itself loudly when it runs.
# MODIFY PER PROJECT: none normally. If the repo has its own gate script
# (for example tools/check.sh), prefer that and use this as the fallback.
# A project may list extra language folders in .gates-extra, one per line.
# USAGE: run-gates.sh [--quick]   (--quick skips tests and the vulnerability scan)
# EXIT: 0 all gates green; 1 a gate failed; 2 a required tool is missing
# (a gate script exited 2 and no gate failed). When the run exits 2 the
# tool-missing gate scripts are named in the final line.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
QUICK=0; [ "${1:-}" = "--quick" ] && QUICK=1
worst=0
missing_tools=""
run() {
  echo "== $*"
  local rc=0
  "$@" || rc=$?
  if [ "$rc" = 1 ]; then
    worst=1
  elif [ "$rc" = 2 ]; then
    missing_tools="$missing_tools $1"
    [ "$worst" = 0 ] && worst=2
  elif [ "$rc" != 0 ]; then
    worst=1
  fi
}
run_set() {
  # run_set <set-dir>: lint + debug-check always, test unless --quick.
  run "$HERE/$1/lint.sh"; run "$HERE/$1/debug-check.sh"
  [ "$QUICK" = 0 ] && run "$HERE/$1/test.sh"
}

# Language detection: the detector is primary (I-02).
DETECTOR_OK=0
STACKS=""
if command -v python3 >/dev/null 2>&1 && [ -f "$HERE/stack-detect.py" ]; then
  if DETECT_OUT="$(python3 "$HERE/stack-detect.py" --root . --format shell-vars 2>/dev/null)"; then
    STACKS="$(printf '%s\n' "$DETECT_OUT" | sed -n 's/^STACKS=//p')"
    DETECTOR_OK=1
  fi
fi

if [ "$DETECTOR_OK" = 1 ]; then
  dispatched=""
  for s in $STACKS; do
    case "$s" in
      go) setdir="go" ;;
      rust) setdir="rust" ;;
      mojo) setdir="mojo" ;;
      dart|flutter) setdir="dart-flutter" ;;
      python) setdir="python" ;;
      javascript) setdir="javascript" ;;
      typescript) setdir="typescript" ;;
      react) setdir="react" ;;
      nextjs) setdir="nextjs" ;;
      prisma) setdir="prisma" ;;
      php) setdir="php" ;;
      shell)
        run "$HERE/shell/lint.sh"
        continue ;;
      *) echo "WARNING: detector named unknown stack '$s'; no gate set dispatched for it" >&2; continue ;;
    esac
    case " $dispatched " in
      *" $setdir "*) ;;
      *) dispatched="$dispatched $setdir"; run_set "$setdir" ;;
    esac
  done
else
  echo "WARNING: stack detector unavailable (python3 or stack-detect.py missing, or the detector failed); falling back to legacy inline detection. Gate coverage may differ from the manifest." >&2
  # Legacy inline detection (fallback only; the detector is the law).
  if ls go.mod >/dev/null 2>&1; then
    run "$HERE/go/lint.sh"; run "$HERE/go/debug-check.sh"
    [ "$QUICK" = 0 ] && run "$HERE/go/test.sh"
  fi
  if ls Cargo.toml >/dev/null 2>&1; then
    run "$HERE/rust/lint.sh"; run "$HERE/rust/debug-check.sh"
    [ "$QUICK" = 0 ] && run "$HERE/rust/test.sh"
  fi
  if ls ./*.mojo >/dev/null 2>&1 || [ -f mojoproject.toml ]; then
    run "$HERE/mojo/lint.sh"; run "$HERE/mojo/debug-check.sh"
    [ "$QUICK" = 0 ] && run "$HERE/mojo/test.sh"
  fi
  if ls pubspec.yaml >/dev/null 2>&1; then
    run "$HERE/dart-flutter/lint.sh"; run "$HERE/dart-flutter/debug-check.sh"
    [ "$QUICK" = 0 ] && run "$HERE/dart-flutter/test.sh"
  fi
  if ls package.json >/dev/null 2>&1; then
    pkg_dep() { node -e "try{const p=require('./package.json');process.exit((p.dependencies&&p.dependencies['$1'])||(p.devDependencies&&p.devDependencies['$1'])?0:1)}catch(e){process.exit(1)}" 2>/dev/null; }
    pkg_esm() { node -e "try{process.exit(require('./package.json').type==='module'?0:1)}catch(e){process.exit(1)}" 2>/dev/null; }
    lang=""
    if [ -f tsconfig.json ] || pkg_dep typescript; then lang="typescript"
    elif pkg_esm; then lang="javascript"
    fi
    if [ -n "$lang" ]; then
      run "$HERE/$lang/lint.sh"; run "$HERE/$lang/debug-check.sh"
      [ "$QUICK" = 0 ] && run "$HERE/$lang/test.sh"
    else
      run "$HERE/js-ts/lint.sh"; run "$HERE/js-ts/debug-check.sh"
      [ "$QUICK" = 0 ] && run "$HERE/js-ts/test.sh"
    fi
    if pkg_dep react; then
      run "$HERE/react/lint.sh"; run "$HERE/react/debug-check.sh"
      [ "$QUICK" = 0 ] && run "$HERE/react/test.sh"
    fi
    if [ -f next.config.js ] || [ -f next.config.mjs ] || [ -f next.config.ts ] || [ -f next.config.cjs ] || pkg_dep next; then
      run "$HERE/nextjs/lint.sh"; run "$HERE/nextjs/debug-check.sh"
      [ "$QUICK" = 0 ] && run "$HERE/nextjs/test.sh"
    fi
    if [ -d prisma/schema ] || [ -f prisma/schema.prisma ] || [ -f schema.prisma ] || find prisma -maxdepth 1 -name '*.prisma' 2>/dev/null | grep -q . || pkg_dep prisma || pkg_dep @prisma/client; then
      run "$HERE/prisma/lint.sh"; run "$HERE/prisma/debug-check.sh"
      [ "$QUICK" = 0 ] && run "$HERE/prisma/test.sh"
    fi
  fi
  if ls pyproject.toml >/dev/null 2>&1 || ls requirements.txt >/dev/null 2>&1; then
    run "$HERE/python/lint.sh"; run "$HERE/python/debug-check.sh"
    [ "$QUICK" = 0 ] && run "$HERE/python/test.sh"
  fi
  if ls composer.json >/dev/null 2>&1 || find . -maxdepth 2 -name '*.php' -not -path './vendor/*' | grep -q .; then
    run "$HERE/php/lint.sh"; run "$HERE/php/debug-check.sh"
    [ "$QUICK" = 0 ] && run "$HERE/php/test.sh"
  fi
  if find . -name '*.sh' -not -path './node_modules/*' | grep -q .; then
    run "$HERE/shell/lint.sh"
  fi
fi

run "$HERE/common/secrets-scan.sh"
[ "$QUICK" = 0 ] && run "$HERE/common/vuln-scan.sh"
if [ "$worst" = 0 ]; then
  echo "GATES: ALL GREEN"
elif [ "$worst" = 2 ]; then
  echo "GATES: TOOL-MISSING (exit 2) from:$missing_tools"
else
  echo "GATES: RED"
fi
exit "$worst"
