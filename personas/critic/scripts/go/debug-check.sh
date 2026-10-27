#!/usr/bin/env bash
# PURPOSE: Check that this Go module HAS its debugging built in, as
# concrete artefacts (report L1-04), not as a grep for any log line.
# STEPS:
#   1. Count diagnostic artefacts present; at least 2 are required:
#      a. log/slog in use
#      b. net/http/pprof or runtime/pprof imported
#      c. runtime/trace imported
#      d. an OpenTelemetry SDK import (go.opentelemetry.io/otel)
#   2. pprof safety: if a pprof import exists, a listener binding a
#      non-loopback address in the same files is a finding (pprof
#      belongs on an internal-only listener).
#   3. Print ban: fmt.Print* or log.Print* outside package main and
#      outside _test.go files is a finding (the forbidigo rule from
#      the report, enforced here by scan because this gate cannot
#      assume the project's golangci config enables forbidigo).
# MODIFY PER PROJECT: a project that names its diag package
# differently still passes on artefacts a-d; no config needed.
# USAGE: go/debug-check.sh [module-dir]
# EXIT: 0 at least 2 artefacts and no findings; 1 otherwise.
set -u
cd "${1:-.}" || exit 2
count=0
grep -rq '"log/slog"' --include='*.go' . && { echo "artefact: log/slog in use"; count=$((count+1)); }
grep -rqE '"net/http/pprof"|"runtime/pprof"' --include='*.go' . && { echo "artefact: pprof imported"; count=$((count+1)); }
grep -rq '"runtime/trace"' --include='*.go' . && { echo "artefact: runtime/trace imported"; count=$((count+1)); }
grep -rq 'go.opentelemetry.io/otel' --include='*.go' . && { echo "artefact: OpenTelemetry SDK imported"; count=$((count+1)); }
fail=0
[ "$count" -ge 2 ] || { echo "go debug check: only $count diagnostic artefact(s); at least 2 required (slog, pprof, trace, otel). Run debug-add.sh" >&2; fail=1; }
if grep -rqE '"net/http/pprof"|"runtime/pprof"' --include='*.go' .; then
  if grep -rE 'ListenAndServe\("(0\.0\.0\.0|\[::\]|:)' --include='*.go' . | grep -v '_test.go' | grep -q .; then
    echo "finding: a non-loopback ListenAndServe exists in a module importing pprof; pprof must sit on an internal-only listener" >&2; fail=1
  fi
fi
strays="$(grep -rnE '\bfmt\.Print|\blog\.Print' --include='*.go' . | grep -v '_test\.go' | grep -vE '^[^:]+:[0-9]+:package main' || true)"
# Keep only strays in files whose package is not main.
real=""
while IFS= read -r line; do
  [ -z "$line" ] && continue
  f="$(echo "$line" | cut -d: -f1)"
  head -20 "$f" 2>/dev/null | grep -q '^package main' || real="${real}${line}
"
done <<EOF2
$strays
EOF2
if [ -n "$real" ]; then
  echo "finding: fmt.Print*/log.Print* outside package main (use the slog diag channel):" >&2
  echo "$real" >&2; fail=1
fi
[ "$fail" = 0 ] && echo "go debug check: $count artefacts, no print strays"
exit "$fail"
