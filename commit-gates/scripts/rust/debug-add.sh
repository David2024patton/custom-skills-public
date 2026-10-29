#!/usr/bin/env bash
# PURPOSE: Print the standard Rust diagnostic pattern for this project
# class, and (for a crate with src/) scaffold src/diag.rs when asked.
# The pattern: a diag module with an emit function every refusal,
# overage, and verdict calls; counters readable by status surfaces;
# no_std friendly (a ring buffer sink on bare metal, log/tracing on
# hosted code).
# MODIFY PER PROJECT: choose the sink per target (UART/ring on bare
# metal, tracing on hosted) at the seam, not at call sites.
# USAGE: rust/debug-add.sh [--apply] [crate-dir]
# EXIT: 0 pattern printed or scaffold written; 2 no src/ when applying.
set -u
cat <<'EOF'
PATTERN (adapt names to the crate):
  pub mod diag {
      pub enum Event { Refusal, Overage, Verdict }
      pub fn emit(event: Event, what: &str) { /* sink: ring/log/tracing */ }
  }
  Every refusal path calls diag::emit(Event::Refusal, "...") exactly
  once. Counters live in diag so About/status surfaces can read them.
EOF
if [ "${1:-}" = "--apply" ]; then
  d="${2:-.}"
  [ -d "$d/src" ] || { echo "no src/ in $d" >&2; exit 2; }
  [ -f "$d/src/diag.rs" ] || cat > "$d/src/diag.rs" <<'EOF'
//! Diagnostic channel: every refusal, overage, and verdict emits here.
use core::sync::atomic::{AtomicU64, Ordering};

static REFUSALS: AtomicU64 = AtomicU64::new(0);

#[derive(Clone, Copy, Debug)]
pub enum Event {
    Refusal,
    Overage,
    Verdict,
}

/// Record one diagnostic event. The sink is project-chosen (ring
/// buffer on bare metal, log/tracing hosted); call sites never change.
pub fn emit(event: Event, _what: &str) {
    if matches!(event, Event::Refusal) {
        REFUSALS.fetch_add(1, Ordering::Relaxed);
    }
}

/// Refusals emitted since start, for status surfaces.
pub fn refusals() -> u64 {
    REFUSALS.load(Ordering::Relaxed)
}
EOF
  echo "scaffolded $d/src/diag.rs (add 'pub mod diag;' to lib.rs/main.rs)"
fi
