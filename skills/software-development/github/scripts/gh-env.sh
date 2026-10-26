#!/usr/bin/env bash
# GitHub environment detection helper for this skill.
#
# Usage: source this file from the skill folder (the folder holding SKILL.md,
# where scripts/ and references/ are siblings):
#
#   source scripts/gh-env.sh
#
# Or source it by any path that reaches this file. The helper locates nothing
# outside itself and reads no credential files.
#
# After sourcing, these variables are set:
#   GH_AUTH_METHOD  - "gh" or "none" (there is no token based fallback)
#   GH_USER         - GitHub username (only when authenticated)
#   GH_OWNER        - repo owner  (only if inside a git repo with a github remote)
#   GH_REPO         - repo name   (only if inside a git repo with a github remote)
#   GH_OWNER_REPO   - owner/repo  (only if inside a git repo with a github remote)
#
# Authentication rule: agents authenticate only through gh auth. This helper
# never reads, extracts, stores, or prints a token, and it sets no token
# variable. If gh is missing or not logged in, GH_AUTH_METHOD is "none" and
# the only fix is to install gh and run gh auth login. See
# references/auth.md in this skill.

# --- Auth detection ---

GH_AUTH_METHOD="none"
GH_USER=""

if command -v gh &>/dev/null && gh auth status &>/dev/null 2>&1; then
    GH_AUTH_METHOD="gh"
    GH_USER=$(gh api user --jq '.login' 2>/dev/null)
fi

# --- Repo detection (if inside a git repo with a GitHub remote) ---

GH_OWNER=""
GH_REPO=""
GH_OWNER_REPO=""

_remote_url=$(git remote get-url origin 2>/dev/null)
if [ -n "$_remote_url" ] && echo "$_remote_url" | grep -q "github.com"; then
    GH_OWNER_REPO=$(echo "$_remote_url" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
    GH_OWNER=$(echo "$GH_OWNER_REPO" | cut -d/ -f1)
    GH_REPO=$(echo "$GH_OWNER_REPO" | cut -d/ -f2)
fi
unset _remote_url

# --- Summary ---

echo "GitHub Auth: $GH_AUTH_METHOD"
[ -n "$GH_USER" ]       && echo "User: $GH_USER"
[ -n "$GH_OWNER_REPO" ] && echo "Repo: $GH_OWNER_REPO"
[ "$GH_AUTH_METHOD" = "none" ] && echo "Not authenticated: install gh, run 'gh auth login', then retry. See references/auth.md in this skill."

export GH_AUTH_METHOD GH_USER GH_OWNER GH_REPO GH_OWNER_REPO
