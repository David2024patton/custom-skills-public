#!/usr/bin/env bash
# PURPOSE: JavaScript (plain ESM Node, "type": "module") lint gate.
# This set is for plain JavaScript ONLY.
# STEPS:
#   1. Syntax: run `node --check` on every .js/.mjs/.cjs source file
#      (node --check parses ESM when the nearest package.json says
#      "type": "module"; .mjs is always ESM).
#   2. Lint, from what the target repo declares in package.json:
#      a. the project's own lint script, when one is defined;
#      b. else `npx eslint . --max-warnings 0`, when eslint is a
#         declared dependency (--max-warnings 0 so warnings cannot
#         pass green through this gate's own invocation; report
#         L1-22/L1-28)
#         (the flat config eslint.config.* is the project's own);
#      c. else print the library "NO LINT CONFIGURED" line.
#   3. There is deliberately NO TypeScript step in this set, ever.
#      A TypeScript project uses the typescript set instead.
# MODIFY PER PROJECT: nothing here; rule sets are the project's own
# eslint config. Add eslint to package.json rather than editing
# this file.
# USAGE: javascript/lint.sh [dir]
# FLAT CONFIG: eslint.config.* is required when eslint is
# declared (inserted enforcement, report L1-22; see the block
# before the exit line).
# EXIT: 0 clean or no lint configured (stated); 1 findings; 2 no npm/node or no package.json.
set -u
cd "${1:-.}" || exit 2
command -v node >/dev/null 2>&1 || { echo "node not found" >&2; exit 2; }
command -v npm >/dev/null 2>&1 || { echo "npm not found" >&2; exit 2; }
[ -f package.json ] || { echo "no package.json here" >&2; exit 2; }
fail=0
while IFS= read -r f; do
  node --check "$f" || fail=1
done < <(find . \( -name '*.js' -o -name '*.mjs' -o -name '*.cjs' \) -not -path './node_modules/*' -not -path './.git/*' | sort)
has_script() { node -e "process.exit(require('./package.json').scripts&&require('./package.json').scripts['$1']?0:1)" 2>/dev/null; }
has_dep() { node -e "const p=require('./package.json');process.exit((p.dependencies&&p.dependencies['$1'])||(p.devDependencies&&p.devDependencies['$1'])?0:1)" 2>/dev/null; }
if has_script lint; then
  npm run lint || fail=1
elif has_dep eslint; then
  npx eslint . --max-warnings 0 || fail=1
else
  echo "NO LINT CONFIGURED: lint gate not enforced for this project"
  echo "note: no lint script and no eslint dependency in package.json (add eslint; stated, not hidden)"
fi
echo "note: plain JavaScript set: no TypeScript step runs here, by design"
# Flat-config enforcement (report L1-22): ESLint 10 is flat-config
# only. A repo whose eslint setup is legacy-only (.eslintrc*) or
# has eslint declared with NO flat config cannot be running the
# blocking typed rule set; that is a finding, not a pass.
if has_dep eslint; then
  if ! ls eslint.config.js eslint.config.mjs eslint.config.cjs eslint.config.ts eslint.config.mts >/dev/null 2>&1; then
    echo "finding: eslint is declared but no flat config (eslint.config.*) exists; ESLint 10 is flat-config only (report L1-22)" >&2
    fail=1
  fi
fi
exit "$fail"
