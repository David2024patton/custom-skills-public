# Go
Checked against: Go 1.26 (Oct 2026).

## Debug instrumentation (BUILD)

Use the stdlib `log/slog` (Go 1.21+). Check `go.mod` for the Go version; if older, use the project's existing logger (zap/zerolog) with the same pattern.

```go
// internal/logging/logging.go
var Level = new(slog.LevelVar) // flip at runtime

func Init() *slog.Logger {
    if v := os.Getenv("LOG_LEVEL"); v != "" { _ = Level.UnmarshalText([]byte(v)) } // handle error: warn on bad value
    h := slog.NewJSONHandler(os.Stderr, &slog.HandlerOptions{Level: Level, AddSource: true,
        ReplaceAttr: redact}) // redact password/token/secret/authorization keys
    l := slog.New(h); slog.SetDefault(l); return l
}

// per package
var log = slog.Default().With("module", "orders")

func (s *Service) Create(ctx context.Context, in Input) (out Output, err error) {
    l := log.With("request_id", reqID(ctx))
    start := time.Now()
    l.Debug("create: enter", "items", len(in.Items))
    defer func() {
        if err != nil { l.Error("create: failed", "err", err, "dur", time.Since(start)) } else { l.Debug("create: ok", "dur", time.Since(start)) }
    }()
    ...
}
```

Rules: wrap errors with `fmt.Errorf("create order: %w", err)` so the chain is logged; pass `context.Context` as the first param everywhere and honor cancellation; every goroutine launched goes through a helper that has `defer recover()` + logging + a way to stop (ctx/WaitGroup/errgroup); expose `net/http/pprof` on a localhost-only debug port behind a flag; set `GODEBUG`/`GOTRACEBACK=all` in debug runs.

Debug self-test: build the handler over a `bytes.Buffer`, run failure path, assert record present and that a fake secret is absent.

## Gates (in order)

```bash
test -z "$(gofmt -l .)"            # or gofmt -l . and review output
go vet ./...
golangci-lint run ./...             # if installed / .golangci.yml exists
go build ./...
go test -race -count=1 -shuffle=on -timeout 300s ./...
govulncheck ./...
```

Version currency (see SKILL.md): keep the go.mod `toolchain` line on the current patched release and the CI Go version in agreement with it; govulncheck flags the toolchain itself when it is stale, and that failure is a HIGH, not noise. govulncheck itself must be BUILT with a Go at least as new as the toolchain it scans: an older build fails parsing newer stdlib sources ("file requires newer Go version"). Rebuild it before distrusting the target: `GOTOOLCHAIN=<target> go install golang.org/x/vuln/cmd/govulncheck@latest`, then rerun.

Extras when relevant:
- Hostile lint set (if no config exists): `golangci-lint run -E errcheck,gosec,staticcheck,revive,bodyclose,noctx,errorlint,contextcheck,gocritic,unparam,nilerr,rowserrcheck,sqlclosecheck,exhaustive`.
- Leaks: `go.uber.org/goleak` in `TestMain` (`goleak.VerifyTestMain(m)`).
- Fuzz: `go test -fuzz=FuzzParse -fuzztime=60s ./pkg`. Bench: `go test -bench . -benchmem`. Coverage: `go test -cover -coverprofile=c.out ./... && go tool cover -func=c.out`.
- Build tags/OS matrix: `GOOS=linux go vet ./...`, `GOOS=windows go build ./...` if cross-platform.
- Module hygiene: `go mod tidy && git diff --exit-code go.mod go.sum`, `go mod verify`.
- Debugger: `dlv test ./pkg -- -test.run TestName` / `dlv debug`.
- Goroutine/heap dumps: `curl localhost:6060/debug/pprof/goroutine?debug=2`.

## Hallucination traps

- Invented stdlib functions or packages (`strings.ContainsAny` vs non-existent helpers, `slices`/`maps` only exist in 1.21+, `min`/`max`/`clear` builtins 1.21+, loop-var semantics changed in 1.22). Verify with `go doc pkg.Func`.
- Third-party API drift (`gin`, `chi`, `gorm` v1 vs v2, `pgx` v4 vs v5, `grpc` options). Check `go.mod` version and `go doc github.com/x/y.Func`.
- `go build` is the truth: never assume it compiles.

## Go audit checklist

- Ignored errors: `_ = err`, `x, _ :=`, unchecked `defer f.Close()` on writes, `rows.Err()` not checked, `resp.Body` not closed.
- Concurrency: shared maps without mutex (race detector), loop variable capture (pre-1.22), `WaitGroup.Add` inside the goroutine, unbuffered channel send without receiver/ctx select (leak), `time.After` in loops, missing `ctx.Done()` select, `sync.Mutex` copied by value, double close of channel.
- HTTP: no `ReadHeaderTimeout`/`Timeout` on server/client, `http.DefaultClient` without timeout, no `MaxBytesReader`, handlers that `panic`, leaking `err.Error()` to clients.
- Security: `exec.Command("sh","-c", userInput)`, SQL by `fmt.Sprintf`, `filepath.Join` with user path without `filepath.Clean` + prefix check, `math/rand` for tokens (use `crypto/rand`), `InsecureSkipVerify`, JWT `alg` not pinned, timing-unsafe secret compare (use `subtle.ConstantTimeCompare`), IDOR in handlers that load by ID without ownership check.
- Nil: nil map writes, nil interface holding nil pointer, unchecked type assertions (`v := x.(T)` without `ok`).
- Architecture: package cycles, `init()` side effects, global mutable state, interfaces defined on the producer side, giant `main.go`.
