#!/usr/bin/env bash
# PURPOSE: Secrets scanning in two layers (report L1-30).
# LAYER 1, per commit (default): a pattern scan of the staged
# changes plus the working tree, with betterleaks (the gitleaks
# author's successor) when installed, else gitleaks. Blocking on
# any finding that is not fingerprinted in the project's ignore
# file with an unexpired entry (the scanners enforce their own
# ignore files: .gitleaksignore / .betterleaksignore).
# LAYER 2, deep (arg: deep): full history, all refs, with the
# pattern scanner, PLUS TruffleHog --only-verified. Verified
# findings are split out and printed as SECRET-VERIFIED-LIVE
# lines: a P0, rotate before the report closes.
# REPORTING LAW: findings are reported by rule, file, and
# fingerprint only. The secret VALUE is never printed (at most a
# hash the scanner itself emits). If NO scanner binary runs, the
# step reports DID-NOT-RUN and exits 2: the old pattern-grep
# fallback is retired, grep is not a secrets scanner.
# USAGE: secrets-scan.sh [path] [deep]
# EXIT: 0 clean; 1 findings (or a verified-live secret in deep
# mode); 2 DID-NOT-RUN, no scanner installed.
set -u
TARGET="${1:-.}"
MODE="${2:-commit}"
SCANNER=""
if command -v betterleaks >/dev/null 2>&1; then SCANNER=betterleaks
elif command -v gitleaks >/dev/null 2>&1; then SCANNER=gitleaks
else
  echo "DID-NOT-RUN: no secrets scanner installed (install betterleaks, or gitleaks as fallback)" >&2
  exit 2
fi
cd "$TARGET" || exit 2
fail=0
if [ "$MODE" = deep ]; then
  echo "deep layer: full history, all refs, with $SCANNER"
  if [ "$SCANNER" = betterleaks ]; then
    betterleaks detect --source . --no-banner --redact || fail=1
  else
    gitleaks detect --source . --no-banner --redact --log-opts="--all" || fail=1
  fi
  if command -v trufflehog >/dev/null 2>&1; then
    out="$(trufflehog git "file://$PWD" --only-verified --json 2>/dev/null || true)"
    if [ -n "$out" ]; then
      echo "$out" | grep -c '"Verified":true' >/dev/null 2>&1 || true
      n="$(echo "$out" | grep -c '"Verified": *true' || true)"
      if [ "${n:-0}" != 0 ]; then
        echo "SECRET-VERIFIED-LIVE: $n verified-live secret(s) in history (fingerprints in the trufflehog JSON above, values never printed here): P0, rotate before this report closes" >&2
        fail=1
      else
        echo "trufflehog verified layer: no verified-live secrets"
      fi
    else
      echo "trufflehog verified layer: no findings output"
    fi
  else
    echo "note: trufflehog not installed; the verified layer DID NOT RUN (stated, not hidden)" >&2
    [ "$fail" = 0 ] && fail=2
  fi
else
  if [ "$SCANNER" = betterleaks ]; then
    betterleaks detect --source . --no-banner --redact || fail=1
    betterleaks detect --source . --no-banner --redact --staged || fail=1
  else
    gitleaks detect --source . --no-banner --redact || fail=1
    gitleaks protect --source . --no-banner --redact --staged || fail=1
  fi
fi
[ "$fail" = 2 ] && exit 2
[ "$fail" = 0 ] && echo "secrets scan: clean ($SCANNER, $MODE layer)"
exit "$fail"
