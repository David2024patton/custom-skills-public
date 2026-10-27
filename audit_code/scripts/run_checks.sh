#!/usr/bin/env bash
# Run the standard verification gates for every detected stack and print a PASS/FAIL/NOT RUN table.
# Usage: run_checks.sh [project_dir]
# Exit code: 1 if any gate FAILED, else 0. NOT RUN gates are reported but do not fail the script
# (they MUST be reported as unverified in the final report).
# Full logs per gate: $LOGDIR (default /tmp/audit_logs).
set -u
ROOT="$(cd "${1:-.}" && pwd)"
LOGDIR="${LOGDIR:-/tmp/audit_logs}"; mkdir -p "$LOGDIR"
HERE="$(cd "$(dirname "$0")" && pwd)"
RESULTS=(); FAILED=0

# gate <label> <dir> <command...>
# The command runs as argv ("$@"), never by re-parsing a command string.
# A call site that genuinely needs shell features passes bash -c
# explicitly and says why.
gate() {
  local label="$1" dir="$2"; shift 2
  local log="$LOGDIR/$(echo "$label" | tr -c 'A-Za-z0-9\n' '_').log"
  if ( cd "$dir" && "$@" ) >"$log" 2>&1; then
    RESULTS+=("PASS     | $label"); 
  else
    RESULTS+=("FAIL     | $label  (log: $log)"); FAILED=1
    echo "---- FAIL: $label (last 25 lines) ----"; tail -25 "$log"
  fi
}
skip() { RESULTS+=("NOT RUN  | $1 -- $2"); }
have() { command -v "$1" >/dev/null 2>&1; }

STACKS="$(bash "$HERE/detect_stack.sh" "$ROOT" | grep '^STACK' | grep -v '^STACK none ' || true)"

# ---------- Rust ----------
while read -r _ lang marker; do
  [ "$lang" = rust ] || continue
  d="$(dirname "$marker")"; n="rust:$(basename "$d")"
  if ! have cargo; then skip "$n" "cargo not installed"; continue; fi
  gate "$n fmt"    "$d" cargo fmt --all -- --check
  gate "$n clippy" "$d" cargo clippy --all-targets --all-features -- -D warnings
  gate "$n build"  "$d" cargo build --all-targets --all-features
  gate "$n test"   "$d" cargo test --all-features
  if cargo audit --version >/dev/null 2>&1; then gate "$n audit" "$d" cargo audit; else skip "$n audit" "cargo-audit not installed"; fi
  if [ -f "$d/deny.toml" ]; then
    if cargo deny --version >/dev/null 2>&1; then gate "$n deny" "$d" cargo deny check; else skip "$n deny" "cargo-deny not installed"; fi
  fi
done <<< "$STACKS"

# ---------- Go ----------
while read -r _ lang marker; do
  [ "$lang" = go ] || continue
  d="$(dirname "$marker")"; n="go:$(basename "$d")"
  if ! have go; then skip "$n" "go not installed"; continue; fi
  # bash -c: this check needs a pipe, command substitution, and a brace group.
  gate "$n gofmt" "$d" bash -c 'test -z "$(gofmt -l . | grep -v "^vendor/")" || { gofmt -l .; exit 1; }'
  gate "$n vet"   "$d" go vet ./...
  if have golangci-lint; then gate "$n golangci-lint" "$d" golangci-lint run ./...; else skip "$n golangci-lint" "not installed"; fi
  gate "$n build" "$d" go build ./...
  gate "$n test -race" "$d" go test -race -count=1 -shuffle=on -timeout 300s ./...
  if have govulncheck; then gate "$n govulncheck" "$d" govulncheck ./...; else skip "$n govulncheck" "not installed (go install golang.org/x/vuln/cmd/govulncheck@latest)"; fi
  # bash -c: this check needs command substitution, pipes, and a case statement.
  # ROOT reaches the child shell through env because bash -c starts a fresh
  # shell that cannot see this script's unexported variables.
  if [ -d "$ROOT/.github/workflows" ]; then gate "$n version consistency (go.mod vs CI)" "$d" env "ROOT=$ROOT" bash -c 'mod=$(sed -n "s/^toolchain go//p" go.mod | head -1); [ -z "$mod" ] && mod=$(sed -n "s/^go //p" go.mod | head -1); ci=$(grep -rhoE "go-version: .?[0-9]+\.[0-9]+" "$ROOT/.github/workflows" 2>/dev/null | grep -oE "[0-9]+\.[0-9]+" | head -1); if [ -n "$ci" ]; then case "$mod" in "$ci"*) echo "consistent: go.mod $mod, CI $ci";; *) echo "DRIFT: go.mod toolchain $mod vs CI go $ci"; exit 1;; esac; else echo "no CI go-version pin found"; fi'; fi
done <<< "$STACKS"

# ---------- Flutter / Dart ----------
while read -r _ lang marker; do
  case "$lang" in flutter|dart) ;; *) continue ;; esac
  d="$(dirname "$marker")"; n="$lang:$(basename "$d")"
  if [ "$lang" = flutter ]; then
    if ! have flutter; then skip "$n" "flutter not installed"; continue; fi
    gate "$n pub get" "$d" flutter pub get
    gate "$n format"  "$d" dart format --output=none --set-exit-if-changed .
    gate "$n analyze" "$d" flutter analyze
    if [ -d "$d/test" ]; then gate "$n test" "$d" flutter test; else RESULTS+=("FAIL     | $n test -- no test/ directory"); FAILED=1; fi
    [ -d "$d/integration_test" ] && skip "$n integration_test" "needs device/emulator: run manually: flutter test integration_test"
    if [ -d "$d/web" ]; then
      gate "$n build web (no CDN)" "$d" flutter build web --no-web-resources-cdn
      gate "$n FontManifest has bundled text font" "$d" python3 -c "import json,sys; fams={e.get('family') for e in json.load(open('build/web/assets/FontManifest.json'))}; extra=fams-{'MaterialIcons'}; print('font families:', sorted(x for x in fams if x)); sys.exit(0 if extra else 1)"
    fi
  else
    if ! have dart; then skip "$n" "dart not installed"; continue; fi
    gate "$n pub get" "$d" dart pub get
    gate "$n format"  "$d" dart format --output=none --set-exit-if-changed .
    gate "$n analyze" "$d" dart analyze --fatal-infos
    if [ -d "$d/test" ]; then gate "$n test" "$d" dart test; else RESULTS+=("FAIL     | $n test -- no test/ directory"); FAILED=1; fi
  fi
done <<< "$STACKS"

# ---------- Web (JS/TS) ----------
while read -r _ lang marker; do
  [ "$lang" = web ] || continue
  d="$(dirname "$marker")"; n="web:$(basename "$d")"
  if ! have node || ! have npm; then skip "$n" "node/npm not installed"; continue; fi
  if [ -f "$d/package-lock.json" ]; then gate "$n npm ci" "$d" npm ci --no-audit --no-fund; else skip "$n npm ci" "no package-lock.json: run npm install manually and say so"; fi
  if [ -f "$d/tsconfig.json" ] || grep -q '"typescript"' "$d/package.json" 2>/dev/null; then gate "$n tsc --noEmit" "$d" npx tsc --noEmit; else skip "$n tsc" "no TypeScript detected"; fi
  if ls "$d"/.eslintrc* >/dev/null 2>&1 || [ -f "$d/eslint.config.js" ] || [ -f "$d/eslint.config.mjs" ] || grep -q '"eslint"' "$d/package.json" 2>/dev/null; then gate "$n eslint" "$d" npx eslint .; else skip "$n eslint" "ESLint not configured"; fi
  if grep -q '"test"[[:space:]]*:' "$d/package.json" 2>/dev/null; then gate "$n npm test" "$d" npm test; else skip "$n npm test" "no test script in package.json"; fi
  if grep -q '"build"[[:space:]]*:' "$d/package.json" 2>/dev/null; then gate "$n npm run build" "$d" npm run build; else skip "$n build" "no build script in package.json"; fi
  if [ -f "$d/package-lock.json" ]; then gate "$n npm audit" "$d" npm audit --audit-level=high; else skip "$n npm audit" "no lockfile"; fi
done <<< "$STACKS"

# ---------- Secret history scan (all stacks) ----------
if [ -d "$ROOT/.git" ]; then
  if have gitleaks; then gate "secrets gitleaks (full history)" "$ROOT" gitleaks detect --source . --no-banner;
  elif have trufflehog; then gate "secrets trufflehog (full history)" "$ROOT" trufflehog git file://. --fail --no-update;
  else skip "secrets history scan" "gitleaks/trufflehog not installed: run the pattern-grep fallback in SKILL.md and report PARTIAL"; fi
fi

# ---------- Mojo ----------
while read -r _ lang marker; do
  [ "$lang" = mojo ] || continue
  d="$ROOT"; [ -f "$(dirname "$marker")/pixi.toml" ] && d="$(dirname "$marker")"
  n="mojo:$(basename "$d")"
  if [ -f "$d/pixi.toml" ] && have pixi; then M="pixi run mojo"; elif have mojo; then M="mojo"; else skip "$n" "mojo/pixi not installed"; continue; fi
  SRC="$(find "$d" -maxdepth 3 -name 'main.mojo' -not -path '*/.pixi/*' 2>/dev/null | head -1)"
  # Format check WITHOUT mutating the audited tree: copy sources to a temp dir,
  # format the copies, and diff. An audit must never dirty the diff it is reviewing.
  # bash -c: this check needs temp-dir variables, command substitution, a
  # pipe, and a subshell; it cannot be a plain argv command.
  gate "$n format (check-only, temp copy)" "$d" bash -c "T=\$(mktemp -d); find . -maxdepth 4 \\( -name '*.mojo' -o -name '*.🔥' \\) -not -path './.pixi/*' -exec cp --parents {} \"\$T\" \\; ; ( cd \"\$T\" && $M format . >/dev/null 2>&1 ); OUT=\$(find \"\$T\" -type f \\( -name '*.mojo' -o -name '*.🔥' \\) | while read -r f; do rel=\"\${f#\$T/}\"; cmp -s \"\$f\" \"\$rel\" || echo \"unformatted: \$rel\"; done); rm -rf \"\$T\"; if [ -n \"\$OUT\" ]; then echo \"\$OUT\"; exit 1; fi"
  if [ -n "$SRC" ]; then
    # bash -c: $M is itself a command string ("pixi run mojo" or "mojo"),
    # so a shell must split and run it; the entry path stays single-quoted.
    gate "$n build -g -D MOJO_DEBUG" "$d" bash -c "$M build -g -D MOJO_DEBUG -o /tmp/mojo_audit_bin '$SRC'"
  else skip "$n build" "no main.mojo found: build the entry point manually (or: $M package <src> -o /tmp/p.mojopkg)"; fi
  if [ -d "$d/test" ] || [ -d "$d/tests" ]; then
    T="$d/test"; [ -d "$T" ] || T="$d/tests"
    # bash -c: same $M command-string reason as the build gate above.
    gate "$n test" "$d" bash -c "$M test -I . '$T'"
  else RESULTS+=("FAIL     | $n test -- no test/ or tests/ directory"); FAILED=1; fi
  skip "$n lint" "Mojo has no dedicated linter: review compiler warnings + manual checklist (references/mojo.md)"
done <<< "$STACKS"

[ -z "$STACKS" ] && skip "all" "no supported stack detected under $ROOT"

echo; echo "================ TOOL VERSIONS ================"
for t in go cargo rustc flutter dart node npm golangci-lint govulncheck gitleaks trufflehog mojo; do
  if have "$t"; then if [ "$t" = go ]; then echo "go: $(go version 2>&1 | head -1)"; else echo "$t: $($t --version 2>&1 | head -1)"; fi; fi
done

echo; echo "================ VERIFICATION SUMMARY ================"
printf '%s\n' "${RESULTS[@]}"
echo "======================================================"
echo "Logs: $LOGDIR"
[ $FAILED -eq 0 ] && echo "RESULT: no failures (NOT RUN items remain UNVERIFIED)" || echo "RESULT: FAILURES PRESENT"
exit $FAILED
