# Mojo
Checked against: Mojo via pixi (Oct 2026). Flags and stdlib names change fast; verify against the installed version (see below).

Mojo evolves quickly and its tooling is thinner than Rust/Go. **Before relying on any flag or stdlib name below, confirm it against the installed version**:

```bash
mojo --version
mojo --help ; mojo build --help ; mojo run --help ; mojo test --help ; mojo format --help
```

Typical environment: a `pixi.toml` (or legacy `magic`/`mojoproject.toml`) project. Prefix commands with `pixi run` (or `magic run`) so the pinned toolchain is used, e.g. `pixi run mojo build src/main.mojo`. If a task `[tasks]` section exists (`pixi task list`), prefer those tasks.

## Debug instrumentation (BUILD)

1. **Check the stdlib first** for a logging facility (`from logger import ...` exists in recent releases; verify with `mojo doc` or the stdlib docs for the installed version). If present, use it. If absent, create one tiny `log.mojo` wrapper and use it everywhere (no scattered `print`).
2. **Compile-time debug switch** so release builds pay nothing:

```mojo
from sys import is_defined, env_get_string   # verify names for the installed version

alias DEBUG = is_defined["MOJO_DEBUG"]()      # build with: mojo build -D MOJO_DEBUG ...

@always_inline
fn debug_log[module: StringLiteral](msg: String):
    @parameter
    if DEBUG:
        print("[DEBUG]", module, ":", msg)

fn error_log(module: String, msg: String):
    print("[ERROR]", module, ":", msg)
```

3. Use `debug_assert` (compiled out unless assertions enabled; check `-D ASSERT=all` in the installed version's docs) for invariants, and explicit `raises` + `try/except` with context-rich messages for runtime failures. Mojo has no exception chain: **include the cause in the re-raised message** (`raise Error("load_config: " + String(e))`).
4. Wrap `main` in a top-level `try/except` that prints the error and exits non-zero:

```mojo
fn main():
    try:
        run()
    except e:
        error_log("main", String(e))
        # exit non-zero per installed stdlib (e.g. sys.exit(1))
```

5. For each module log: entry/exit of public fns at DEBUG, every raised error, every FFI/Python-interop call (`Python.import_module`) and its result summary, and sizes/shapes for tensors/buffers.
6. Runtime level: read an env var once at startup (`os.getenv`) and keep it in a module-level struct if the stdlib allows; otherwise rely on the compile-time `-D` flag and document it.
7. Debug self-test: write a test that calls a failing path and checks the raised error text includes the module name and cause. Where logging goes to stdout, test via a sink parameter (pass a writer/closure) rather than capturing stdout.

## Gates

```bash
mojo format -l 100 .              # or: mojo format <files>; then `git diff --exit-code` to verify formatted (no --check flag assumed: verify `mojo format --help`)
mojo build -o /tmp/app_check src/main.mojo      # warnings count: read and fix each
mojo build -g -D MOJO_DEBUG -o /tmp/app_debug src/main.mojo   # debug symbols + debug logs
mojo test -I src test/            # or: pixi run test ; the Mojo `testing` module: assert_equal, assert_true, assert_raises
mojo package src -o /tmp/pkg.mojopkg   # if the repo is a library: proves the package compiles
```

Notes:
- **No dedicated linter**: compensate with `mojo build` warnings reviewed as errors, `mojo format`, the language server diagnostics (`mojo-lsp-server` if used by the editor), and the manual checklist below. Say so in the report instead of pretending a lint passed.
- Debugger: `mojo debug src/main.mojo` (LLDB-based) or `mojo build -g` then `lldb ./app`; also VS Code Mojo debugger. Use for crash reproduction, not as a replacement for tests.
- Sanitizers/optimization: try `mojo build --sanitize address` (and `thread`) if the installed version lists it in `--help`; compare `-O0` vs `-O3` behavior for UB-like discrepancies.
- Python interop: run the Python side's own checks too (`ruff`, `mypy`, `pytest`) if the project has Python modules.
- GPU/MAX code: needs matching hardware; if unavailable, report NOT RUN and test CPU fallbacks.
- Benchmarks: use the stdlib `benchmark` module for perf claims; never claim speedups without numbers.

## Hallucination traps (high risk in Mojo)

- Stdlib/module renames between releases (`tensor`, `memory`, `collections`, `utils`, `sys`, `os`, `time` APIs; `Tensor` removed/moved; `DTypePointer` -> `UnsafePointer`; `let` removed; `inout` -> `mut`, `borrowed` -> `read`, `owned` -> `var` in newer conventions; `fn`/`def` semantics; `String`/`StringRef`/`StringSlice` changes; `Span`; `List` vs `DynamicVector`). Model memory of Mojo is frequently stale: **grep the installed stdlib source or docs** (find with `pixi run python -c "import sys"`/`find / -name "*.mojopkg"` or the `modular` install dir) before using any API, and let `mojo build` be the arbiter.
- Syntax from Python that Mojo lacks: no full Python dynamic features in `fn`; no list comprehensions in older versions; keyword/default semantics differ; check each language feature.
- Argument conventions and ownership: `read`/`mut`/`var`/`out`/`ref` (or older `borrowed`/`inout`/`owned`): use whichever the installed compiler accepts.

## Mojo audit checklist

- Use-after-move/free; copies of large structs missing `^` transfer or implicit copies in hot loops; `UnsafePointer` alloc without matching `free`, out-of-bounds pointer arithmetic, uninitialized memory; lifetime/origin errors that compile but alias.
- Missing `raises` handling: unhandled `raises` at top level; empty `except`; swallowing errors from Python interop.
- SIMD/vectorize/parallelize: tail handling for sizes not multiple of SIMD width, race on shared buffers inside `parallelize`, off-by-one in `vectorize` bounds, dtype overflow/precision (float16/bfloat16), NaN/inf handling.
- Python interop: GIL/blocking, unconverted `PythonObject`, exceptions from Python not mapped, leaking references, untrusted data into `Python.evaluate`.
- Compile-time parameters: `alias`/parameter misuse that moves runtime failure to confusing compile errors; unbounded recursion in parameter evaluation.
- Tests: Mojo tests must cover edge sizes (0, 1, width-1, width, width+1, large), error paths (`assert_raises`), and numerical tolerance (`assert_almost_equal`).
- Architecture: module/package layout (`__init__.mojo`), no giant single-file programs, consistent naming (snake_case fns, PascalCase structs), traits used for interfaces rather than copy-paste.
