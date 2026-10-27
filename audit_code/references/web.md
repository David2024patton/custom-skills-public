# Web (JavaScript / TypeScript, React and friends)
Checked against: Node LTS, TypeScript 5, React 19, Vite 6/7 (Oct 2026).

For browser apps and Node services: Vite, webpack, Next, plain React, vanilla TS. Confirm the actual stack from `package.json` (scripts, dependencies, lockfile) before trusting any command below; let the project's own scripts win on conflict.

## Debug instrumentation (BUILD)

One tiny logger module per app, used everywhere; no bare `console.log` in shipped code (lint `no-console`, allow `warn`/`error` only if the project already does).

```ts
// src/lib/log.ts
type Level = 'debug' | 'info' | 'warn' | 'error';
const order: Record<Level, number> = { debug: 10, info: 20, warn: 30, error: 40 };
// Vite: import.meta.env.VITE_LOG_LEVEL. Next: process.env.NEXT_PUBLIC_LOG_LEVEL.
// Plain Node: process.env.LOG_LEVEL.
const active = order[(import.meta.env?.VITE_LOG_LEVEL ?? 'info') as Level] ?? 20;
const SECRET = /password|token|secret|authorization|api[-_]?key|cookie/i;
function scrub(fields: Record<string, unknown>) {
  const out: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(fields)) out[k] = SECRET.test(k) ? '[redacted]' : v;
  return out;
}
export function log(level: Level, module: string, msg: string, fields: Record<string, unknown> = {}) {
  if (order[level] < active) return;
  console[level === 'debug' ? 'log' : level](`[${level}] ${module}: ${msg}`, scrub(fields));
}
```

Rules: log at the same boundaries as every other language (public function entry/exit at debug, every error with its cause, every fetch with method, path, status, duration; never bodies, headers, or tokens). Carry an operation ID in the fields. In React, install an error boundary at the app root that logs the component stack and shows the user a plain recovery screen, never a raw error or a blank page; also hook `window.addEventListener('error')` and `'unhandledrejection'` into the logger so async failures are not silent. In Node services, the same logger writes JSON lines to stderr and a process-level `unhandledRejection`/`uncaughtException` handler logs and exits non-zero.

Debug self-test: unit test that sets the level to debug, calls a failing path, asserts the record was emitted with module and operation ID, and that a fake secret in the fields came out as `[redacted]`.

## Gates (in order)

```bash
npm ci                        # if a lockfile exists; else npm install, and say which
npx tsc --noEmit              # when TypeScript / tsconfig.json present
npx eslint .                  # when ESLint is configured; --max-warnings 0 for the hostile pass
npm test                      # the project's own test script (vitest/jest/node:test)
npm run build                 # the production build is a gate, not a courtesy
npm audit --audit-level=high  # needs network; if it cannot run, NOT RUN, never "clean"
```

Extras when relevant:
- Formatting: `npx prettier --check .` when Prettier is configured.
- Bundle honesty: read the build output sizes; a bundle that ballooned, a new heavy dependency, or a dev-only package in the production bundle is a finding. `npx vite-bundle-visualizer` or the framework equivalent when available.
- Test quality: same rule as every language; coverage on the changed files, failure paths asserted, one mutation check on a key line.
- E2E smoke when the change is user-facing: the project's Playwright/Cypress suite if present; if none, a scripted browser pass over the changed route counts, and its absence is reported under residual risk.

## Hallucination traps

- Invented or renamed package APIs are the norm, not the exception: React 19 removed and renamed things older code relied on, router and state libraries change APIs across majors (react-router, zustand, tanstack query), and Vite/Next config keys move between versions. Verify against the version pinned in the lockfile: read the package's own types in `node_modules/<pkg>` or its docs for that version. `tsc` is the first arbiter; a green type check with `any` smeared over the boundary proves nothing.
- `skipLibCheck: true` hides real type errors in dependencies; note it in the report when present.
- Phantom dependencies: importing a package that only arrives transitively. Check it is a direct dependency in `package.json`.
- Environment variables in browser builds are PUBLIC: anything in a `VITE_`/`NEXT_PUBLIC_` var or inlined at build time ships to every visitor. A secret there is a CRITICAL, not a config nit.
- Node vs browser globals: code that type checks under one `lib`/`types` config and explodes in the other runtime (`Buffer`, `window`, `process.env` in the browser).

## Web audit checklist

- Security: `dangerouslySetInnerHTML` / `innerHTML` with unsanitized data (XSS), user input into `href`/`src` (`javascript:` URLs), tokens in `localStorage` on origins that run third-party scripts, secrets in client env vars, source maps shipping full source to production without a decision, postMessage without origin checks, open redirects from query params.
- Async and state: missing `AbortController` on fetches (setState after unmount, races where a slow earlier response overwrites a newer one), effect dependency lies (eslint exhaustive-deps disabled), stale closures, list keys from array indexes on reorderable data, promises created in render.
- Error UX: fetches with no timeout or error state, `.catch(() => {})` swallowing, error screens that print the raw exception to the user, loading states that can spin forever.
- Correctness: floating point money, date/timezone handling via local `Date` parsing of server strings, `==` coercion surprises, JSON parsed without validation at the trust boundary (parse, then check shape; a cast is not a check).
- Architecture: business logic inside components, direct DOM manipulation fighting the renderer, duplicated fetch logic instead of the project's data layer, god components.
