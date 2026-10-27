#!/usr/bin/env bash
# PURPOSE: Scan the working tree for secrets before any commit. Uses
# betterleaks if installed (validates whether a found credential is
# live), else gitleaks. Any finding stops the commit.
# MODIFY PER PROJECT: add project-specific allowlist entries only via a
# .gitleaks.toml / .betterleaks.toml in the repo root, never by editing
# this script, and never allowlist a real credential.
# USAGE: secrets-scan.sh [path]   (default: current directory)
# EXIT: 0 clean; 1 findings; 2 no scanner installed.
set -u
TARGET="${1:-.}"
if command -v betterleaks >/dev/null 2>&1; then
  betterleaks detect --source "$TARGET" --no-banner || exit 1
elif command -v gitleaks >/dev/null 2>&1; then
  gitleaks detect --source "$TARGET" --no-banner || exit 1
else
  echo "NO SECRET SCANNER INSTALLED (install betterleaks or gitleaks)" >&2
  exit 2
fi
echo "secrets scan: clean"
