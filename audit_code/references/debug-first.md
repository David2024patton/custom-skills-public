# Debug-first contract (all languages)
Checked against: the language references in this skill (Oct 2026).

Read after the language reference. This is the language-neutral spec each module must satisfy.

## Minimum instrumentation per module

| Requirement | Rust | Go | Flutter/Dart | Mojo |
|---|---|---|---|---|
| Logger | `tracing` (`target = module_path!()`) | `log/slog` child logger with `"module"` attr | `package:logging` `Logger('feature.module')` | stdlib logger if present, else thin `log.mojo` wrapper |
| Runtime level | `RUST_LOG=my_crate::mod=debug` | `LOG_LEVEL=debug` env -> `slog.LevelVar` | `--dart-define=LOG_LEVEL=FINE` | `-D MOJO_DEBUG` compile flag + env var read at startup |
| Op correlation | `#[instrument]` / spans | ctx carries `request_id`, `logger.With(...)` | `Logger` name + id in message map | explicit `op_id` arg |
| Crash capture | `std::panic::set_hook` | `defer recover()` in goroutine wrapper + `main` | `FlutterError.onError`, `PlatformDispatcher.onError`, `runZonedGuarded` | top-level `try/except` in `main` |
| Debug asserts | `debug_assert!` | explicit `if debug {}` checks / build tag `debug` | `assert()` | `debug_assert` |
| Log capture in tests | `tracing-test` or custom `MakeWriter` | `slog.NewJSONHandler(&buf, ...)` | `Logger.root.onRecord` into list | wrapper writes to injectable sink |

## What to log (and not)

Log: module start/stop, config loaded (redacted), each public function's entry and result summary at DEBUG, each external call with duration, each retry with attempt number, each error with full cause chain, each state transition.

Never log: passwords, tokens, API keys, session cookies, full request/response bodies, card numbers, emails/phones, raw user content. Redact in the logger layer (field-name denylist: `password`, `token`, `secret`, `authorization`, `api_key`, `cookie`). Prefer logging IDs and sizes over contents.

## Debug self-test template (adapt per language)

1. Configure the logger to write to an in-memory buffer at DEBUG.
2. Call the module's public function on a failure path (bad input).
3. Assert: an ERROR/WARN record exists, it includes the module name and operation ID, and it includes the cause.
4. Call with an input containing a fake secret (`"sk-test-123"`); assert the buffer does **not** contain it.
5. Assert that at INFO level the DEBUG lines are absent (level switch works).

## Per-module checklist for the audit (vector 6)

- [ ] Logger created, named after the module
- [ ] Entry/exit/error boundaries logged
- [ ] External calls timed and logged
- [ ] Level switch documented and tested
- [ ] Crash/panic capture installed at the entry point
- [ ] No secrets/PII in logs (test proves it)
- [ ] Debug assertions present for invariants
- [ ] Real log excerpt captured from a run for the final report

## Capturing the excerpt for the final report

Run the program or a test with debug on and save the output (`2>&1 | tee /tmp/debug_run.log`), then paste 10-30 relevant lines: one success path, one failure path. If the code cannot run in the environment (e.g., Flutter without a device), say so, and use the test-captured log output instead.
