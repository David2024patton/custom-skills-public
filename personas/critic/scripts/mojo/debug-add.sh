#!/usr/bin/env bash
# PURPOSE: Print the standard Mojo diagnostic pattern, and (when
# asked) scaffold diag.mojo into a Mojo project directory. The
# pattern mirrors rust/debug-add.sh: a diag module with an emit
# function every refusal, overage, and verdict calls, and a refusal
# counter readable by status surfaces. Mojo has no log/tracing
# standard-library analogue in this pattern, so the scaffold's sink
# is print; hosted projects swap the sink inside diag.mojo, never at
# call sites. `mojo build -g` (debug info) and `mojo debug` are the
# toolchain's own debugging support and pair with this seam.
# MODIFY PER PROJECT: choose the sink per target at the seam, not at
# call sites. Refuses to overwrite an existing diag.mojo.
# USAGE: mojo/debug-add.sh [--apply] [project-dir]
# EXIT: 0 pattern printed or scaffold written; 2 no Mojo sources
# when applying.
set -u
cat <<'EOF'
PATTERN (adapt names to the project):
  # diag.mojo
  struct Diag:
      var refusals: Int
      fn __init__(out self):
          self.refusals = 0
      fn emit(mut self, event: String, what: String):
          if event == "refusal":
              self.refusals += 1
          print("diag", event, what)
  Every refusal path calls diag.emit("refusal", "...") exactly once.
  The counter lives in Diag so status surfaces can read it.
EOF
if [ "${1:-}" = "--apply" ]; then
  d="${2:-.}"
  ls "$d"/*.mojo >/dev/null 2>&1 || { echo "no .mojo sources in $d" >&2; exit 2; }
  if [ -f "$d/diag.mojo" ]; then echo "$d/diag.mojo already exists"; exit 0; fi
  cat > "$d/diag.mojo" <<'EOF'
# Diagnostic channel: every refusal, overage, and verdict emits here.
# The sink is print in this scaffold; swap it inside this file only,
# never at call sites.
struct Diag:
    var refusals: Int

    fn __init__(out self):
        self.refusals = 0

    fn emit(mut self, event: String, what: String):
        if event == "refusal":
            self.refusals += 1
        print("diag", event, what)
EOF
  echo "scaffolded $d/diag.mojo: wire Diag.emit at every refusal point"
fi
