#!/usr/bin/env bash
# PURPOSE: Next.js security checklist gate (report L1-25, the
# remainder beyond never-next-lint and ignoreBuildErrors). Static
# checks, each printed with its verdict. Server Actions are
# public POST endpoints; the checklist treats them that way.
# CHECKS:
#   1. typedRoutes: an App Router TypeScript project must have
#      experimental.typedRoutes (15.x) or typedRoutes (16+) on
#      in next.config, and next typegen must be wired (the lint
#      gate runs it). typedRoutes has been stable since 15.5.
#   2. Server Actions: every "use server" file is listed; each
#      must show an auth signal (auth(, getServerSession,
#      currentUser, verifySession, requireAuth) AND an input
#      validation signal (zod, .parse(, validate, schema) in the
#      same file or a sibling schema module. A file with neither
#      is a finding per action file.
#   3. Headers: a headers() definition or middleware must set
#      Content-Security-Policy, Strict-Transport-Security,
#      X-Content-Type-Options (nosniff), and Referrer-Policy.
#      Each missing header is a finding.
#   4. No secret-named NEXT_PUBLIC_ variables: NEXT_PUBLIC_ names
#      containing SECRET, KEY, TOKEN, or PASSWORD ship to the
#      browser by design; any hit is a FAIL.
#   5. images config must use remotePatterns; the deprecated
#      domains key is a finding.
#   6. Auth must not live ONLY in proxy/middleware (the
#      CVE-2025-29927 pattern class): if auth checks appear only
#      in middleware.* and in no route, layout, or action file,
#      that is a finding.
# MODIFY PER PROJECT: none; the signals are heuristics and are
# printed for a human or critic to confirm.
# USAGE: nextjs/security.sh [dir]
# EXIT: 0 checklist clean; 1 findings; 2 not a Next project.
set -u
cd "${1:-.}" || exit 2
[ -f package.json ] || { echo "no package.json here" >&2; exit 2; }
node -e "const p=require('./package.json');process.exit((p.dependencies&&p.dependencies.next)||(p.devDependencies&&p.devDependencies.next)?0:1)" 2>/dev/null || { echo "not a Next.js project" >&2; exit 2; }
fail=0
cfg="$(ls next.config.js next.config.mjs next.config.ts next.config.cjs 2>/dev/null | head -1)"
if [ -n "$cfg" ]; then
  if grep -qE 'domains[[:space:]]*:' "$cfg"; then
    echo "finding: $cfg uses images.domains, which is deprecated; use remotePatterns" >&2; fail=1
  fi
  if [ -f tsconfig.json ] && [ -d app ] || [ -d src/app ]; then
    grep -q 'typedRoutes' "$cfg" || { echo "finding: App Router TypeScript project without typedRoutes enabled in $cfg (stable since Next 15.5)" >&2; fail=1; }
  fi
fi
if grep -rhoE 'NEXT_PUBLIC_[A-Z0-9_]*(SECRET|TOKEN|PASSWORD|PRIVATE_KEY|API_KEY)[A-Z0-9_]*' --include='*.ts' --include='*.tsx' --include='*.js' --include='*.env*' . --exclude-dir=node_modules 2>/dev/null | sort -u | grep -q .; then
  echo "FAIL: secret-named NEXT_PUBLIC_ variable(s) present; NEXT_PUBLIC_ values ship to the browser:" >&2
  grep -rhoE 'NEXT_PUBLIC_[A-Z0-9_]*(SECRET|TOKEN|PASSWORD|PRIVATE_KEY|API_KEY)[A-Z0-9_]*' --include='*.ts' --include='*.tsx' --include='*.js' --include='*.env*' . --exclude-dir=node_modules 2>/dev/null | sort -u >&2
  fail=1
fi
actions="$(grep -rl '"use server"\|'"'"'use server'"'"'' --include='*.ts' --include='*.tsx' --include='*.js' app src lib 2>/dev/null | sort -u)"
if [ -n "$actions" ]; then
  for f in $actions; do
    grep -qE 'auth\(|getServerSession|currentUser|verifySession|requireAuth|requireUser' "$f" || { echo "finding: Server Action file $f shows no auth check (actions are public POST endpoints)" >&2; fail=1; }
    grep -qE 'zod|\.parse\(|validate|schema' "$f" || { echo "finding: Server Action file $f shows no input validation signal" >&2; fail=1; }
  done
else
  echo "note: no Server Action files found (stated)"
fi
all_hdr="$(cat next.config.* middleware.* src/middleware.* 2>/dev/null)"
for h in Content-Security-Policy Strict-Transport-Security X-Content-Type-Options Referrer-Policy; do
  echo "$all_hdr" | grep -q "$h" || { echo "finding: security header $h not set in next.config headers() or middleware" >&2; fail=1; }
done
mw="$(ls middleware.* src/middleware.* 2>/dev/null | head -1)"
if [ -n "$mw" ] && grep -qE 'auth|session' "$mw"; then
  if ! grep -rqE 'auth\(|getServerSession|requireAuth|verifySession' --include='*.ts' --include='*.tsx' app src/app src/lib lib 2>/dev/null; then
    echo "finding: auth signals appear only in $mw and nowhere in routes, layouts, or actions; middleware-only auth is the CVE-2025-29927 failure pattern" >&2; fail=1
  fi
fi
exit "$fail"
