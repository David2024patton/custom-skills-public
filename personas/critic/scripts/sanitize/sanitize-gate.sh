#!/usr/bin/env bash
# === CRITIC SCRIPT MANIFEST ===
# question: Does this web target sanitize user HTML with a current canonical sanitizer, on every sink, and does its sanitizer configuration actually stop the family XSS corpus?
# stackDetection: manifest stacks javascript, typescript, react, nextjs; the wrapper takes the stack as its first argument for evidence labeling and passes it to sanitize-gate.mjs.
# inputs: sanitize-gate.sh STACK TARGET_DIR [--mode quick|full] [--corpus PATH] [--refenv DIR] [--out PATH]
# effects: read-only on the target; the target-module leg of the Node gate imports target code in a child process inside the review sandbox.
# exits: 0 clean; 1 findings; 2 node missing or the corpus execution leg could not run (DID-NOT-RUN, stated); 3 gate error; 124 timeout (imposed by the caller).
# output: JSON lines on stdout from sanitize-gate.mjs; human summary on stderr.
# === END MANIFEST ===
# PURPOSE: Family-style wrapper for the executable sanitizer gate
# (scripts/sanitize/sanitize-gate.mjs). The heavy logic lives in the
# Node program; this wrapper resolves the stack and target arguments,
# checks the runtime, and propagates the gate exit code unchanged.
# USAGE: sanitize-gate.sh STACK TARGET_DIR [--mode quick|full] [--corpus PATH] [--refenv DIR] [--out PATH]
# EXIT: 0 clean; 1 findings; 2 node missing or execution leg DID-NOT-RUN; 3 gate error.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
STACK="${1:-}"; TARGET="${2:-}"
if [ -z "$STACK" ] || [ -z "$TARGET" ]; then
  echo "usage: sanitize-gate.sh STACK TARGET_DIR [--mode quick|full] [--corpus PATH] [--refenv DIR] [--out PATH]" >&2
  exit 3
fi
shift 2
command -v node >/dev/null 2>&1 || { echo "node not found; sanitizer corpus execution DID-NOT-RUN" >&2; exit 2; }
[ -d "$TARGET" ] || { echo "target directory missing: $TARGET" >&2; exit 3; }
exec node "$HERE/sanitize-gate.mjs" --root "$TARGET" --stack "$STACK" "$@"
