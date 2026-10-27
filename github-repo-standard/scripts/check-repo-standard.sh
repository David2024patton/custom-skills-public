#!/usr/bin/env bash
# PURPOSE: Check a repo against the github-repo-standard file set.
# Prints one row per standard file (present or missing, instruction
# header present or stripped), a TODO and PLAN cross-reference sample
# check in both directions, one row per standard machinery file, and
# a conformance summary line.
# MODIFY PER PROJECT: none. The file lists below are the standard;
# when the standard changes, this script changes in the same pass.
# USAGE: check-repo-standard.sh [--strict] [repo-path]
#   repo-path defaults to the current directory.
#   --strict also fails on missing machinery files, stripped headers,
#   and failed cross-reference samples.
# EXIT: 0 conforming; 1 a non-negotiable standard file is missing
#   (or, under --strict, any reported defect); 2 bad input.
# DIAGNOSTICS: every failure prints DIAG lines to stderr naming the
#   repo, the file, and the check that failed, so a red run explains
#   itself. Set CHECK_REPO_STANDARD_DEBUG=1 for per-file debug lines.
# DEPENDENCIES: bash plus coreutils and grep only.
set -u

DEBUG="${CHECK_REPO_STANDARD_DEBUG:-0}"
STRICT=0
REPO=""

for arg in "$@"; do
  case "$arg" in
    --strict) STRICT=1 ;;
    --help|-h)
      echo "USAGE: check-repo-standard.sh [--strict] [repo-path]"
      exit 0
      ;;
    --*) echo "DIAG: unknown option: $arg" >&2; exit 2 ;;
    *) REPO="$arg" ;;
  esac
done
REPO="${REPO:-.}"

diag() { printf 'DIAG: %s\n' "$*" >&2; }
debug() { [ "$DEBUG" = "1" ] && printf 'DEBUG: %s\n' "$*" >&2; return 0; }

if [ ! -d "$REPO" ]; then
  diag "repo path is not a directory: $REPO"
  exit 2
fi
REPO_ABS="$(cd "$REPO" && pwd)" || { diag "cannot resolve repo path: $REPO"; exit 2; }
debug "checking repo at $REPO_ABS (strict=$STRICT)"

# The non-negotiable standard set (github-repo-standard/SKILL.md).
STANDARD_FILES="TODO.md IDEA.md PLAN.md ENDGOAL.md STATUS.md DECISIONS.md CHANGELOG.md REFERENCES.md README.md docs/RULES.md docs/RUNBOOK.md docs/MAP.md"
# The standard machinery files (same SKILL.md, machinery section).
MACHINERY_FILES=".gitignore .editorconfig .gitattributes CODEOWNERS SECURITY.md .github/pull_request_template.md .github/workflows/gates.yml"

total=0
present_count=0
missing_nonnegotiable=0
missing_machinery=0
header_ok=0
header_stripped=0
xref_ok=0
xref_fail=0
xref_skipped=0

has_header() {
  # Instruction headers live in an HTML comment at the top of the
  # template files: the marker text appears in the first 40 lines.
  head -n 40 "$1" 2>/dev/null | grep -q 'INSTRUCTIONS FOR THIS FILE'
}

printf '%-38s %-8s %-10s %s\n' "FILE" "STATUS" "HEADER" "NOTE"
printf '%-38s %-8s %-10s %s\n' "----" "------" "------" "----"

for f in $STANDARD_FILES; do
  total=$((total + 1))
  path="$REPO_ABS/$f"
  if [ -f "$path" ]; then
    present_count=$((present_count + 1))
    if has_header "$path"; then
      header_ok=$((header_ok + 1))
      printf '%-38s %-8s %-10s %s\n' "$f" "present" "present" ""
    else
      header_stripped=$((header_stripped + 1))
      printf '%-38s %-8s %-10s %s\n' "$f" "present" "STRIPPED" "instruction header missing"
      diag "header stripped or never added: $f"
    fi
  else
    missing_nonnegotiable=$((missing_nonnegotiable + 1))
    printf '%-38s %-8s %-10s %s\n' "$f" "MISSING" "n/a" "non-negotiable standard file"
    diag "missing non-negotiable file: $f (repo: $REPO_ABS)"
  fi
  debug "checked standard file $f"
done

for f in $MACHINERY_FILES; do
  total=$((total + 1))
  path="$REPO_ABS/$f"
  if [ -f "$path" ]; then
    present_count=$((present_count + 1))
    printf '%-38s %-8s %-10s %s\n' "$f" "present" "n/a" "machinery file"
  else
    missing_machinery=$((missing_machinery + 1))
    printf '%-38s %-8s %-10s %s\n' "$f" "MISSING" "n/a" "machinery file"
    diag "missing machinery file: $f (repo: $REPO_ABS)"
  fi
  debug "checked machinery file $f"
done

# Cross-reference sample check, both directions. Samples up to 5
# entries per direction so the output stays readable; a sample is a
# check of the linking discipline, not a full audit of either file.
SAMPLE=5
TODO_FILE="$REPO_ABS/TODO.md"
PLAN_FILE="$REPO_ABS/PLAN.md"

if [ -f "$TODO_FILE" ] && [ -f "$PLAN_FILE" ]; then
  checked=0
  while IFS= read -r line; do
    [ "$checked" -ge "$SAMPLE" ] && break
    id="$(printf '%s' "$line" | grep -oE 'T-[0-9]+\.[0-9]+' | head -n 1)"
    sec="$(printf '%s' "$line" | grep -oE '\(PLAN S[0-9]+\)' | grep -oE '[0-9]+' | head -n 1)"
    [ -z "$id" ] && continue
    checked=$((checked + 1))
    if [ -z "$sec" ] && printf '%s' "$line" | grep -q '(PLAN S'; then
      xref_skipped=$((xref_skipped + 1))
      printf '%-38s %-8s %-10s %s\n' "XREF TODO->PLAN" "SKIPPED" "n/a" "$id carries a placeholder (PLAN S<n>) tag (unfilled template)"
      debug "xref TODO->PLAN skipped for $id: placeholder tag in an unfilled template"
    elif [ -z "$sec" ]; then
      xref_fail=$((xref_fail + 1))
      printf '%-38s %-8s %-10s %s\n' "XREF TODO->PLAN" "FAIL" "n/a" "$id carries no (PLAN S<n>) tag"
      diag "xref TODO->PLAN failed: $id in TODO.md has no PLAN tag"
    elif grep -Eq "^## S${sec}([: ]|$)" "$PLAN_FILE"; then
      xref_ok=$((xref_ok + 1))
      printf '%-38s %-8s %-10s %s\n' "XREF TODO->PLAN" "ok" "n/a" "$id -> PLAN S$sec exists"
    else
      xref_fail=$((xref_fail + 1))
      printf '%-38s %-8s %-10s %s\n' "XREF TODO->PLAN" "FAIL" "n/a" "$id -> PLAN S$sec not found in PLAN.md"
      diag "xref TODO->PLAN failed: $id points at PLAN S$sec, no such section in PLAN.md"
    fi
  done <<EOF_TODO
$(grep -E 'T-[0-9]+\.[0-9]+' "$TODO_FILE" 2>/dev/null)
EOF_TODO
  if [ "$checked" -eq 0 ]; then
    xref_skipped=$((xref_skipped + 1))
    printf '%-38s %-8s %-10s %s\n' "XREF TODO->PLAN" "SKIPPED" "n/a" "no numbered TODO ids sampled"
    diag "xref TODO->PLAN skipped: no numbered TODO ids found (template placeholders are not numeric)"
  fi

  checked=0
  plan_todo_skip=0
  if grep -qF '(PLAN S<n>)' "$TODO_FILE"; then
    xref_skipped=$((xref_skipped + 1))
    printf '%-38s %-8s %-10s %s\n' "XREF PLAN->TODO" "SKIPPED" "n/a" "TODO.md is an unfilled template (placeholder PLAN tags)"
    debug "xref PLAN->TODO skipped: TODO.md carries placeholder (PLAN S<n>) tags"
    plan_todo_skip=1
    checked=1
  fi
  for sec in $(grep -oE '^## S[0-9]+' "$PLAN_FILE" 2>/dev/null | grep -oE '[0-9]+'); do
    [ "$plan_todo_skip" = "1" ] && break
    [ "$checked" -ge "$SAMPLE" ] && break
    checked=$((checked + 1))
    if grep -q "(PLAN S${sec})" "$TODO_FILE"; then
      xref_ok=$((xref_ok + 1))
      printf '%-38s %-8s %-10s %s\n' "XREF PLAN->TODO" "ok" "n/a" "PLAN S$sec is referenced from TODO.md"
    else
      xref_fail=$((xref_fail + 1))
      printf '%-38s %-8s %-10s %s\n' "XREF PLAN->TODO" "FAIL" "n/a" "PLAN S$sec has no (PLAN S$sec) reference in TODO.md"
      diag "xref PLAN->TODO failed: PLAN section S$sec is not referenced from TODO.md"
    fi
  done
  if [ "$checked" -eq 0 ]; then
    xref_skipped=$((xref_skipped + 1))
    printf '%-38s %-8s %-10s %s\n' "XREF PLAN->TODO" "SKIPPED" "n/a" "no numbered PLAN sections sampled"
    diag "xref PLAN->TODO skipped: no numbered PLAN sections found"
  fi
else
  xref_skipped=$((xref_skipped + 1))
  printf '%-38s %-8s %-10s %s\n' "XREF TODO<->PLAN" "SKIPPED" "n/a" "TODO.md or PLAN.md missing"
  diag "xref skipped: TODO.md or PLAN.md missing in $REPO_ABS"
fi

result="PASS"
fail=0
if [ "$missing_nonnegotiable" -gt 0 ]; then
  result="FAIL"
  fail=1
fi
if [ "$STRICT" = "1" ] && { [ "$missing_machinery" -gt 0 ] || [ "$header_stripped" -gt 0 ] || [ "$xref_fail" -gt 0 ]; }; then
  result="FAIL"
  fail=1
fi

printf 'CONFORMANCE: %s/%s files present, headers %s ok / %s stripped, machinery missing %s, xref %s ok / %s failed / %s skipped, RESULT: %s (repo: %s)\n' \
  "$present_count" "$total" "$header_ok" "$header_stripped" "$missing_machinery" "$xref_ok" "$xref_fail" "$xref_skipped" "$result" "$REPO_ABS"

if [ "$fail" = "1" ]; then
  diag "conformance FAILED for $REPO_ABS: missing non-negotiable=$missing_nonnegotiable, machinery missing=$missing_machinery, headers stripped=$header_stripped, xref failed=$xref_fail, strict=$STRICT"
fi
exit "$fail"
