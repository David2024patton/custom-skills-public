#!/usr/bin/env bash
# PURPOSE: Scaffold the standard Go diagnostic seam into a module that
# lacks one: an internal/diag package wrapping log/slog with an Emit
# function for refusals, overages, and verdicts, plus a counters map a
# /debug or status surface can read. Refuses to overwrite an existing
# diag package.
# MODIFY PER PROJECT: after scaffolding, rename the package path in the
# import comment to the module path from go.mod, and wire Emit at every
# refusal point. Keep the shape: structured fields, no secrets in logs.
# USAGE: go/debug-add.sh [module-dir]
# EXIT: 0 scaffolded or already present; 2 not a Go module.
set -u
cd "${1:-.}" || exit 2
[ -f go.mod ] || { echo "no go.mod here" >&2; exit 2; }
if [ -d internal/diag ]; then echo "internal/diag already exists"; exit 0; fi
mkdir -p internal/diag
cat > internal/diag/diag.go <<'EOF'
// Package diag is this module's diagnostic channel. Every refusal,
// overage, and verdict emits through Emit so a failure can always be
// explained from the logs. Counters are readable by status surfaces.
package diag

import (
	"log/slog"
	"sync/atomic"
)

var refusals atomic.Int64

// Emit records one diagnostic event with structured fields.
func Emit(event string, fields ...any) {
	if event == "refusal" {
		refusals.Add(1)
	}
	slog.Info("diag", append([]any{"event", event}, fields...)...)
}

// Refusals returns how many refusals have been emitted since start.
func Refusals() int64 { return refusals.Load() }
EOF
echo "scaffolded internal/diag/diag.go: wire diag.Emit at every refusal point"
