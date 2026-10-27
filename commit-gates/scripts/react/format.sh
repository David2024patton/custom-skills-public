#!/usr/bin/env bash
# PURPOSE: Web format gate (report L1-22). Format is its own
# gate, separate from lint.
# STEPS:
#   1. Two formatters configured is a FINDING: prettier config
#      (a prettier key, .prettierrc*, or prettier dep) together
#      with a Biome config (biome.json/biome.jsonc or @biomejs
#      dep used as formatter) means two tools own the same job.
#   2. Where Biome is the project's adopted formatter (biome
#      config, no prettier): biome format . runs as the check.
#   3. Default: prettier --check . (exit 0 clean / 1 unformatted
#      / 2 prettier missing, stated as tool-missing).
# MODIFY PER PROJECT: formatter choice and ignores live in the
# project's own config, not here.
# USAGE: format.sh [dir]
# EXIT: 0 formatted; 1 unformatted or two formatters; 2 the
# formatter is missing.
set -u
cd "${1:-.}" || exit 2
command -v npm >/dev/null 2>&1 || { echo "npm not found" >&2; exit 2; }
[ -f package.json ] || { echo "no package.json here" >&2; exit 2; }
has_dep() { node -e "const p=require('./package.json');process.exit((p.dependencies&&p.dependencies['$1'])||(p.devDependencies&&p.devDependencies['$1'])?0:1)" 2>/dev/null; }
has_prettier=0; has_biome=0
{ has_dep prettier || ls .prettierrc* prettier.config.* >/dev/null 2>&1 || node -e "process.exit(require('./package.json').prettier?0:1)" 2>/dev/null; } && has_prettier=1
{ [ -f biome.json ] || [ -f biome.jsonc ] || has_dep @biomejs/biome; } && has_biome=1
if [ "$has_prettier" = 1 ] && [ "$has_biome" = 1 ]; then
  echo "finding: two formatters configured (prettier and Biome); running two formatters is itself a finding (report L1-22)" >&2
  exit 1
fi
if [ "$has_biome" = 1 ]; then
  command -v npx >/dev/null 2>&1 || exit 2
  npx biome format . || exit 1
  echo "web format: clean (Biome, the project's adopted formatter)"
  exit 0
fi
has_dep prettier || { echo "prettier not declared; format gate DID-NOT-RUN (add prettier, or adopt Biome with a biome.json)" >&2; exit 2; }
npx prettier --check .
