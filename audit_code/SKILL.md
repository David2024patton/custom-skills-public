---
name: audit_code
description: Hostile self-review, debug-first instrumentation, and verification gates for code written in Mojo, Rust, Go, Flutter/Dart, or JavaScript/TypeScript. Use when writing or modifying code in any of these languages (BUILD mode - bake logging/debug hooks into every module from the start), and when asked to review, critique, audit, red-team, harden, or "be your own worst critic" on code just written (AUDIT mode - evidence-based findings, fix loop, linters, tests, sanitizers, proof of execution). Also use before declaring any Mojo/Rust/Go/Flutter/Web task done.
author: David Patton
license: MIT
---

# audit_code (Mojo / Rust / Go / Flutter / Web)

Two modes, one contract: **nothing is "done" until it has debugging built in, passes every gate for its language, and survived a hostile review with evidence.**

- **BUILD mode** - applies while writing code. Instrument first, code second.
- **AUDIT mode** - applies after code exists (or when the user asks for critique). Attack the real diff, fix CRITICAL/HIGH, prove it.

Run both for any non-trivial task: BUILD while writing, AUDIT before reporting back.

## Step 0 - Detect the stack

Run `bash scripts/detect_stack.sh [project_dir]`, where `scripts/` is the scripts folder inside this skill's own directory, wherever the skill is installed. Never assume an absolute install path; the skill must work on any machine it is copied to. It prints which of Mojo, Rust, Go, Flutter, Web are present (by `*.mojo`/`🔥`/`pixi.toml`, `Cargo.toml`, `go.mod`, `pubspec.yaml`, `package.json`) and which toolchains are installed.

Then read the reference file for **every detected language** (a repo may be polyglot, e.g. Flutter app + Go backend + Rust core):

| Language | Reference |
|---|---|
| Rust | `references/rust.md` |
| Go | `references/go.md` |
| Flutter / Dart | `references/flutter.md` |
| Mojo | `references/mojo.md` |
| Web (JS/TS) | `references/web.md` |

Each reference has: debug-instrumentation pattern, exact lint/format/build/test commands, race/leak/sanitizer tooling, security scanners, language-specific hallucination traps, and a per-language audit checklist. For the cross-language debug contract, also read `references/debug-first.md`. Each reference carries a "Checked against" stamp (the toolchain versions its facts were verified on). If the project under audit uses a NEWER toolchain than a reference's stamp, say so in the report's residual risk: that reference may be stale, and its version-specific traps and flags get re-verified against the installed toolchain before use.

If a toolchain is missing, try to install it (rustup, go tarball, flutter SDK, pixi/magic for Mojo). If that is impossible, mark every gate for that language `NOT RUN` in the final report. Never imply it passed.

## BUILD mode - Debug-first rules (apply from the first file)

Every module, package, widget, or service created must ship with its own debugging. Do this *before* the business logic, not after.

1. **One logger per module**, named after the module path, created at the top of the file/package. Use the language's structured logger (see references). No bare `print`/`println!`/`fmt.Println` in production paths.
2. **Log at boundaries**: function entry/exit for public APIs (inputs sanitized, outputs summarized), every error path (with cause chain), every external call (network, disk, DB, FFI, subprocess) with duration, and state transitions.
3. **Levels**: ERROR = failed operation, WARN = recovered/degraded, INFO = lifecycle and business events, DEBUG = inputs/outputs/branching, TRACE = per-iteration detail. Default INFO in release, DEBUG in debug builds.
4. **Runtime switch, zero rebuild where possible**: log level controlled by env var or flag (`RUST_LOG`, `LOG_LEVEL`, `--dart-define=LOG_LEVEL=FINE`, `-D MOJO_DEBUG`), documented in the module header or README.
5. **Never log secrets or PII**: tokens, passwords, keys, full request bodies, user emails. Redact at the logger, not at call sites.
6. **Correlation**: carry a request/operation ID through logs (`tracing` spans, `context.Context` + slog attrs, logger name + ID in Dart, explicit arg in Mojo).
7. **Fail loud in debug, degrade gracefully in release**: debug builds enable assertions (`debug_assert!`, `assert`, Dart `assert`, Mojo `debug_assert`), crash hooks that print context and stack, and invariant checks. Release builds keep error handling but drop expensive checks.
8. **Global crash capture** at the entry point: Rust panic hook, Go `recover` in goroutine wrappers and `main`, Flutter `FlutterError.onError` + `PlatformDispatcher.onError` + `runZonedGuarded`, Mojo top-level `try/except` in `main` printing the error chain.
9. **Debug self-test**: add a small test proving the logging works (captures log output, asserts the expected line appears on an error path and that a secret does NOT appear). A debug facility with no test is assumed broken.
10. **Debug evidence at the end**: in the final report, include a short real log excerpt (from an actual run) showing the instrumentation firing on a success path and a failure path.

Module header checklist (3-line comment atop each new module): logger name, how to raise verbosity, main failure modes.

## AUDIT mode - Hostile review

### Persona and rules
You are a hostile Principal Staff Engineer and red-team security auditor reviewing a pull request from an untrusted contractor. You did not write this code and gain nothing from it shipping.

- Review the **real artifact**: run `git status` and `git diff <base>...HEAD` (plus unstaged changes), re-read every changed file in full, plus callers, callees, tests, config.
- No praise, no summaries of what the code does.
- Every finding needs **evidence**: `file:line`, snippet, and a failing command/test or a concrete triggering input/sequence. No evidence -> label `[UNVERIFIED]` and name the check that would confirm it. Never inflate severity.
- A clean vector is reported as `No findings - checked: <what was run/inspected>`. Do not invent problems.

### 0. Requirements trace
Turn the original task into a numbered acceptance-criteria checklist (include implied ones: backward compat, performance, docs, and the BUILD-mode debug hooks). Mark each MET / PARTIAL / MISSING with evidence. PARTIAL/MISSING are findings.

### 1-6. Vectors
1. **Laziness and hallucination**: TODO/FIXME/XXX, stubs (`todo!()`, `unimplemented!()`, `panic("not implemented")`, `UnimplementedError`, `pass`), mock data on production paths, fake success responses, commented-out code. Verify every import, method, flag, and package exists at the **pinned version** (lockfile, `cargo doc`, `go doc`, pub.dev docs, Mojo stdlib source/docs). See each reference's "hallucination traps".
2. **Failure and edge cases**: nil/null/empty/zero/negative, huge input, malformed encodings, unicode, timeouts, partial failure, retries/idempotency, concurrency, ordering, clock/timezone. Swallowed errors (`_ = err`, `let _ =`, `.ok()`, empty `catch`/`except`, `unwrap()` on fallible runtime paths). Leaks (goroutines, tasks, streams, controllers, subscriptions, file handles), unbounded queues/caches, deadlocks, data races. Durability writes are never fire-and-forget: a write whose loss corrupts state (persistence, queues, billing, audit logs) must surface its errors to the caller, and a corrupt state file must fail loud and be preserved, never silently overwritten.
   - **Lifecycle sweep**: for everything the code issues or accumulates (sessions, tokens, pairings, cache entries, queued tasks, subscriptions), ask three questions: does it expire or get evicted, does every size cap have a recovery path (a capped collection with no expiry is a permanent lockout waiting for its 65th entry), and is every nonce/counter unique within its full domain (per direction, per peer, per epoch), with replay rejected.
3. **Security and trust boundaries**: injection (SQL/command/path/template/SSRF/XSS/deserialization), unvalidated input at every boundary, authN/authZ/IDOR, client-only checks, hardcoded secrets, secrets/PII in logs, internal errors leaked to callers, insecure defaults, weak crypto, new/vulnerable dependencies, `unsafe`/FFI/`dart:ffi`/Mojo `UnsafePointer` misuse.
   - **Tenancy sweep (multi-tenant code)**: cross-tenant data leaks are the highest-impact bug class in a multi-tenant system and a diff review misses them by default. Grep every data query, handler, and background job touched by the change and confirm each one is scoped to the caller's tenant and checks membership or ownership server-side. A query that loads by ID without a tenant/owner condition is a CRITICAL even if the UI never links to it. Confirm log lines carry the tenant and actor IDs, or an isolation bug cannot be traced after the fact.
   - **Secret history scan**: the diff is not the whole attack surface. Run a secret scanner (gitleaks or trufflehog) over the FULL repository history, not just the change; if neither is installed, run the pattern grep in the verification gates and report the scan as partial. A live credential committed in any earlier commit is a CRITICAL finding with a rotation instruction, even when the current tree is clean.
   - **Secrets travel**: check the other places secrets ride: process command lines (argv is readable by every process on the box via /proc; pass secrets by env or file, never argv), URLs and query strings, environment dumps in error reports, and child-process environments. Where the diff spawns a subprocess with a credential, a test should assert the secret and its flag appear in neither argv nor logs.
   - **Validation ends at the final target**: any check on a URL, host, scheme, or version must still hold after redirects and resolution, not just at the first hop. Redirect chains are capped, scheme downgrades (https to http) refused, and the validated value is the one actually used. The same rule covers version logic: a version string that cannot be parsed fails CLOSED (refused), never waved through a downgrade or freshness check.
   - **Freshness, not just authenticity**: a signature proves who signed, not that the thing is current. Any signed channel (update manifests, config, licenses, tokens with embedded versions) needs a monotonic freshness check (a stored high-water mark of the newest version seen) or a captured old-but-valid artifact replays forever. Missing freshness next to a signature is a finding.
4. **Architecture and maintainability**: compare against 2-3 neighboring files for layering, naming, error-handling and logging conventions; duplicated logic that already exists; god-files/functions; breaking public API/schema/migration changes; missing rollback.
   - **Singleton and process-mode scoping**: anything that grabs a shared singleton resource (stdin, a prompt, a fixed port, a signal handler, global mutable state) must declare which process modes it may run in (one-shot CLI, interactive TUI, server, test) and fail closed in every other mode. An interactive helper that leaks into a server process will prompt the wrong human, eat another component's input, or hang the run; absence in the wrong modes must be by construction, and pinned by a test where practical.
5. **Proof of execution**: build, format check, lint, type-check, and the full relevant test suite were run **in this session** with output shown. Anything not run is a finding. Audit the tests themselves: do they assert behavior, cover failure paths, and go red when a key line is mutated? (Mutate one line, confirm failure, restore.)
6. **Operability and debuggability**: BUILD-mode rules honored per module (logger present, boundaries logged, levels sane, runtime switch documented, crash capture installed, no secrets logged, debug self-test exists). Timeouts, config, docs, safe deploy/rollback.

### Severity
- `[CRITICAL]` exploitable security hole, data loss/corruption, crash/hang on a normal path, missing acceptance criterion, build or tests failing.
- `[HIGH]` wrong behavior on realistic edge cases, race/leak, swallowed error hiding failures, hallucinated API, untested critical path, breaking change, module with no debug instrumentation.
- `[MEDIUM]` convention drift, weak tests, thin observability, avoidable complexity, off-hot-path perf.
- `[NIT]` style, naming, comments.

### Finding format
```
[SEVERITY][vector #] path/file.ext:LINE - what is wrong
  Evidence: <command output / failing input / code path>
  Impact:   <what breaks, for whom>
  Fix:      <specific change>
```

### Fix loop (no permission needed for CRITICAL and HIGH)
1. Fix in severity order, one finding at a time, **smallest possible diff**. No drive-by refactors; no new dependencies without stating why.
2. For each fix, add or update a test that **fails before and passes after**. Show both runs.
3. After each fix, rerun the full gate set. If a fix breaks something, revert it and report the conflict; do not stack patches.
4. List MEDIUM/NIT; fix only if trivial and safe. Ask before changing public APIs, schemas, or scope. Also stop and ask when a fix would change user-visible behavior on a live system (wording, defaults, flows, timing, what data is shown to whom), even when the fix itself is small: restoring the specified behavior is a fix, inventing new behavior is a product decision.
5. **Second pass**: re-run `git diff`, audit your own fixes with the same hostility. Repeat until a pass yields no new CRITICAL/HIGH, or 3 passes are done.
6. **New-surface inventory (part of every second pass)**: fixes ship with less review than the code they fix, and they add surface. List everything the whole change ADDS: routes/endpoints, CLI commands and flags, process modes, file formats, config keys, background jobs. For each item, ask out loud: what authenticates it, what is its lifecycle (expiry, cap, recovery), what singleton resources does it touch and in which process modes, and what happens on malformed input. Re-grep the route/registration tables rather than trusting the diff view; an endpoint added by a fix and missed by the inventory is exactly how unauthenticated surface ships.

### Verification gates
Run `bash scripts/run_checks.sh [project_dir]` (the scripts folder inside this skill's own directory). It runs every applicable gate for every detected language, prints a PASS / FAIL / NOT RUN table, saves full logs to `/tmp/audit_logs`, and exits non-zero on any FAIL. It is a floor, not a ceiling: also run the deeper tools in the references (race detector, sanitizers, miri, fuzzing, vuln scanners) where relevant to the change. If the project has its own `Makefile`/CI/pixi tasks, run those too and let them win on conflict.

One gate is not per-language: the **secret history scan**. Run `gitleaks detect --source <repo>` (or trufflehog) over the full history. If no scanner is installed, fall back to a pattern grep over tracked files and history (`git grep -I -E '(password|passwd|secret|api[_-]?key|token)\s*[:=]' $(git rev-list --all) -- .` plus provider key shapes like `AKIA`, `sk-`, `ghp_`), and report the scan as PARTIAL with the pattern list named. A scan that did not run is NOT RUN, never clean.

**Version currency (every audit, not optional).** Being behind on versions is a security posture, not housekeeping: a pinned toolchain with known vulnerabilities fails the audit even when the project's own code is clean.
- **Inventory the pins**: language toolchains (go.mod `go` and `toolchain` lines, rust-toolchain.toml, .nvmrc and package.json `engines`, pubspec SDK constraint, Flutter version files), base images in Dockerfiles, and setup-action versions in CI. Print pinned vs latest patch in that release line, side by side, in the report. Currency is checked against the vendor's own release channel (release page/feed, package manager), never from memory.
- **Severity**: a pin behind a patch release that carries security fixes is HIGH (this is exactly what govulncheck flags when the Go toolchain itself is stale); a pin behind on features only is MEDIUM. The fix is bumping the pin (go.mod toolchain line, CI setup version, Dockerfile tag), not pinning harder.
- **Consistency**: the same toolchain version must agree everywhere it is named: module file, CI workflows, Dockerfiles, and the environment actually running the gates. Drift between them is a finding, because each surface silently tests a different program.
- **Gate tools are versioned too**: print every gate tool's own version in the gate table (linter, vuln scanner, secret scanner). A scanner built against an older toolchain than the code it scans can fail to even parse the target (govulncheck built with an older Go cannot scan newer Go code): rebuild or reinstall the tool with a toolchain at least as new as the target before trusting its output, or its result is NOT RUN.
- **NOT RUN has a cost**: before any gate may be reported NOT RUN for a missing tool, attempt the install at a pinned version (record the exact install command and version in the report). A gate that is NOT RUN in two consecutive audits of the same project is itself a finding (MEDIUM, against the environment), named in the verdict area, not a footnote that repeats forever.

Gate set per language (flags and extras in references):
- **Rust**: `cargo fmt --check`, `cargo clippy --all-targets --all-features -- -D warnings`, `cargo build`, `cargo test`, plus `cargo audit`/`deny`, `miri`/sanitizers for `unsafe`.
- **Go**: `gofmt -l`, `go vet`, `golangci-lint run`, `go build`, `go test -race -count=1 -shuffle=on`, `govulncheck`.
- **Flutter**: `dart format --set-exit-if-changed`, `flutter analyze`, `flutter test`, plus `integration_test` and a debug build smoke when UI or platform code changed. Web targets also gate on `flutter build web --no-web-resources-cdn` and a FontManifest.json check that the text font is bundled (see references/flutter.md).
- **Mojo**: `mojo format`, `mojo build -g -D MOJO_DEBUG` (warnings reviewed), `mojo test`, sanitizer run if available. Mojo has no dedicated linter and its flags change fast: confirm with `mojo --help` first and say so in the report.
- **Web**: install from the lockfile (`npm ci`), `tsc --noEmit` when TypeScript, ESLint when configured, the project's test script, the production build, and `npm audit --audit-level=high` (see references/web.md).

## Final report (always)
0. **Verdict, one line, first**: SHIP, SHIP AFTER FIXES (name them), or DO NOT SHIP (name the blocker). The reader should never have to dig for the answer.
1. Acceptance-criteria table (MET/PARTIAL/MISSING).
2. Findings fixed, with before/after test evidence.
3. Findings remaining (MEDIUM/NIT/UNVERIFIED) and why.
4. Commands run with exact pass/fail results (paste the `run_checks.sh` table).
5. Debug evidence: real log excerpt showing instrumentation on a success and a failure path.
6. Residual risk: what could NOT be verified (no staging, no load test, missing toolchain, device-only behavior) and what a human should check before merge. Never write "verified" for anything not executed.
7. **Claims ledger**: list every factual claim the report makes about behavior outside this repo (it ships, it sends, it saves, it charges, it renders on the device) and the evidence class behind each: EXECUTED HERE (ran in this session), EXECUTED ON TARGET (ran on the real device/server/production route), PROVIDER RECORD (checked the vendor's own delivery/status record, not just the API's acceptance), or UNVERIFIED. The expensive failures are claims, not code: a build called shippable that crashes on the real device, an endpoint that passes tests but 404s on the live route, a message the API accepted but the carrier never delivered. Any claim that can be checked against the live system or the provider's record MUST be, before it is stated as fact; otherwise it goes in the ledger as UNVERIFIED.
8. **Carry-over and aging**: if a previous audit report for this project exists (in the repo, its docs, or provided), diff against it. Every still-open finding is listed with its age (days open, and how many audits it has survived). A CRITICAL or HIGH open across two or more audits is named in the verdict line itself; repeats must get louder, not blend into the remaining list. Closed-since-last-time findings are listed as closed, with the closing evidence.

## Tips
- Best results: run AUDIT mode in a fresh context or a separate subagent given only the task description and the diff; use a different model than the author if possible.
- For large diffs, split into narrow reviewers (security, concurrency, requirements) and merge findings.
- Read `AGENTS.md`/`CLAUDE.md`/CONTRIBUTING first; its conventions define vector 4.
