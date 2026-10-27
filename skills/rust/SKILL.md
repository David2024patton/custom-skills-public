---
name: rust
description: "Use when writing Rust: crates, patterns, and tooling."
version: 1.0.0
license: MIT
hermes:
 tags:
 - rust
 - cargo
 - memory-safety
 - systems-programming
 - ffi
 - async
 - quality-gates
 - supply-chain-security
---

# Rust: production-grade engineering

Stand-alone skill for an agent that programs well and must write, review, test,
or harden Rust on the AlphaFlux pipeline (roles: builder, tester, security). Two
rules govern everything below: re-verify anything version-shaped the moment you
cite it, and run the section 9 gates before reporting Rust work done.

## 0. Verified toolchain baseline (checked 2026-10-22)

Read from primary sources that date; the train moves every six weeks, so
re-check before citing anything in a report.

- Stable is Rust 1.99.1 (2026-10-15), on the six week train (beta 6 weeks behind,
 nightly each night); 1.99.0 shipped 2026-10-01. Release notes:
 https://doc.rust-lang.org/stable/releases.html
- Edition 2024 stable since Rust 1.85 (2025-02-20); new `cargo new` projects
 declare `edition = "2024"`. Confirm it in the generated Cargo.toml.
- `edition = "2024"` implies `resolver = "3"` (MSRV-aware, since 1.84); a virtual
 workspace must set `resolver` in `[workspace]` itself.
- Let chains in `if` / `while` stabilized in 1.88 and are 2024-only, since they
 depend on the `if let` rescoping change.
- Async closures stabilized in 1.85, `async fn` in traits since 1.75, C-ABI
 variadic definitions since 1.99.0.
- `LazyLock` / `LazyCell` since 1.80, `OnceLock` / `OnceCell` since 1.70: prefer
 them over `lazy_static!` and `once_cell`.
- `gen` blocks are unstable and `gen` is reserved in 2024, so rename `gen`
 identifiers or write `r#gen`.

No crate versions appear here on purpose: resolve them with `cargo add <crate>`
(Cargo writes the current version into Cargo.toml) or read https://docs.rs. If a
report must quote one, write "verify current" unless you just read Cargo.lock.

## 1. Toolchain setup and reproducibility

Never build against whatever rustc is on PATH. Pin the toolchain per repo so
builder, tester, and security profiles compile identical artifacts.

```bash
# One-time host setup
rustup toolchain install stable && rustup default stable
rustup component add rustfmt clippy

# Per-repo pinning (preferred): commit rust-toolchain.toml, then these commands
# pick the pinned toolchain automatically.
cargo check --workspace --all-targets
cargo clippy --workspace --all-targets -- -D warnings
```

```toml
# rust-toolchain.toml, committed at the repo root
[toolchain]
channel = "1.99.1" # exact pin for reproducible CI; bump deliberately
components = ["rustfmt", "clippy", "rust-src"]
profile = "minimal"
# targets = ["x86_64-unknown-linux-musl"]
```

`channel = "stable"` means tracking the moving edge; say so in the PR. Exact pins
break only when you bump them. Everyday commands:

```bash
rustc --version --verbose # compiler, commit hash, host triple
cargo metadata --format-version 1 --no-deps # machine-readable workspace graph
cargo tree -e features --workspace # who enables which feature
cargo tree -d # duplicate versions in the lockfile
cargo update --workspace --dry-run # what a lockfile bump would change
```

## 2. Project layout: modules first

David's standing rule is modular design with a clear layout, and every feature
gets its own module. Promote a feature to its own crate when it gains its own
dependency surface or release cadence.

```text
alphafux-scanner/
 Cargo.toml # virtual workspace: members, resolver = "3"
 rust-toolchain.toml
 deny.toml # cargo-deny policy (section 9)
 crates/
 core/ # pure logic, no I/O: parsing, rules, scoring
 src/lib.rs
 tests/property.rs
 api/ # HTTP surface, depends on core
 src/lib.rs
 src/main.rs
 ffi/ # C ABI for iTaK Browser embedding, depends on core
 cli/ # thin operator binary, depends on core + api
 src/main.rs
 fuzz/fuzz_targets/ # cargo-fuzz targets, excluded from normal builds
 scripts/gates.sh # the one command CI and humans both run
```

```toml
# Root Cargo.toml (virtual workspace, so no [package] table here)
[workspace]
resolver = "3"
members = ["crates/*"]

[workspace.lints.clippy]
unwrap_used = "deny"
expect_used = "warn"
pedantic = "warn"

[workspace.lints.rust]
unsafe_code = "forbid" # lift per crate only where FFI or perf demands it
```

Members opt in with `[lints] workspace = true`, so policy lives in one place and
new crates inherit it. `unsafe_code = "forbid"` plus a deliberate
`#![allow(unsafe_code)]` in `crates/ffi` turns every unsafe block into a review
artifact: the security profile reads that allow list as its work queue.

## 3. Core language refresher

One sentence: each value has one owner, borrows are many-shared or one-exclusive,
and the borrow checker proves no use overlaps a conflicting borrow. Lifetimes,
traits, smart pointers, and `Send` / `Sync` are machinery for that proof.

```rust
fn main() {
 let mut s = String::from("alphafux");
 let r1 = &s;
 let r2 = &s;
 println!("{r1} {r2}"); // many shared borrows: fine
 let r3 = &mut s; // starts after r1 and r2 are last used (NLL)
 r3.push_str("-scan");
 println!("{r3}"); // one exclusive borrow: fine
 // println!("{r1}"); // fails: r1 outlives its usefulness
}
```

Lifetimes are the compiler's name for how long a reference may live, not runtime
objects. Elision covers single-input and `&self` cases; name lifetimes only when
the compiler asks.

```rust
// Explicit form; elision infers the same thing for two &str inputs.
fn longest<'a>(a: &'a str, b: &'a str) -> &'a str {
 if a.len() > b.len() { a } else { b }
}

// Elision covers `&self` too: a method returning &str borrows from &self.
fn main() {
 assert_eq!(longest("abc", "ab"), "abc");
}
```

Traits give static dispatch by default and dynamic dispatch when you ask. Reach
for `dyn` at real plugin boundaries only: one indirection, no inlining.

```rust
trait Shape {
 fn area(&self) -> f64;
 fn label(&self) -> &'static str { "shape" }
}

struct Square(f64);

impl Shape for Square {
 fn area(&self) -> f64 { self.0 * self.0 }
}

// Static dispatch: monomorphized per T.
fn area_of<T: Shape>(s: &T) -> f64 { s.area() }

// Dynamic dispatch: one vtable pointer, requires object safety.
fn report(shape: &dyn Shape) {
 println!("{}: {:.2}", shape.label(), shape.area());
}

fn main() {
 let shapes: Vec<Box<dyn Shape>> = vec![Box::new(Square(2.0))];
 for s in &shapes { report(s.as_ref()); }
 assert_eq!(area_of(&Square(2.0)), 4.0);
}
```

Enums plus `Result` and `?` replace exceptions; `?` converts through `From`, so
one error enum with `From` impls is the standard library-crate shape.

```rust
#[derive(Debug, PartialEq)]
enum ParseError { Empty, BadNumber, Overflow }

fn port(raw: &str) -> Result<u16, ParseError> {
 let t = raw.trim();
 if t.is_empty() { return Err(ParseError::Empty); }
 let v: u32 = t.parse().map_err(|_| ParseError::BadNumber)?;
 u16::try_from(v).map_err(|_| ParseError::Overflow)
}

fn main() {
 assert_eq!(port(" 8080 "), Ok(8080));
 assert_eq!(port("abc"), Err(ParseError::BadNumber));
 assert_eq!(port("70000"), Err(ParseError::Overflow));
}
```

Prefer iterators over index loops: `filter_map`, `zip`, `copied`, and
`collect::<Result<Vec<_>, _>>()` cover most aggregation shapes.

## 4. Edition 2024: what actually changed

Editions are opt-in and backwards compatible, so 2015, 2021, and 2024 crates
interoperate in one graph. Migrate with `cargo fix --edition`, then read the diff.

```bash
# From the crate root, on a clean tree
cargo fix --edition --allow-dirty # rewrites code for the next edition
# Then set edition = "2024" in Cargo.toml and rebuild
cargo check --workspace --all-targets
cargo test --workspace

# Diagnostic group that finds leftover incompatibilities
cargo clippy --workspace -- -W rust-2024-compatibility
```

What every builder, tester, and security reviewer must know:

1. **Return-position `impl Trait` captures all in-scope lifetimes by default.**
 Soundness fix: in edition 2021 the same signature failed with `E0700`.

```rust
// Edition 2024: compiles as written; the hidden iterator may borrow `data`.
fn copied(data: &[u8]) -> impl Iterator<Item = u8> {
 data.iter().copied()
}

```

2. **Let chains** interleave `let` patterns and boolean operands at the top level
 of `if` and `while`. 2024-only.

```rust
#[derive(Clone, Copy)]
enum Stage { Ready(u32), Busy }

fn ready_total(a: Option<Stage>, b: Option<Stage>, warm: bool) -> u32 {
 let mut total = 0;
 if let Some(Stage::Ready(x)) = a
 && let Some(Stage::Ready(y)) = b
 && warm
 {
 total = x + y;
 }
 total
}

fn main() {
 assert_eq!(ready_total(Some(Stage::Ready(2)), Some(Stage::Ready(3)), true), 5);
 assert_eq!(ready_total(Some(Stage::Ready(2)), None, true), 0);
}
```

3. **`unsafe extern` blocks are mandatory**: foreign declarations live in
 `unsafe extern "C" { ... }`, safe wrappers carry the proof.
4. **Unsafe attributes are mandatory**: `#[unsafe(no_mangle)]` and friends,
 since mistakes here corrupt the process.
5. **`unsafe_op_in_unsafe_fn` warns by default**: an `unsafe fn` body is no
 longer an implicit unsafe block.
6. **References to `static mut` deny by default**: use atomics, `Mutex`,
 `RwLock`, `OnceLock`, `LazyLock`, or raw borrows (`&raw const` / `&raw mut`).
7. **Never type fallback changed**, with `never_type_fallback_flowing_into_unsafe`
 at deny; `!`-dependent code may need an annotation.
8. **Tail expression and `if let` rescoping** change drop order; re-read tests
 that assert when destructors run.
9. **Resolver 3 is the default.** Set `package.rust-version` per crate so Cargo
 prefers dependencies that compile on your claimed toolchain.
10. **`gen` is reserved.** The fixer rewrites it to `r#gen`.

## 5. Unsafe code, FFI, and soundness

Unsafe does not disable the borrow checker. It adds four powers: dereference raw
pointers, call unsafe functions, access mutable statics, implement unsafe
traits. Everything else holds, and every `unsafe` block needs a `SAFETY:`
comment naming the caller's obligation.

```rust
use std::ffi::c_char;

// Edition 2024: the block itself is marked unsafe.
unsafe extern "C" {
 fn strlen(s: *const c_char) -> usize;
}

/// SAFETY: `s` must be non-null, NUL-terminated, and live for the whole call,
/// as C strlen requires.
pub unsafe fn c_str_len(s: *const c_char) -> usize {
 unsafe { strlen(s) }
}

// Edition 2024: unsafe attributes are explicit.
#[unsafe(no_mangle)]
pub extern "C" fn alphafux_abi_version() -> u32 {
 1
}
```

C-ABI variadic definitions are stable as of Rust 1.99.0: `unsafe extern "C" fn f
(mut args: ...)`, read with `VaList::next_arg::<T>()`, with the required argument
count in the SAFETY contract. Inside any `unsafe fn`, wrap each operation in its
own `unsafe { }` block: a raw read such as `*ptr.add(idx)` must name the caller's
length and validity contract where it happens.

Mutable globals: never take a reference to a `static mut`.

```rust
use std::sync::atomic::{AtomicU64, Ordering};

static VISITS: AtomicU64 = AtomicU64::new(0);

fn on_request() { VISITS.fetch_add(1, Ordering::Relaxed); }

fn report() -> u64 { VISITS.load(Ordering::Relaxed) }

fn main() {
 on_request();
 on_request();
 assert_eq!(report(), 2);
}
```

Manual memory stays rare: prefer `Vec`, `Box`, and iterators. When you need it,
`MaybeUninit<T>` defers initialization, `ManuallyDrop<T>` suppresses the drop,
and `Pin<P>` freezes an address so self-referential futures poll safely
(`Box::pin` for `'static`, `pin!` on the stack).

Unsafe review checklist (security profile): every block has a `SAFETY:`
comment; every FFI boundary states ownership, lifetime, nullability, and thread
assumptions; `#![forbid(unsafe_code)]` holds outside crates that opted out; no
`static mut` references; no `transmute` across differing validity invariants;
raw pointers never dereferenced after the owning allocation can be freed.

## 6. Concurrency: threads, shared state, async

`T: Send` means moving `T` to another thread is safe; `T: Sync` means `&T` can be
shared. A rejected move or spawn is a data race the compiler found: fix the type,
not the lint (`Rc` to `Arc`, `RefCell` to `Mutex`, thread-local state stays put).

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn upper_all(lines: Vec<String>) -> Vec<String> {
 let shared = Arc::new(Mutex::new(Vec::<String>::new()));
 let mut handles = Vec::new();

 for part in lines.chunks(64).map(|c| c.to_vec()) {
 let shared = Arc::clone(&shared);
 handles.push(thread::spawn(move || {
 // Lock scope stays tiny: lock, extend, drop.
 let mut guard = shared.lock().expect("poisoned by a panicked peer");
 guard.extend(part.into_iter().map(|l| l.to_uppercase()));
 }));
 }

 for h in handles { h.join().expect("worker panicked"); }
 Arc::try_unwrap(shared).expect("workers alive").into_inner().expect("poisoned")
}

fn main() {
 assert_eq!(upper_all(vec!["alpha".into(), "flux".into()]), vec!["ALPHA", "FLUX"]);
}
```

Two rules remove most production deadlocks: never hold a lock across an
`.await`, and never take two locks without a fixed global order. Release guards
before calling unknown code, since a panic under a lock poisons it for everyone.

Atomics serve flags, counters, and handoffs: `Relaxed` for counters with no
dependent data, `Acquire`/`Release` for publish-subscribe, `SeqCst` only for one
global order, `fetch_update` when read-modify-write must not lose increments.

Async Rust is structured concurrency on an executor: a future does nothing until
polled, and `tokio::spawn` (verify current tokio version with `cargo add tokio
--features full`) requires `Send + 'static`.

```rust
use tokio::sync::mpsc;
use tokio::time::{sleep, timeout, Duration};

// Losing branches are dropped cleanly; only select abandon-safe operations.
async fn wait_for_first(mut rx: mpsc::Receiver<u32>) -> u32 {
 tokio::select! {
 Some(v) = rx.recv() => v,
 _ = sleep(Duration::from_millis(250)) => 0,
 }
}

async fn bounded() -> Result<(), String> {
 timeout(Duration::from_millis(100), sleep(Duration::from_millis(10)))
 .await
 .map(|_| ())
 .map_err(|_| "timed out".to_string())
}

#[tokio::test]
async fn first_message_wins() {
 let (tx, rx) = mpsc::channel(4);
 tx.send(7).await.expect("receiver alive");
 assert_eq!(wait_for_first(rx).await, 7);
 assert_eq!(bounded().await, Ok(()));
}
```

Flag in review: `.await` under a `MutexGuard`; blocking calls (`std::fs`, heavy
CPU) in async tasks, which need `spawn_blocking`; `select!` branches that drop
partial writes; unbounded channels; and `!Send` futures reaching `tokio::spawn`
through an `Rc`. Every socket await needs a timeout, and every worker pool needs
a size you can justify.

## 7. Error handling, logging, operator-facing behavior

- Libraries: typed errors implementing `std::error::Error`, converted with `?`.
- Binaries: one top-level error type (or a context-chain crate from `cargo add`,
 verify current) plus actionable messages.
- Panics are for programmer bugs: `expect` with a real message on proved
 invariants. Never panic on user or network input, never unwind across FFI
 (catch at the boundary, or `panic = "abort"` after validating).
- David's simplicity bar makes error text the interface: what failed, what to do
 next, and an ID the operator can search in the docs.

```rust
use std::fmt;

#[derive(Debug)]
pub enum ScanError {
 BadRule { rule: String, detail: String },
 Io { path: String, source: std::io::Error },
}

impl fmt::Display for ScanError {
 fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
 match self {
 ScanError::BadRule { rule, detail } => {
 write!(f, "invalid rule {rule}: {detail}; fix the rule and rerun")
 }
 ScanError::Io { path, source } => {
 write!(f, "cannot read {path}: {source}; check permissions")
 }
 }
 }
}

```

Add `impl From<std::io::Error> for ScanError` (or derive it with `thiserror`,
verify current) so `?` keeps working in I/O paths. Use `tracing` in services and
a simple logger in small tools, both added with `cargo add`; log identifiers and
durations, never payloads, secrets, or PII, and give every record a `scan_id` or
`request_id` so one job can be followed end to end.

## 8. Testing: the tester profile's contract

Four layers run before merge: unit tests in the module, integration tests in
`tests/`, doctests that double as documentation, and property or fuzz tests for
anything that parses untrusted input.

```rust
//! `src/lib.rs`. Doctests compile and run under `cargo test --doc`:
//! ```
//! assert_eq!(alphafux_core::parse_pair("a=1"), Some(("a".into(), "1".into())));
//! ```

pub fn parse_pair(raw: &str) -> Option<(String, String)> {
 let (k, v) = raw.split_once('=')?;
 (!k.is_empty()).then(|| (k.to_string(), v.to_string()))
}

#[cfg(test)]
mod tests {
 use super::*;

 #[test]
 fn parses_simple_pair() {
 assert_eq!(parse_pair("a=1"), Some(("a".into(), "1".into())));
 }

 #[test]
 fn rejects_missing_separator() {
 assert_eq!(parse_pair("novalue"), None);
 }

 // Table-driven, deterministic, reproducible, and no extra crate needed.
 #[test]
 fn roundtrip_is_lossless() {
 for sample in ["", "a", "key=value", "\u{1F600}"] {
 match parse_pair(sample) {
 Some((k, v)) => assert_eq!(format!("{k}={v}"), sample),
 None => assert!(!sample.contains('=')),
 }
 }
 }
}
```

For randomized properties use `proptest`; for parsers use `cargo-fuzz` (add with
`cargo add --dev proptest` and `cargo install cargo-fuzz`, verify current). Each
parser gets a target that never panics, hangs, or allocates without bound:

```rust
// fuzz/fuzz_targets/parse_rule.rs
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
 if let Ok(text) = std::str::from_utf8(data) {
 let _ = alphafux_core::parse_rule(text);
 }
});
```

Test hygiene: no sleeps as synchronization (use channels, barriers, or paused
time); no shared mutable globals, since the harness runs tests in parallel; a
tempfile crate for fixtures; assertions that print inputs; every test runnable
alone.

## 9. Quality gates: what "done" means

These gates are the shared contract between builder, tester, and security
profiles. Run them locally before reporting work; CI runs the same script so the
two can never drift.

```bash
set -euo pipefail

cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-targets
cargo test --workspace --doc
cargo doc --workspace --no-deps --document-private-items # broken docs fail CI

# Supply chain and policy (install via cargo install, verify current)
cargo deny check advisories licenses bans sources
cargo audit

# Memory and UB hunting on nightly
cargo +nightly miri test --workspace
cargo +nightly miri test --workspace -Zmiri-strict-provenance

# Coverage and fuzzing (Linux CI recommended)
cargo llvm-cov --workspace --lcov --output-path lcov.info
cargo fuzz run parse_rule -- -max_total_time=60
```

`deny.toml` (start from `cargo deny init`, then edit; key names vary by release,
so verify against your installed version):

```toml
[advisories]
yanked = "deny"
ignore = [
 # { id = "RUSTSEC-XXXX-XXXX", reason = "not reachable; tracked in PROJ-1234" },
]

[licenses]
allow = ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unicode-3.0", "Zlib"]

[bans]
multiple-versions = "warn"
wildcards = "deny"

[sources]
unknown-registry = "deny"
unknown-git = "deny"
```

Every advisory ignore needs a tracker ID in the harness and an expiry date; silent
ignores are how CVEs come back. CI shape (pin third-party actions to a reviewed
commit SHA after verifying the current tag):

```yaml
name: rust-gates
on:
 pull_request:
 push:
 branches: [main]
jobs:
 gates:
 runs-on: ubuntu-latest
 steps:
 - uses: actions/checkout@v4
 - uses: dtolnay/rust-toolchain@stable
 with:
 components: rustfmt, clippy
 - uses: Swatinem/rust-cache@v2
 - run: cargo fmt --all -- --check
 - run: cargo clippy --workspace --all-targets --all-features -- -D warnings
 - run: cargo test --workspace --all-targets --locked
 - run: cargo deny check
```

Keep `scripts/gates.sh` running the same commands in the same order, so a green
local run means a green CI run.

## 10. Security hardening (security profile)

- **Supply chain:** lockfile committed, `cargo deny` and `cargo audit` green, no
 git deps without a pinned revision, `--locked` on every CI build, `cargo vendor`
 for air-gapped AlphaFlux deployments.
- **MSRV:** `package.rust-version` per crate, proven with `cargo +<msrv> check`.
- **Unsafe budget:** `#![forbid(unsafe_code)]` by default; each opt-out crate
 publishes its block list for review.
- **Untrusted input:** bound allocations derived from input length before
 allocating, `checked_add` / `checked_mul` in parsers, oversized frames rejected
 up front, `Vec::try_reserve` where allocation failure must be an error.
- **Secrets:** a struct holding tokens must not derive `Debug` verbatim; redact
 or omit the field.
- **FFI:** the C ABI exported to iTaK Browser validates pointers and lengths on
 the Rust side, catches panics so no unwind crosses the boundary, and says which
 side frees each buffer.
- **Denial of service:** timeouts on every socket await, bounded channels, worker
 counts you can justify under load.
- **Crypto:** never hand-roll primitives; use a reviewed crate (verify current)
 and keep algorithm choice in configuration.

## 11. Performance and profiling

Measure before optimizing; prefer clarity until a profile says otherwise.

```toml
# Cargo.toml release profile for shipped binaries
[profile.release]
lto = "fat" # cross-crate inlining, costs build time
codegen-units = 1 # better optimization, slower compile
panic = "abort" # smaller binaries; only where nothing catches panics
strip = true # drop symbols from the artifact

# Keep dev builds fast: no lto, no opt-level in [profile.dev]
```

```bash
cargo build --release --locked

# Where does time go? (install the tools with cargo install, verify current)
cargo flamegraph --bin scanner -- ./testdata/corpus
perf record -g -- ./target/release/scanner ./testdata/corpus # Linux

# Nightly sanitizer sweeps for the tester profile: ASan, LSan, TSan
RUSTFLAGS="-Zsanitizer=address" cargo +nightly test -Zbuild-std --target x86_64-unknown-linux-gnu
```

Benchmarks on stable need a maintained harness such as `criterion` (add with
`cargo add --dev criterion`, verify current), since `#[bench]` stays nightly-only:
wrap the hot call in `b.iter(|| ...)` and compare distributions, not one timing.

Optimization order: kill clones in hot loops (`&str` over `String`, `iter()` over
`into_iter()` on a borrow), pick the right container (`VecDeque` queues,
`Cow<str>` read-mostly text, `Box<[T]>` fixed sequences), drop `dyn` from inner
loops, then unsafe or SIMD.

## 12. Macros, generics, serialization

Start with `macro_rules!`; use a procedural macro only when the shape cannot be
declared. Real derives use `syn` and `quote` (`cargo add syn --features full`,
`cargo add quote`, verify current) and emit a spanned `compile_error!` on
unsupported shapes. Const generics put sizes in the type: `fn dot<const N: usize>
(a: &[f64; N], b: &[f64; N]) -> f64` refuses mismatched inputs at compile time,
and `struct Grid<const R: usize, const C: usize> { cells: [[f64; C]; R] }`
checks array lengths for free.

A dependency-free procedural macro crate, minimal but real:

```rust
// crate: alphafux-macros, with [lib] proc-macro = true in Cargo.toml
use proc_macro::TokenStream;

#[proc_macro]
pub fn make_answer(_: TokenStream) -> TokenStream {
 "fn answer() -> u32 { 42 }".parse().expect("literal tokens parse")
}

```

Serialization: `serde` with `derive` is the default (`cargo add serde --features
derive`, `cargo add serde_json`, verify current). Give optional config fields
`#[serde(default = "...")]` so older configs keep loading, and parse with
`serde_json::from_str::<ScanConfig>(raw)` so bad configuration is a typed error,
not a panic at first access.

## 13. Diagnostics cookbook: read the error, then apply the fix

Abbreviated shapes of the errors you hit most; real output carries spans, notes,
and a `rustc --explain <code>` pointer. Run the explain command whenever a
message is not self-explanatory.

```text
error[E0499]: cannot borrow `s` as mutable more than once at a time
 |
4 | let r1 = &mut s;
 | - first mutable borrow
6 | let r2 = &mut s;
 | ^^^^^^ second mutable borrow occurs here

error[E0277]: the trait bound `Client: Send` is not satisfied
 = note: `Client` holds an `Rc` or raw pointer; swap to `Arc` or `Mutex`,
 or keep the value on its owning thread
```

| Symptom | First fix |
| --- | --- |
| E0499 / E0502 double borrow | narrow scopes, or restructure with indices instead of live refs |
| E0382 use of moved value | borrow with `&v`, clone at the boundary, pass by reference |
| E0597 temporary dropped | bind the owner to a `let` before taking the reference |
| E0277 `Send` not satisfied | find the `Rc`, `RefCell`, or raw pointer and replace it |
| `select!` arm borrow conflict | declare `&mut` handles outside the macro, or clone the handle |

## 14. Pitfalls checklist before reporting Rust work done

1. `cargo fmt --check`, `clippy -D warnings`, `cargo test`, `cargo test --doc`,
 and `cargo build --locked` pass on a clean tree.
2. No `unwrap()` on input, config, or lock acquisition in library code; `expect`
 on an invariant you proved must carry a real message.
3. No `unsafe` without a `SAFETY:` comment, none outside allowed crates, no
 `static mut` references.
4. No lock held across `.await` or while calling unknown code; a documented lock
 order whenever more than one lock exists.
5. Allocations sized from untrusted input are bounded or use `try_reserve`;
 parser arithmetic is checked.
6. Errors are typed at library boundaries, human-readable at the CLI, and name
 the operator's next step.
7. Panics never cross the FFI boundary; `panic = "abort"` is a deliberate
 per-profile decision, not an inherited default.
8. `package.rust-version` set, lockfile committed, `cargo deny` and `cargo audit`
 green, every exception carrying a tracker ID with an expiry.
9. New dependencies justified in the PR: purpose, maintenance signal, license,
 and version read from `cargo add` or Cargo.lock.
10. A benchmark or profiling note backs any performance claim.

## 15. Using this skill on the AlphaFlux pipeline

- **Builder:** sections 1, 2, 3, 4, 11, 12. One module per feature, workspace
 lints inherited, `cargo fix --edition` for migrations, gates green before
 handoff.
- **Tester:** sections 8, 9, 13, 14. Four test layers, Miri and sanitizer sweeps
 on nightly, fuzz targets for every parser, coverage artifact produced.
- **Security:** sections 5, 9, 10. Walk every `unsafe` block and FFI export, run
 `cargo deny` and `cargo audit`, verify MSRV claims, confirm input paths are
 bounded and panic-free.

Brand strings are exact in code, logs, docs, and CLI output: AlphaFlux,
AlphaVision, AlphaSafe, iTaK, Patriot Pest Control. Do not invent casing
variants.

## 16. References (stable, official)

- The Rust Programming Language: https://doc.rust-lang.org/book/
- Rust Reference: https://doc.rust-lang.org/reference/
- Edition Guide (2024 changes): https://doc.rust-lang.org/edition-guide/
- Release notes: https://doc.rust-lang.org/stable/releases.html
- The Cargo Book: https://doc.rust-lang.org/cargo/
- Clippy lints: https://doc.rust-lang.org/clippy/
- Error index: https://doc.rust-lang.org/error_codes/error-index.html
- Rustonomicon (unsafe): https://doc.rust-lang.org/nomicon/
- Unsafe Code Guidelines: https://rust-lang.github.io/unsafe-code-guidelines/
- Async Book: https://rust-lang.github.io/async-book/
- rustup Book: https://rust-lang.github.io/rustup/
- Blog: https://blog.rust-lang.org/ | docs.rs: https://docs.rs
- crates.io: https://crates.io | RustSec: https://rustsec.org

Verify crate-level facts (features, MSRV, version, maintenance) on docs.rs when
you use them. This skill states no crate versions on purpose.
