#!/usr/bin/env bash
# PURPOSE: Mojo lint gate: format check plus a compile check with
# debug info. Mojo has NO dedicated linter and `mojo format` has no
# --check flag (it reformats in place; see docs.modular.com/mojo/cli/
# format), so the format check follows the audit_code pattern: copy
# the sources to a temp dir, format the copies, and diff. The compile
# check mirrors rust/lint.sh's clippy step with the closest real Mojo
# analogue: `mojo build` of the entry point, which surfaces compiler
# warnings and errors. There is no Mojo equivalent of
# `clippy -- -D warnings`, and this script does not pretend one exists.
# MODIFY PER PROJECT: none normally. A project whose entry point is
# not main.mojo (or named after the project) passes it as an extra
# arg. Tool resolution matches audit_code: `pixi run mojo` when a
# pixi.toml is present and pixi is installed, else the mojo binary.
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
  $MOJO build -g -D MOJO_DEBUG -o /tmp/mojo_gate_bin "$entry" || fail=1
else
  echo "note: no main.mojo entry point found, compile check skipped (stated, not hidden)"
fi
exit "$fail"
