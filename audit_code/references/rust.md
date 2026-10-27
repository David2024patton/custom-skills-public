# Rust
Checked against: Rust stable, 2021/2024 editions (Oct 2026).

## Debug instrumentation (BUILD)

Dependencies: `tracing`, `tracing-subscriber` (features `env-filter`, `json` optional), `anyhow`/`thiserror` for error chains.

```rust
// logging.rs - call once from main()
pub fn init() {
    use tracing_subscriber::{fmt, EnvFilter};
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new(if cfg!(debug_assertions) { "debug" } else { "info" }));
    fmt().with_env_filter(filter).with_target(true).with_thread_ids(true).init();
    std::panic::set_hook(Box::new(|info| {
        tracing::error!(panic = %info, backtrace = %std::backtrace::Backtrace::force_capture(), "panic");
    }));
}

// per module
use tracing::{debug, error, info, instrument, warn};

#[instrument(skip(secret_arg), err)]       // logs args, span, and Err results
pub async fn fetch(url: &str, secret_arg: &Token) -> Result<Body, FetchError> { ... }
```

Rules: `#[instrument(skip(...))]` any arg holding secrets or large data; use `err` to log returned errors; use `debug_assert!` for invariants; wrap errors with context (`.context("while parsing config")`) so the chain is logged; library crates emit tracing events only and never install a subscriber. Run with `RUST_LOG=my_crate=debug,hyper=warn RUST_BACKTRACE=1`.

Debug self-test: use `tracing-test` (`#[traced_test]`, `logs_contain("...")`) or a custom `MakeWriter` into a `Mutex<Vec<u8>>`.

## Gates (run in this order)

```bash
cargo fmt --all -- --check
cargo clippy --all-targets --all-features -- -D warnings
cargo build --all-targets --all-features
cargo test --all-features
cargo test --doc
```

Extras when relevant:
- `cargo clippy -- -W clippy::pedantic -W clippy::unwrap_used -W clippy::expect_used -W clippy::panic -W clippy::todo -W clippy::unimplemented -W clippy::dbg_macro` for a hostile lint pass (review output; do not blindly silence).
- `cargo audit` (RustSec) and `cargo deny check` (licenses, bans, advisories) if installed or `deny.toml` exists.
- `cargo miri test` (nightly) for any `unsafe`; or sanitizers: `RUSTFLAGS="-Zsanitizer=address" cargo +nightly test --target x86_64-unknown-linux-gnu`; `thread` sanitizer for data races.
- Concurrency models: `loom` for custom sync primitives. Async: look for blocking calls inside async fns, holding `MutexGuard` across `.await`, unbounded channels, dropped `JoinHandle`s.
- Fuzz parsers: `cargo fuzz run <target> -- -max_total_time=60`. Property tests: `proptest`.
- Coverage: `cargo llvm-cov --summary-only`. Unused deps: `cargo machete` or `cargo udeps` (nightly).
- Feature matrix: `cargo hack check --feature-powerset` if features exist. MSRV: `cargo msrv verify` if declared.
- Benchmarks for perf claims: `cargo bench` / `criterion`.

## Hallucination traps

- Crate APIs change across majors (`tokio`, `axum` 0.6 -> 0.7, `reqwest`, `sqlx`, `clap` 3 -> 4, `rand` 0.8 -> 0.9). Check the version in `Cargo.lock` and read the docs for it: `cargo doc --open`, or look inside `~/.cargo/registry/src/*/<crate>-<ver>/`.
- Invented feature flags: confirm in the crate's `Cargo.toml` `[features]`.
- Non-existent trait methods or wrong trait imports (compile will tell: never skip build).
- Edition-specific syntax (let-chains, async closures) needs a recent toolchain: check `rust-toolchain.toml`.

## Rust audit checklist

- `unwrap()`/`expect()`/indexing/slicing/`as` casts/integer overflow/`unreachable!` on runtime-fallible paths; `let _ = fallible()`; `.ok()` discarding errors.
- `unsafe` blocks: each needs a `// SAFETY:` comment justifying invariants; check FFI lifetimes, aliasing, uninit memory, `Send`/`Sync` impls.
- Async: cancellation safety, `select!` dropping futures mid-operation, spawn without join/shutdown path, blocking in async, lock across await.
- Resource: unbounded `mpsc::unbounded_channel`, `Vec`/`HashMap` growth from user input, missing request body limits and timeouts.
- Security: `Command::new` with user input, path traversal (`Path::join` with absolute user path), SQL via `format!`, `serde` deserialization of untrusted data without size limits, `#[derive(Debug)]` on types containing secrets (use `secrecy::Secret`).
- API: `pub` surface larger than needed, missing `#[must_use]`, errors as `String`, breaking semver changes (`cargo semver-checks`).
