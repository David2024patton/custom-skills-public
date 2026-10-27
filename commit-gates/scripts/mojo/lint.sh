#!/usr/bin/env bash
# PURPOSE: Mojo lint gate (report L1-13): compiler-as-lint plus the
# format check. There is NO Mojo linter, SAST tool, or coverage
# tool as of October 2026 (explicit gap, report L1-14); the
# compiler is the lint, and this script says so instead of
# pretending a clippy analogue exists.
# STEPS:
#   1. Format check: `mojo format` has no --check or --diff, so
#      the copy-format-diff workaround stands, hardened: copy the
#      sources to a temp dir, format the copies, diff. Any diff
#      is exit 1; the formatter missing is exit 2.
#   2. Compiler-as-lint: mojo build --Werror
#      --warn-on-unstable-apis --diagnose-missing-doc-strings
#      --diagnostic-format json on the entry point. Warnings are
#      errors here. A gate or project flag of --disable-warnings
#      anywhere in the tree is itself a finding.
#   3. debug_assert discipline: sources are grep-tiered for
#      debug_assert usage. The project declares its assertion
#      level in .gates-extra (ASSERT=all|safe|none, default
#      safe). Level none with debug_assert calls present is a
#      finding: assertions were compiled out by declaration.
#   Sanitizer builds (--sanitize address|thread) belong to the
#   nightly lane (mojo/deps.sh and the property harness), not
#   this per-commit gate.
# MODIFY PER PROJECT: entry point as extra arg when it is not
# main.mojo. Tool resolution: `pixi run mojo` when pixi.toml and
# pixi are present, else the mojo binary.
# USAGE: mojo/lint.sh [dir] [entry.mojo]
# EXIT: 0 clean; 1 findings; 2 mojo toolchain missing or no sources.
set -u
cd "${1:-.}" || exit 2
if [ -f pixi.toml ] && command -v pixi >/dev/null 2>&1; then MOJO="pixi run mojo"
elif command -v mojo >/dev/null 2>&1; then MOJO="mojo"
else echo "mojo not found (install Mojo, or pixi with a Mojo project)" >&2; exit 2; fi
mapfile -t files < <(find . \( -name '*.mojo' -o -name '*.🔥' \) -not -path './.pixi/*' -not -path './node_modules/*')
[ "${#files[@]}" = 0 ] && { echo "no Mojo sources found" >&2; exit 2; }
fail=0
grep -rq -- '--disable-warnings' . --include='*.toml' --include='*.sh' --include='*.mojo' 2>/dev/null && { echo "finding: --disable-warnings present in project files; a gate that silences its compiler is a green lie" >&2; fail=1; }
T="$(mktemp -d)"
for f in "${files[@]}"; do mkdir -p "$T/$(dirname "$f")"; cp "$f" "$T/$f"; done
( cd "$T" && $MOJO format . >/dev/null 2>&1 )
for f in "${files[@]}"; do
  cmp -s "$T/$f" "$f" || { echo "unformatted: $f (run: mojo format)"; fail=1; }
done
rm -rf "$T"
entry="${2:-}"
if [ -z "$entry" ]; then
  entry="$(find . -maxdepth 3 -name 'main.mojo' -not -path './.pixi/*' 2>/dev/null | head -1)"
fi
if [ -n "$entry" ]; then
  # shellcheck disable=SC2086
  $MOJO build --Werror --warn-on-unstable-apis --diagnose-missing-doc-strings --diagnostic-format json -o /tmp/mojo_gate_bin "$entry" || fail=1
else
  echo "note: no main.mojo entry point found, compiler-as-lint skipped (stated, not hidden)"
fi
ASSERT_LEVEL="safe"
[ -f .gates-extra ] && grep -q '^ASSERT=' .gates-extra && ASSERT_LEVEL="$(grep '^ASSERT=' .gates-extra | cut -d= -f2)"
if grep -rq 'debug_assert' --include='*.mojo' . 2>/dev/null; then
  echo "debug_assert: present (declared level: $ASSERT_LEVEL)"
  [ "$ASSERT_LEVEL" = "none" ] && { echo "finding: ASSERT=none declared while debug_assert calls exist; assertions silently compiled out" >&2; fail=1; }
else
  echo "debug_assert: none found (tier note; add debug_assert for internal invariants)"
fi
echo "GAP: no Mojo linter, SAST, or coverage tool exists as of October 2026; compiler-as-lint above is the whole lint story (report L1-14)"
exit "$fail"
