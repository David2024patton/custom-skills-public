#!/usr/bin/env bash
# PURPOSE: Print the standard Prisma diagnostic pattern.
# STEPS:
#   1. Print the schema-side pattern: datasource url through
#      env("...") (never a literal credential) and a generator
#      block with an explicit output.
#   2. Print the client-side pattern: PrismaClient created with
#      query/error/warn log events enabled, those events forwarded
#      into the project's diag channel, so database refusals and
#      errors surface through the same seam as everything else.
#   3. The pattern's rules: log the event and the model, not query
#      values (parameters may carry secrets or personal data);
#      every refusal path still emits through diag exactly once.
# NOTES:
#   - For environment trouble, `prisma debug` prints CLI
#     environment info for a bug report; it changes nothing.
# PROHIBITION (every script in this set): no migrate, no db push,
# pull, execute, or seed, no studio. Nothing touches a live
# database, ever.
# MODIFY PER PROJECT: the diag module is the project's own (see
# the javascript/typescript debug-add patterns); only its sink
# changes per target.
# USAGE: prisma/debug-add.sh [dir]
# EXIT: 0.
set -u
cd "${1:-.}" 2>/dev/null || true
cat <<'EOF'
PATTERN:
  // prisma/schema.prisma (schema side)
  // datasource db {
  //   provider = "postgresql"
  //   url      = env("DATABASE_URL")   // never a literal credential
  // }
  // generator client {
  //   provider = "prisma-client-js"
  //   output   = "../generated/client" // explicit, reviewable output
  // }

  // lib/prisma.ts (client side): forward Prisma log events to diag.
  // const prisma = new PrismaClient({
  //   log: [
  //     { emit: 'event', level: 'query' },
  //     { emit: 'event', level: 'error' },
  //     { emit: 'event', level: 'warn' },
  //   ],
  // });
  // prisma.$on('error', (e) => diag.emit('prisma-error', { message: e.message }));
  // prisma.$on('warn',  (e) => diag.emit('prisma-warn',  { message: e.message }));
  Every refusal path still calls diag.emit('refusal', {why}) once.
EOF
