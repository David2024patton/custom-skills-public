#!/usr/bin/env bash
# PURPOSE: Runtime-version gate family (report L1-29, generalising
# the PHP2Shell signature from Cluster B). The version that SERVES
# or BUILT the artefact is checked, never a manifest constraint:
# a composer.json / package.json / go.mod line is a claim, not the
# runtime.
# SIGNATURE FILE: passed as an argument (the canonical signature
# library ships separately; this gate reads whatever file it is
# given). Format, one entry per line, pipe-separated, comments
# start with #:
#   SIG-ID | runtime | fixed-versions | vulnerable-below | notes
# Example:
#   SIG-PHP-2026-001 | php | 8.5.12,8.4.27,8.3.36,8.2.35 | branch | CVE-2026-109618/619 PHP2Shell; backports may fix without a version bump
# Fields:
#   fixed-versions: comma list of the first fixed release per
#     branch, or the single fixed release for a fixed-release
#     runtime (Node, Python: the advisory floor).
#   vulnerable-below: "branch" means compare within the artefact's
#     own branch (PHP style); "floor" means any version below the
#     listed release is vulnerable (single-line runtimes).
# VERDICT STATES per runtime found:
#   PATCHED-UPSTREAM: version at or above its branch fix (or the
#     floor). PATCHED-BACKPORT: only when the caller supplies a
#     backport attestation file (arg 3) naming the SIG-ID, the
#     vendor, and the vendor advisory ID; a version string alone
#     can never claim backport. VULNERABLE: below the fix with no
#     attestation. UNKNOWN: runtime present but version unreadable,
#     or a branch with no listed fix (for example PHP 8.1 and
#     older for SIG-PHP-2026-001, where no upstream fix exists):
#     UNKNOWN is never a pass.
# PROBES:
#   php: the php binary's version (in a deployed check this gate
#     is pointed at the serving runtime's version file, arg 2 may
#     be a file containing "runtime version" lines instead of
#     probing binaries; see USAGE).
#   node: node --version. python: python3 --version.
#   go: go version -m on a built binary (arg 2 = binary path), or
#     the go toolchain version when arg 2 is a directory.
# This gate never sends exploit traffic; it compares versions.
# USAGE: runtime-version.sh <signature-file> [version-file|binary|dir] [backport-attestations]
#   version-file lines look like: php 8.4.10 / node v22.9.0 /
#   python 3.12.3 / go go1.26.9
# EXIT: 0 every runtime found is PATCHED-UPSTREAM or
# PATCHED-BACKPORT; 1 any VULNERABLE; 2 signature file missing,
# or any runtime UNKNOWN, or no runtime found at all.
set -u
SIG="${1:-}"
[ -n "$SIG" ] && [ -f "$SIG" ] || { echo "signature file missing (pass the signature library path as arg 1)" >&2; exit 2; }
SRC="${2:-.}"
ATTEST="${3:-}"
declare -A VER
if [ -f "$SRC" ] && grep -qE '^(php|node|python|go) ' "$SRC" 2>/dev/null; then
  while read -r rt v; do VER["$rt"]="$v"; done < <(grep -E '^(php|node|python|go) ' "$SRC")
elif [ -n "$SRC" ] && [ -f "$SRC" ] && [ -x "$SRC" ]; then
  if command -v go >/dev/null 2>&1; then
    gv="$(go version -m "$SRC" 2>/dev/null | awk '/^.*: go[0-9]/{print $2; exit} /build.*-ldflags/{next}')"
    [ -z "$gv" ] && gv="$(go version -m "$SRC" 2>/dev/null | grep -m1 -oE 'go[0-9]+\.[0-9]+(\.[0-9]+)?' || true)"
    [ -n "$gv" ] && VER[go]="$gv"
  fi
else
  command -v php >/dev/null 2>&1 && VER[php]="$(php -r 'echo PHP_VERSION;' 2>/dev/null)"
  command -v node >/dev/null 2>&1 && VER[node]="$(node --version 2>/dev/null)"
  command -v python3 >/dev/null 2>&1 && VER[python]="$(python3 -c 'import platform;print(platform.python_version())' 2>/dev/null)"
  if command -v go >/dev/null 2>&1; then VER[go]="$(go version 2>/dev/null | grep -oE 'go[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1)"; fi
fi
[ "${#VER[@]}" = 0 ] && { echo "UNKNOWN: no runtime version could be probed (never a pass)" >&2; exit 2; }
verlt() { # verlt A B: true if A < B (dotted numeric compare)
  python3 -c "
import sys
def p(v):
    v=v.lstrip('v').replace('go','',1) if v.startswith('go') else v.lstrip('v')
    return [int(x) for x in v.split('.') if x.isdigit()]
sys.exit(0 if p('$1') < p('$2') else 1)" 2>/dev/null
}
fail=0; unknown=0
while IFS='|' read -r id rt fixed mode notes; do
  id="$(echo "$id" | tr -d ' ')"
  case "$id" in ''|'#'*) continue ;; esac
  rt="$(echo "$rt" | tr -d ' ')"
  v="${VER[$rt]:-}"
  [ -z "$v" ] && continue
  vclean="$(echo "$v" | sed 's/^v//; s/^go//')"
  branch="$(echo "$vclean" | cut -d. -f1-2)"
  fix=""
  IFS=',' read -ra FIXES <<< "$(echo "$fixed" | tr -d ' ')"
  for f in "${FIXES[@]}"; do
    if [ "$mode" = " branch " ] || [ "$(echo "$mode"|tr -d ' ')" = "branch" ]; then
      [ "$(echo "$f" | cut -d. -f1-2)" = "$branch" ] && fix="$f"
    else
      fix="$f"
    fi
  done
  if [ -z "$fix" ]; then
    echo "$id $rt $vclean: UNKNOWN (no fixed release listed for branch $branch; no upstream fix to compare against, never a pass)"
    unknown=1; continue
  fi
  if verlt "$vclean" "$fix"; then
    if [ -n "$ATTEST" ] && [ -f "$ATTEST" ] && grep -q "$id" "$ATTEST"; then
      echo "$id $rt $vclean: PATCHED-BACKPORT ($(grep "$id" "$ATTEST" | head -1))"
    else
      echo "$id $rt $vclean: VULNERABLE (fixed in $fix; $notes)" >&2
      fail=1
    fi
  else
    echo "$id $rt $vclean: PATCHED-UPSTREAM (at or above $fix)"
  fi
done < "$SIG"
[ "$fail" = 1 ] && exit 1
[ "$unknown" = 1 ] && exit 2
exit 0
