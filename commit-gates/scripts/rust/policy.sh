#!/usr/bin/env bash
# PURPOSE: Rust dependency and policy gate (report L1-08).
# STEPS:
#   1. Hard gate: cargo deny check (advisories, bans, licenses,
#      sources) against the project's committed deny.toml
#      (template shipped beside this script: explicit license
#      allowlist, every advisory ignore carries an expiry
#      comment). No deny.toml: exit 2, stated; the policy the
#      template encodes is not in force without it.
#   2. cargo-deny missing: exit 2 with the install hint. A
#      missing policy tool is never a pass.
#   The fast cargo audit lane lives in common/vuln-scan.sh
#   (cargo audit --deny warnings); this script is the policy
#   superset, not a duplicate of it.
# MODIFY PER PROJECT: policy lives in deny.toml, not here.
# USAGE: rust/policy.sh [dir]
# EXIT: 0 policy clean; 1 policy findings; 2 cargo-deny or
# deny.toml missing.
set -u
export PATH="$HOME/.cargo/bin:$PATH"
cd "${1:-.}" || exit 2
command -v cargo >/dev/null 2>&1 || { echo "cargo not found" >&2; exit 2; }
cargo deny --version >/dev/null 2>&1 || { echo "cargo-deny not found (install: cargo install cargo-deny); policy gate DID NOT RUN" >&2; exit 2; }
[ -f deny.toml ] || { echo "no committed deny.toml (copy the template shipped beside this script); policy gate DID NOT RUN" >&2; exit 2; }
cargo deny check
rc=$?
# cargo-deny uses its own exit codes (for example 4 for license
# failures); the gate normalises any failure to exit 1.
[ "$rc" != 0 ] && { echo "cargo-deny raw exit $rc normalised to gate exit 1" >&2; exit 1; }
exit 0
