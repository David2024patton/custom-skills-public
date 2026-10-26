#!/usr/bin/env bash
# Detect which of Mojo / Rust / Go / Flutter are present in a project and which toolchains are installed.
# Usage: detect_stack.sh [project_dir]
# Output: lines "STACK <name> <path-of-marker>" and "TOOL <name> <ok|missing>"; exit 0 always.
set -u
ROOT="${1:-.}"
EXCL=(-not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/target/*' -not -path '*/.dart_tool/*' -not -path '*/build/*' -not -path '*/.pixi/*' -not -path '*/.magic/*' -not -path '*/vendor/*')
found=0
mark() { echo "STACK $1 $2"; found=1; }

while IFS= read -r f; do mark rust "$f"; done < <(find "$ROOT" -maxdepth 4 -name Cargo.toml "${EXCL[@]}" 2>/dev/null)
while IFS= read -r f; do mark go "$f"; done < <(find "$ROOT" -maxdepth 4 -name go.mod "${EXCL[@]}" 2>/dev/null)
while IFS= read -r f; do
  if grep -q "flutter" "$f" 2>/dev/null; then mark flutter "$f"; else mark dart "$f"; fi
done < <(find "$ROOT" -maxdepth 4 -name pubspec.yaml "${EXCL[@]}" 2>/dev/null)
while IFS= read -r f; do mark web "$f"; done < <(find "$ROOT" -maxdepth 3 -name package.json "${EXCL[@]}" 2>/dev/null)
mojo_hit=$(find "$ROOT" -maxdepth 5 \( -name '*.mojo' -o -name '*.🔥' -o -name mojoproject.toml \) "${EXCL[@]}" 2>/dev/null | head -1)
[ -z "$mojo_hit" ] && [ -f "$ROOT/pixi.toml" ] && grep -qi "mojo\|max" "$ROOT/pixi.toml" 2>/dev/null && mojo_hit="$ROOT/pixi.toml"
[ -n "$mojo_hit" ] && mark mojo "$mojo_hit"

[ $found -eq 0 ] && echo "STACK none (no Cargo.toml/go.mod/pubspec.yaml/package.json/*.mojo found under $ROOT)"

chk() { if command -v "$1" >/dev/null 2>&1; then echo "TOOL $1 ok"; else echo "TOOL $1 missing"; fi; }
for t in cargo rustc go gofmt golangci-lint govulncheck flutter dart mojo pixi magic git node npm npx gitleaks trufflehog; do chk "$t"; done
if command -v cargo >/dev/null 2>&1; then
  for sub in clippy fmt audit deny miri llvm-cov; do
    if cargo "$sub" --version >/dev/null 2>&1 || cargo "$sub" --help >/dev/null 2>&1; then echo "TOOL cargo-$sub ok"; else echo "TOOL cargo-$sub missing"; fi
  done
fi
exit 0
