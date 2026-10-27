<div align="center">

# Custom Skills

**The portable skill and persona package for Hermes Agent.**

A snapshot of the methods, gates, and personas David Patton runs, in one
repo a fresh install (or another harness) can rebuild itself from. It is a
snapshot, not a live sync: the private source repo moves first, and this
package is republished from it.

[QA-LOOP](QA-LOOP.md) · [MANIFEST](MANIFEST.md) · [IDEA](IDEA.md) ·
[Public mirror](https://github.com/David2024patton/custom-skills-public)

</div>

---

## What this is

Skills come from everywhere: written by David, built by whichever AI he is
working with, or picked up from other projects and kept because they work.
This repo is the one home for all of them, no matter where they started.

Each skill is self-contained in its own folder:

| Piece | Role |
|---|---|
| `SKILL.md` | the method, written so an agent can run the task cold |
| `skill.yaml` | name, title, and the one-line description, in the folders that carry one |
| `references/`, `scripts/`, `templates/` | supporting material where a skill needs it |

Not every skill carries a `skill.yaml`: 115 of the 297 skills in this repo
carry a `skill.yaml` (recount 2026-10-26). The rest state their name, author, and
license in the `SKILL.md` frontmatter alone, or carry no frontmatter at all;
[THIRD-PARTY.md](THIRD-PARTY.md) records which is which for every skill.

## Repo map

| Path | What lives there |
|---|---|
| [personas/](personas/) | one `SOUL.md` per Hermes persona profile (23 total: business, SDLC engineering, orchestrator, critic, skeptic, uispecialist, ideator) |
| [skills/](skills/) | the pipeline skills: the 18 `persona-*` role skills, the critics (`persona-skeptic`, `critic-lens-*`), gates (`exec-scripts`, `ui-visual-check`, `final-auditor`), context control, research and SEO |
| [critic-lens-compliance](skills/software-development/critic-lens-compliance/SKILL.md) | compliance readiness audits: one control library across SOC 2, GDPR/CCPA, NIST CSF, ISO 27001 with file:line evidence |
| [scripts/](scripts/) | per-language QA packs (12 languages) plus `security/` and `web/` instruments, and the publish tooling |
| [knowledge/](knowledge/) | curated per-language digests |
| [context/](context/) | context-loading and domain-fanout notes |
| [QA-LOOP.md](QA-LOOP.md) | the build law: 7-phase loop, critic checklist, fix loop, visual gate |
| [MANIFEST.md](MANIFEST.md) | full inventory of the pipeline package and its sources |
| [bootstrap.sh](bootstrap.sh) | rebuild a fresh Hermes install from this package |
| [collection-router/](collection-router/) | the one entry skill: routes any task to the right skill or persona over registry.json |
| [registry.json](registry.json) | machine generated index of every skill and persona (built by scripts/build-registry.py; never hand edited) |
| [WORDING-STANDARD.md](WORDING-STANDARD.md) | the wording law: portable core, labeled local bindings, capability vocabulary |

## The persona pipeline

This repo carries the portable pieces of the Hermes persona pipeline, so
another harness or a fresh Hermes install can rebuild the whole system from
here: phase profiles that hand work down a parent-chained kanban line, a
critic stack that attacks every diff before it ships, and the QA law that
decides what done means.

## Skill index

Every flat skill, grouped by where it came from. Pipeline skills under
`skills/` are indexed by category in [MANIFEST.md](MANIFEST.md).

### David custom

| Skill | What it does |
|---|---|
| [audit_code](audit_code/SKILL.md) | Hostile self-review, debug-first instrumentation, and verification gates for Mojo, Rust, Go, Flutter/Dart, and JavaScript/TypeScript. BUILD mode bakes logging and debug hooks into every module from the start; AUDIT mode attacks ... |
| [collection-router](collection-router/SKILL.md) | Route a task to the right skill or persona in this collection. Use first when a task could match more than one skill, when no specific skill has been named, or when a workflow spans skills: consults the machine generated registry, applies the ... |
| [commit-gates](commit-gates/SKILL.md) | Commit Gates: nothing lands on red (David Patton). Linked from the github-repo-standard skill. This skill owns everything about proving code before. |
| [deep-research](skills/deep-research/SKILL.md) | Evidence-first deep research with a run ledger, source quality scoring, counterevidence checks, and a built-in skeptic pass, producing cited reports the user can act on. |
| [alphaflux-research](alphaflux-research/SKILL.md) | Deep research specialized for AlphaFlux: the evidence-first deep research engine plus the AlphaFlux layer, top 10 competitors both ways (to the customer and to AlphaFlux), comparison against AlphaFlux's real modules, a ... |
| [game-creation](game-creation/SKILL.md) | Create games end to end: original games, revivals of defunct games, and retro emulation platforms. Covers rights and licenses, design, revival research, prototyping, production, emulator engineering, playtesting, launch, and live ... |
| [github-repo-standard](github-repo-standard/SKILL.md) | GitHub Repo Standard (David Patton). Every repo David owns carries the same skeleton so any project can be picked up cold, by him or by an agent, and. |
| [google-business-profiles](google-business-profiles/SKILL.md) | Run a Google Business Profile end to end: audit, phone and description edits, services cleanup, service areas at the 20 cap, photo cadence, policy-safe posts, reviews, and the appeal when posting gets turned off. Use for any ... |
| [social_publishing_rejected_media](social_publishing_rejected_media/SKILL.md) | Keeps a user rejection of source footage or images in force across re-renders, so approving a template or caption never revives media the user already rejected. |

### Go library (samber and community)

| Skill | What it does |
|---|---|
| [golang-benchmark](golang-benchmark/SKILL.md) | Golang benchmarking, profiling, and performance measurement. Use when writing, running, or comparing Go benchmarks, profiling hot paths with pprof, interpreting CPU/memory/trace profiles, analyzing results with benchstat, setting ... |
| [golang-cli](golang-cli/SKILL.md) | Golang CLI application development. Use when building, modifying, or reviewing a Go CLI tool, especially for command structure, flag handling, configuration layering, version embedding, exit codes, I/O patterns, signal handling, ... |
| [golang-code-style](golang-code-style/SKILL.md) | Golang code style conventions, line length and breaking, variable declarations, control flow clarity, when comments help vs hurt. Use when writing or reviewing Go code, asking about style or clarity, or establishing project ... |
| [golang-concurrency](golang-concurrency/SKILL.md) | Golang concurrency design, goroutine lifecycle and leak prevention, channels and `select`, channel ownership and direction, `sync.Mutex`/`RWMutex`/`sync.Map`/`sync.Once`/atomics, `errgroup`, `singleflight`, worker pools, and ... |
| [golang-context](golang-context/SKILL.md) | Idiomatic context.Context usage in Golang, propagation through API boundaries, cancellation, timeouts and deadlines, request-scoped values, context.WithoutCancel for background work outliving requests. Apply when designing ... |
| [golang-continuous-integration](golang-continuous-integration/SKILL.md) | GitHub Actions CI/CD pipeline configuration for Golang projects, workflow files for test, lint, SAST, coverage and vulnerability-scan jobs, Dependabot and Renovate config files, GoReleaser release pipelines, Docker build/push, ... |
| [golang-data-structures](golang-data-structures/SKILL.md) | Golang data structures, slices (internals, capacity growth, preallocation, slices package), maps (internals, hash buckets, maps package), arrays, container/list/heap/ring, strings.Builder vs bytes.Buffer, generic collections, ... |
| [golang-database](golang-database/SKILL.md) | Comprehensive guide for Go database access, parameterized queries, struct scanning, NULLable columns, transactions, isolation levels, SELECT FOR UPDATE, connection pool, batch processing, context propagation, and migration ... |
| [golang-dependency-injection](golang-dependency-injection/SKILL.md) | Comprehensive guide for dependency injection (DI) in Golang. Covers why DI matters (testability, loose coupling, separation of concerns, lifecycle management), manual constructor injection, and DI library comparison (google/wire, ... |
| [golang-dependency-management](golang-dependency-management/SKILL.md) | Dependency management for Golang projects, go.mod and go.sum, `go get` install and upgrade flows, Minimal Version Selection, conflict resolution with replace/exclude/retract, `govulncheck` scanning of the module tree, outdated ... |
| [golang-design-patterns](golang-design-patterns/SKILL.md) | Idiomatic Golang design patterns, functional options, constructor APIs, `init()` and global-state avoidance, enums, panic vs error decisions, resource management and lifecycle, graceful shutdown, timeouts and retries, streaming ... |
| [golang-documentation](golang-documentation/SKILL.md) | Comprehensive documentation guide for Golang projects, covering godoc comments, README, CONTRIBUTING, CHANGELOG, Go Playground, Example tests, API docs, and llms.txt. Use when writing or reviewing doc comments, documentation, ... |
| [golang-error-handling](golang-error-handling/SKILL.md) | Idiomatic Golang error handling, creation, wrapping with %w, errors.Is/As, errors.Join, custom error types, sentinel errors, panic/recover, the single handling rule, structured logging with slog, HTTP request logging middleware, ... |
| [golang-google-wire](golang-google-wire/SKILL.md) | Compile-time dependency injection in Golang using google/wire, wire.NewSet, wire.Build, wire.Bind (interface→concrete), wire.Struct, wire.Value, wire.InterfaceValue, wire.FieldsOf, cleanup functions, //go:build wireinject ... |
| [golang-gopls](golang-gopls/SKILL.md) | Golang semantic code intelligence via `gopls`, the official Go language server, go-to-definition, find references, call/implementation hierarchy, workspace symbol search, package API discovery, diagnostics, safe rename, ... |
| [golang-graphql](golang-graphql/SKILL.md) | Implements GraphQL APIs in Golang using gqlgen or graphql-go. Apply when building GraphQL servers, designing schemas, writing resolvers, handling subscriptions, or integrating GraphQL with existing Go HTTP services. Also apply ... |
| [golang-grpc](golang-grpc/SKILL.md) | Provides gRPC usage guidelines, protobuf organization, and production-ready patterns for Golang microservices. Use when implementing, reviewing, or debugging gRPC servers/clients, writing proto files, setting up interceptors, ... |
| [golang-how-to](golang-how-to/SKILL.md) | Golang skills orchestrator, always active on any Golang coding, review, debug, or setup task. Reads the task context and loads the most relevant skills from samber/cc-skills-golang, often multiple at once: writing a gRPC service ... |
| [golang-lint](golang-lint/SKILL.md) | Linting best practices and golangci-lint configuration for Golang projects, running linters, configuring .golangci.yml, suppressing warnings with nolint directives, interpreting lint output, and selecting linters. Use when ... |
| [golang-modernize](golang-modernize/SKILL.md) | Modernize Golang code to use recent language features, standard library improvements, and idiomatic patterns. Use when reviewing Go code with old-style patterns, when encountering a deprecation warning, or when the user asks for ... |
| [golang-naming](golang-naming/SKILL.md) | Go (Golang) naming conventions, covers packages, constructors, structs, interfaces, constants, enums, errors, booleans, receivers, getters/setters, functional options, acronyms, test functions, and subtest names. Use this skill ... |
| [golang-observability](golang-observability/SKILL.md) | Golang everyday observability, the always-on signals in production. Covers structured logging with slog, Prometheus metrics, OpenTelemetry distributed tracing, continuous profiling with pprof/Pyroscope, server-side RUM event ... |
| [golang-performance](golang-performance/SKILL.md) | Golang performance optimization patterns and methodology - if X bottleneck, then apply Y. Covers allocation reduction, CPU efficiency, memory layout, GC tuning, pooling, caching, and hot-path optimization. Use when profiling or ... |
| [golang-pkg-go-dev](golang-pkg-go-dev/SKILL.md) | Golang package and module lookup via `godig`, a pkg.go.dev API client (CLI + MCP server). Use for any Go/Golang library's documentation, API signatures, symbols, usage examples, which versions exist, licenses, whether a ... |
| [golang-popular-libraries](golang-popular-libraries/SKILL.md) | Golang library and framework selection, vetted production-ready options by category (web, database, testing, logging, messaging), new and experimental stdlib packages, standard-library-first tradeoffs, and maturity signals ... |
| [golang-project-layout](golang-project-layout/SKILL.md) | Golang project layout and workspace setup, cmd/internal/pkg directory conventions, module and package naming, go.work workspaces, and essential configuration files. Use when starting a new Go project, organizing an existing ... |
| [golang-refactoring](golang-refactoring/SKILL.md) | Golang refactoring, safe, at-scale restructuring of existing Go code: a coverage-adaptive safety net, behavior-preserving transforms (gopls Rename/Extract, `gofmt -r`, `gopatch`), the Fowler catalog mapped to Go, breaking import ... |
| [golang-safety](golang-safety/SKILL.md) | Defensive Golang coding against accidental bugs, nil panics, typed-nil interfaces, `append` backing-array aliasing, silent int64-to-int32 truncation, float `==` comparison, `defer` inside loops, defensive copies of slices and ... |
| [golang-samber-do](golang-samber-do/SKILL.md) | Dependency injection in Golang using samber/do, service containers, lifecycle management, scopes, health checks, graceful shutdown, and module organization. Apply when using or adopting samber/do, when the codebase imports ... |
| [golang-samber-hot](golang-samber-hot/SKILL.md) | In-memory caching in Golang using samber/hot, eviction algorithms (LRU, LFU, TinyLFU, W-TinyLFU, S3FIFO, ARC, TwoQueue, SIEVE, FIFO), TTL, cache loaders, sharding, stale-while-revalidate, missing key caching, and Prometheus ... |
| [golang-samber-lo](golang-samber-lo/SKILL.md) | Functional programming helpers for Golang using samber/lo, 500+ type-safe generic functions for slices, maps, channels, strings, math, tuples, and concurrency (Map, Filter, Reduce, GroupBy, Chunk, Flatten, Find, Uniq, etc.). ... |
| [golang-samber-mo](golang-samber-mo/SKILL.md) | Monadic types for Golang using samber/mo, Option, Result, Either, Future, IO, Task, and State types for type-safe nullable values, error handling, and functional composition with pipeline sub-packages. Apply when using or ... |
| [golang-samber-oops](golang-samber-oops/SKILL.md) | Structured error handling in Golang with samber/oops, error builders, stack traces, error codes, error context, error wrapping, error attributes, user-facing vs developer messages, panic recovery, and logger integration. Apply ... |
| [golang-samber-ro](golang-samber-ro/SKILL.md) | Reactive streams and event-driven programming in Golang using samber/ro, ReactiveX implementation with 150+ type-safe operators, cold/hot observables, 5 subject types (Publish, Behavior, Replay, Async, Unicast), declarative ... |
| [golang-samber-slog](golang-samber-slog/SKILL.md) | Structured logging extensions for Golang using samber/slog-**** packages, multi-handler pipelines (slog-multi), log sampling (slog-sampling), attribute formatting (slog-formatter), HTTP middleware (slog-fiber, slog-gin, ... |
| [golang-security](golang-security/SKILL.md) | Security best practices and vulnerability prevention for Golang, injection (SQL, command, XSS), cryptography, path traversal, SSRF and HTTP security headers, cookies, secrets management, memory safety, PII in logs, STRIDE/DREAD ... |
| [golang-spf13-cobra](golang-spf13-cobra/SKILL.md) | Golang CLI command tree library using spf13/cobra, cobra.Command, RunE vs Run, PersistentPreRunE hook chain, Args validators (NoArgs, ExactArgs, MatchAll, custom), persistent vs local flags, command groups, ValidArgsFunction, ... |
| [golang-spf13-viper](golang-spf13-viper/SKILL.md) | Golang configuration library using spf13/viper, layered precedence (flag > env > file > KV > default), BindPFlag/BindPFlags, SetEnvPrefix + SetEnvKeyReplacer + AutomaticEnv, ReadInConfig + ConfigFileNotFoundError, Unmarshal + ... |
| [golang-stay-updated](golang-stay-updated/SKILL.md) | Golang ecosystem watch list, official sources (go.dev/blog, pkg.go.dev, tour.golang.org, golang-nuts), newsletters (Golang Weekly, Awesome Go Newsletter), communities (r/golang, gophers.slack.com, Go Forum, go.dev/wiki), blogs ... |
| [golang-stretchr-testify](golang-stretchr-testify/SKILL.md) | Comprehensive guide to stretchr/testify for Golang testing. Covers assert, require, mock, and suite packages in depth. Use when writing tests with testify, creating mocks, setting up test suites, or choosing between assert and ... |
| [golang-structs-interfaces](golang-structs-interfaces/SKILL.md) | Golang struct and interface design patterns, composition, embedding, type assertions, type switches, interface segregation, dependency injection via interfaces, struct field tags, and pointer vs value receivers. Use this skill ... |
| [golang-swagger](golang-swagger/SKILL.md) | Golang OpenAPI/Swagger documentation with swaggo/swag, annotation comments (@Summary, @Param, @Success, @Router, @Security), swag init code generation, framework integrations (gin, echo, fiber, chi, net/http), security ... |
| [golang-testing](golang-testing/SKILL.md) | Production-ready Golang tests, table-driven tests, testify suites and mocks, parallel tests, fuzzing, fixtures, goroutine leak detection with goleak, snapshot testing, code coverage, integration tests, idiomatic test naming. Use ... |
| [golang-troubleshooting](golang-troubleshooting/SKILL.md) | Troubleshoot Golang programs systematically - find and fix the root cause. Use when encountering bugs, crashes, deadlocks, races, or unexpected behavior in Go code. Covers debugging methodology, common Go pitfalls, test-driven ... |
| [golang-uber-dig](golang-uber-dig/SKILL.md) | Implements dependency injection in Golang using uber-go/dig, reflection-based container, Provide/Invoke, dig.In/dig.Out parameter and result objects, named values, value groups, optional dependencies, scopes, and Decorate. Apply ... |
| [golang-uber-fx](golang-uber-fx/SKILL.md) | Golang application framework using uber-go/fx, fx.New, fx.Provide, fx.Invoke, fx.Module, fx.Lifecycle hooks, fx.Annotate (name/group/As), fx.Decorate, fx.Supply, fx.Replace, fx.WithLogger, and signal-aware Run(). Apply when ... |

### Local and recovered

| Skill | What it does |
|---|---|
| [android-keyboard](android-keyboard/SKILL.md) | Android Keyboard (IME) Development Skill. Build custom Android keyboards (InputMethodService) with manual APK builds (no Gradle). |
| [appllama-app-design-skill](appllama-app-design-skill/SKILL.md) | Build native-feeling, benchmark-quality mobile app screens (Expo / React Native). Use when designing or implementing any mobile UI, screens, flows, onboarding, paywalls, tab bars, sheets, settings, empty states, or when ... |
| [appllama-usage](appllama-usage/SKILL.md) | Use the Appllama MCP (mcp.appllama.io) well, research real top-grossing mobile apps, their screens, flows, and UI elements, then build from what you learn. Load when the Appllama MCP is connected and the task involves building a ... |
| [local-android-keyboard](local-android-keyboard/SKILL.md) | Recovered local skill; review its instructions before reuse. |
| [local-appllama-app-design-skill](local-appllama-app-design-skill/SKILL.md) | Build native-feeling, benchmark-quality mobile app screens (Expo / React Native). Use when designing or implementing any mobile UI, screens, flows, onboarding, paywalls, tab bars, sheets, settings, empty states, or when ... |
| [local-appllama-usage](local-appllama-usage/SKILL.md) | Use the Appllama MCP (mcp.appllama.io) well, research real top-grossing mobile apps, their screens, flows, and UI elements, then build from what you learn. Load when the Appllama MCP is connected and the task involves building a ... |
| [local-golang-benchmark](local-golang-benchmark/SKILL.md) | Golang benchmarking, profiling, and performance measurement. Use when writing, running, or comparing Go benchmarks, profiling hot paths with pprof, interpreting CPU/memory/trace profiles, analyzing results with benchstat, setting ... |
| [local-golang-cli](local-golang-cli/SKILL.md) | Golang CLI application development. Use when building, modifying, or reviewing a Go CLI tool, especially for command structure, flag handling, configuration layering, version embedding, exit codes, I/O patterns, signal handling, ... |
| [local-golang-code-style](local-golang-code-style/SKILL.md) | Golang code style conventions, line length and breaking, variable declarations, control flow clarity, when comments help vs hurt. Use when writing or reviewing Go code, asking about style or clarity, or establishing project ... |
| [local-golang-concurrency](local-golang-concurrency/SKILL.md) | Golang concurrency design, goroutine lifecycle and leak prevention, channels and `select`, channel ownership and direction, `sync.Mutex`/`RWMutex`/`sync.Map`/`sync.Once`/atomics, `errgroup`, `singleflight`, worker pools, and ... |
| [local-golang-context](local-golang-context/SKILL.md) | Idiomatic context.Context usage in Golang, propagation through API boundaries, cancellation, timeouts and deadlines, request-scoped values, context.WithoutCancel for background work outliving requests. Apply when designing ... |
| [local-golang-continuous-integration](local-golang-continuous-integration/SKILL.md) | GitHub Actions CI/CD pipeline configuration for Golang projects, workflow files for test, lint, SAST, coverage and vulnerability-scan jobs, Dependabot and Renovate config files, GoReleaser release pipelines, Docker build/push, ... |
| [local-golang-data-structures](local-golang-data-structures/SKILL.md) | Golang data structures, slices (internals, capacity growth, preallocation, slices package), maps (internals, hash buckets, maps package), arrays, container/list/heap/ring, strings.Builder vs bytes.Buffer, generic collections, ... |
| [local-golang-database](local-golang-database/SKILL.md) | Comprehensive guide for Go database access, parameterized queries, struct scanning, NULLable columns, transactions, isolation levels, SELECT FOR UPDATE, connection pool, batch processing, context propagation, and migration ... |
| [local-golang-dependency-injection](local-golang-dependency-injection/SKILL.md) | Comprehensive guide for dependency injection (DI) in Golang. Covers why DI matters (testability, loose coupling, separation of concerns, lifecycle management), manual constructor injection, and DI library comparison (google/wire, ... |
| [local-golang-dependency-management](local-golang-dependency-management/SKILL.md) | Dependency management for Golang projects, go.mod and go.sum, `go get` install and upgrade flows, Minimal Version Selection, conflict resolution with replace/exclude/retract, `govulncheck` scanning of the module tree, outdated ... |
| [local-golang-design-patterns](local-golang-design-patterns/SKILL.md) | Idiomatic Golang design patterns, functional options, constructor APIs, `init()` and global-state avoidance, enums, panic vs error decisions, resource management and lifecycle, graceful shutdown, timeouts and retries, streaming ... |
| [local-golang-documentation](local-golang-documentation/SKILL.md) | Comprehensive documentation guide for Golang projects, covering godoc comments, README, CONTRIBUTING, CHANGELOG, Go Playground, Example tests, API docs, and llms.txt. Use when writing or reviewing doc comments, documentation, ... |
| [local-golang-error-handling](local-golang-error-handling/SKILL.md) | Idiomatic Golang error handling, creation, wrapping with %w, errors.Is/As, errors.Join, custom error types, sentinel errors, panic/recover, the single handling rule, structured logging with slog, HTTP request logging middleware, ... |
| [local-golang-google-wire](local-golang-google-wire/SKILL.md) | Compile-time dependency injection in Golang using google/wire, wire.NewSet, wire.Build, wire.Bind (interface→concrete), wire.Struct, wire.Value, wire.InterfaceValue, wire.FieldsOf, cleanup functions, //go:build wireinject ... |
| [local-golang-gopls](local-golang-gopls/SKILL.md) | Golang semantic code intelligence via `gopls`, the official Go language server, go-to-definition, find references, call/implementation hierarchy, workspace symbol search, package API discovery, diagnostics, safe rename, ... |
| [local-golang-graphql](local-golang-graphql/SKILL.md) | Implements GraphQL APIs in Golang using gqlgen or graphql-go. Apply when building GraphQL servers, designing schemas, writing resolvers, handling subscriptions, or integrating GraphQL with existing Go HTTP services. Also apply ... |
| [local-golang-grpc](local-golang-grpc/SKILL.md) | Provides gRPC usage guidelines, protobuf organization, and production-ready patterns for Golang microservices. Use when implementing, reviewing, or debugging gRPC servers/clients, writing proto files, setting up interceptors, ... |
| [local-golang-how-to](local-golang-how-to/SKILL.md) | Golang skills orchestrator, always active on any Golang coding, review, debug, or setup task. Reads the task context and loads the most relevant skills from samber/cc-skills-golang, often multiple at once: writing a gRPC service ... |
| [local-golang-lint](local-golang-lint/SKILL.md) | Linting best practices and golangci-lint configuration for Golang projects, running linters, configuring .golangci.yml, suppressing warnings with nolint directives, interpreting lint output, and selecting linters. Use when ... |
| [local-golang-modernize](local-golang-modernize/SKILL.md) | Modernize Golang code to use recent language features, standard library improvements, and idiomatic patterns. Use when reviewing Go code with old-style patterns, when encountering a deprecation warning, or when the user asks for ... |
| [local-golang-naming](local-golang-naming/SKILL.md) | Go (Golang) naming conventions, covers packages, constructors, structs, interfaces, constants, enums, errors, booleans, receivers, getters/setters, functional options, acronyms, test functions, and subtest names. Use this skill ... |
| [local-golang-observability](local-golang-observability/SKILL.md) | Golang everyday observability, the always-on signals in production. Covers structured logging with slog, Prometheus metrics, OpenTelemetry distributed tracing, continuous profiling with pprof/Pyroscope, server-side RUM event ... |
| [local-golang-performance](local-golang-performance/SKILL.md) | Golang performance optimization patterns and methodology - if X bottleneck, then apply Y. Covers allocation reduction, CPU efficiency, memory layout, GC tuning, pooling, caching, and hot-path optimization. Use when profiling or ... |
| [local-golang-pkg-go-dev](local-golang-pkg-go-dev/SKILL.md) | Golang package and module lookup via `godig`, a pkg.go.dev API client (CLI + MCP server). Use for any Go/Golang library's documentation, API signatures, symbols, usage examples, which versions exist, licenses, whether a ... |
| [local-golang-popular-libraries](local-golang-popular-libraries/SKILL.md) | Golang library and framework selection, vetted production-ready options by category (web, database, testing, logging, messaging), new and experimental stdlib packages, standard-library-first tradeoffs, and maturity signals ... |
| [local-golang-project-layout](local-golang-project-layout/SKILL.md) | Golang project layout and workspace setup, cmd/internal/pkg directory conventions, module and package naming, go.work workspaces, and essential configuration files. Use when starting a new Go project, organizing an existing ... |
| [local-golang-refactoring](local-golang-refactoring/SKILL.md) | Golang refactoring, safe, at-scale restructuring of existing Go code: a coverage-adaptive safety net, behavior-preserving transforms (gopls Rename/Extract, `gofmt -r`, `gopatch`), the Fowler catalog mapped to Go, breaking import ... |
| [local-golang-safety](local-golang-safety/SKILL.md) | Defensive Golang coding against accidental bugs, nil panics, typed-nil interfaces, `append` backing-array aliasing, silent int64-to-int32 truncation, float `==` comparison, `defer` inside loops, defensive copies of slices and ... |
| [local-golang-samber-do](local-golang-samber-do/SKILL.md) | Dependency injection in Golang using samber/do, service containers, lifecycle management, scopes, health checks, graceful shutdown, and module organization. Apply when using or adopting samber/do, when the codebase imports ... |
| [local-golang-samber-hot](local-golang-samber-hot/SKILL.md) | In-memory caching in Golang using samber/hot, eviction algorithms (LRU, LFU, TinyLFU, W-TinyLFU, S3FIFO, ARC, TwoQueue, SIEVE, FIFO), TTL, cache loaders, sharding, stale-while-revalidate, missing key caching, and Prometheus ... |
| [local-golang-samber-lo](local-golang-samber-lo/SKILL.md) | Functional programming helpers for Golang using samber/lo, 500+ type-safe generic functions for slices, maps, channels, strings, math, tuples, and concurrency (Map, Filter, Reduce, GroupBy, Chunk, Flatten, Find, Uniq, etc.). ... |
| [local-golang-samber-mo](local-golang-samber-mo/SKILL.md) | Monadic types for Golang using samber/mo, Option, Result, Either, Future, IO, Task, and State types for type-safe nullable values, error handling, and functional composition with pipeline sub-packages. Apply when using or ... |
| [local-golang-samber-oops](local-golang-samber-oops/SKILL.md) | Structured error handling in Golang with samber/oops, error builders, stack traces, error codes, error context, error wrapping, error attributes, user-facing vs developer messages, panic recovery, and logger integration. Apply ... |
| [local-golang-samber-ro](local-golang-samber-ro/SKILL.md) | Reactive streams and event-driven programming in Golang using samber/ro, ReactiveX implementation with 150+ type-safe operators, cold/hot observables, 5 subject types (Publish, Behavior, Replay, Async, Unicast), declarative ... |
| [local-golang-samber-slog](local-golang-samber-slog/SKILL.md) | Structured logging extensions for Golang using samber/slog-**** packages, multi-handler pipelines (slog-multi), log sampling (slog-sampling), attribute formatting (slog-formatter), HTTP middleware (slog-fiber, slog-gin, ... |
| [local-golang-security](local-golang-security/SKILL.md) | Security best practices and vulnerability prevention for Golang, injection (SQL, command, XSS), cryptography, path traversal, SSRF and HTTP security headers, cookies, secrets management, memory safety, PII in logs, STRIDE/DREAD ... |
| [local-golang-spf13-cobra](local-golang-spf13-cobra/SKILL.md) | Golang CLI command tree library using spf13/cobra, cobra.Command, RunE vs Run, PersistentPreRunE hook chain, Args validators (NoArgs, ExactArgs, MatchAll, custom), persistent vs local flags, command groups, ValidArgsFunction, ... |
| [local-golang-spf13-viper](local-golang-spf13-viper/SKILL.md) | Golang configuration library using spf13/viper, layered precedence (flag > env > file > KV > default), BindPFlag/BindPFlags, SetEnvPrefix + SetEnvKeyReplacer + AutomaticEnv, ReadInConfig + ConfigFileNotFoundError, Unmarshal + ... |
| [local-golang-stay-updated](local-golang-stay-updated/SKILL.md) | Golang ecosystem watch list, official sources (go.dev/blog, pkg.go.dev, tour.golang.org, golang-nuts), newsletters (Golang Weekly, Awesome Go Newsletter), communities (r/golang, gophers.slack.com, Go Forum, go.dev/wiki), blogs ... |
| [local-golang-stretchr-testify](local-golang-stretchr-testify/SKILL.md) | Comprehensive guide to stretchr/testify for Golang testing. Covers assert, require, mock, and suite packages in depth. Use when writing tests with testify, creating mocks, setting up test suites, or choosing between assert and ... |
| [local-golang-structs-interfaces](local-golang-structs-interfaces/SKILL.md) | Golang struct and interface design patterns, composition, embedding, type assertions, type switches, interface segregation, dependency injection via interfaces, struct field tags, and pointer vs value receivers. Use this skill ... |
| [local-golang-swagger](local-golang-swagger/SKILL.md) | Golang OpenAPI/Swagger documentation with swaggo/swag, annotation comments (@Summary, @Param, @Success, @Router, @Security), swag init code generation, framework integrations (gin, echo, fiber, chi, net/http), security ... |
| [local-golang-testing](local-golang-testing/SKILL.md) | Production-ready Golang tests, table-driven tests, testify suites and mocks, parallel tests, fuzzing, fixtures, goroutine leak detection with goleak, snapshot testing, code coverage, integration tests, idiomatic test naming. Use ... |
| [local-golang-troubleshooting](local-golang-troubleshooting/SKILL.md) | Troubleshoot Golang programs systematically - find and fix the root cause. Use when encountering bugs, crashes, deadlocks, races, or unexpected behavior in Go code. Covers debugging methodology, common Go pitfalls, test-driven ... |
| [local-golang-uber-dig](local-golang-uber-dig/SKILL.md) | Implements dependency injection in Golang using uber-go/dig, reflection-based container, Provide/Invoke, dig.In/dig.Out parameter and result objects, named values, value groups, optional dependencies, scopes, and Decorate. Apply ... |
| [local-golang-uber-fx](local-golang-uber-fx/SKILL.md) | Golang application framework using uber-go/fx, fx.New, fx.Provide, fx.Invoke, fx.Module, fx.Lifecycle hooks, fx.Annotate (name/group/As), fx.Decorate, fx.Supply, fx.Replace, fx.WithLogger, and signal-aware Run(). Apply when ... |
| [local-playwright](local-playwright/SKILL.md) | Drive a real headless Chromium with Playwright from this VM: screenshots, clicks, mobile viewport emulation, console error capture. Use when you need to see or interact with a live page, verify a UI change, or test desktop and ... |
| [meta-leads](meta-leads/SKILL.md) | Use Meta Leads when the user asks for Meta Leads or this provider's API. |
| [playwright](playwright/SKILL.md) | Drive a real headless Chromium with Playwright from this VM: screenshots, clicks, mobile viewport emulation, console error capture. Use when you need to see or interact with a live page, verify a UI change, or test desktop and ... |
| [youtube](youtube/SKILL.md) | Use Youtube when the user asks for Youtube or this provider's API. |

### Muse built-in

These skills target the Muse runtime and its install paths; the rest of the collection is agent neutral.

| Skill | What it does |
|---|---|
| [advertising-campaigns](advertising-campaigns/SKILL.md) | Plan, launch and improve paid advertising, from the business goal, audience and channel to creative, budget, approval and performance analysis. Use for any request to write or create an ad, even with no platform named or in a ... |
| [app-creation](app-creation/SKILL.md) | Build or improve an app, page or tool for a concrete need, choosing between a Muse artifact and a hosted builder, and verify that it works for the people who will use it. |
| [business-finance](business-finance/SKILL.md) | Reconcile business accounts, prepare and send invoices and follow up on payments, counting every transaction once against the books. |
| [custom-connector-setup](custom-connector-setup/SKILL.md) | Connect a service Muse does not bundle through its API or MCP server, keep its credential in Muse's secure connection flow, and save the connector doc and any reusable skill. |
| [customer-outreach](customer-outreach/SKILL.md) | Plan and send consented email, SMS and newsletter outreach to the user's customers or subscribers, then measure replies and results. |
| [device-data](device-data/SKILL.md) | Read cached contacts and calendar events from Muse storage. Delete Muse's local copy of either source without modifying paired devices. |
| [documents](documents/SKILL.md) | Read, write and revise documents, PDFs, spreadsheets and presentations, with findings tied to the source and an editable source kept for later changes. |
| [email-management](email-management/SKILL.md) | Find, triage, draft and send email from the right mailbox, keeping the thread, the recipients and the user's approval exact. |
| [event-tickets](event-tickets/SKILL.md) | Find the right event and seats, compare primary and resale offers by delivered total, and buy, transfer or resell tickets within the event's rules. |
| [file-hosting](file-hosting/SKILL.md) | Put a file where the right people can open it and return a safe link, with or without a storage account. |
| [financial-planning](financial-planning/SKILL.md) | Build a budget, test whether a purchase is affordable or plan debt repayment from reconciled spending, balances and due dates. |
| [fitness-tracking](fitness-tracking/SKILL.md) | Review activity, sleep, recovery and body measurements over time against the user's goals, using comparable data from their devices and apps. |
| [flight-booking](flight-booking/SKILL.md) | Find and book the best complete flight for the requested cabin by comparing connected inventory and strong flight sites on verified total price and travel time. |
| [flight-tracking](flight-tracking/SKILL.md) | Check a flight's live status, including a trip already in memory, and monitor a booked trip for schedule, gate, cancellation and fare changes worth acting on. |
| [forget](forget/SKILL.md) | Remove information the user explicitly asks Muse to forget from memory, its copies and any work that could bring it back. |
| [form-design](form-design/SKILL.md) | Design or revise a form or survey with clear questions, a tested respondent path and responses read correctly, whichever tool builds it. |
| [generate_podcast](generate_podcast/SKILL.md) | Research, script and produce a podcast episode, briefing or narrated summary with one or more voices, then deliver, publish or schedule it within the scope the user authorized. |
| [goals](goals/SKILL.md) | Guidance for helping users create and accomplish goals. Read it before you create a goal for the user when no goal-creation contract is in context, and whenever you help with an existing goal. A Goals-tab creation turn already ... |
| [groceries](groceries/SKILL.md) | Shop for groceries for delivery or pickup from the user's chosen store or grocery app, such as Instacart, Walmart or Tesco, including grocery lists, weekly restocking and ingredients for a meal. Also covers takeout and prepared ... |
| [health-review](health-review/SKILL.md) | Organize the user's health records and recent changes into a clear summary and useful questions for a clinician visit. |
| [home-control](home-control/SKILL.md) | Control the user's home devices and routines, check recorded camera events, and confirm each change reached the requested state. |
| [home-search](home-search/SKILL.md) | Find and compare homes to buy or rent in the market where the user is looking, then plan open-house visits or request tours. |
| [hotel-booking](hotel-booking/SKILL.md) | Compare places to stay across hotel sites, booking platforms and rentals by full-stay price, location, room and terms, then book the chosen rate. |
| [image-search](image-search/SKILL.md) | Search the web by text query for image URLs and source pages for feeds, artifacts, and visual references. Does not identify a supplied image or person. |
| [knowledge-organization](knowledge-organization/SKILL.md) | Find, add to and organize the user's notes, notebooks and documents in apps like Notion, Evernote, Google Docs and Drive, keeping the structure they already use. |
| [marketplaces](marketplaces/SKILL.md) | Buy, sell or value used items on resale marketplaces such as eBay, Facebook Marketplace and Craigslist, with fair prices, safe meetups and protected payments. |
| [media-library](media-library/SKILL.md) | Search and inspect the user's photo library, including connected device galleries. Use for photo requests and whenever a photo could ground or personalize a response; lookups of uploaded photos are cheap, so check ... |
| [meeting-follow-up](meeting-follow-up/SKILL.md) | Turn a meeting's notes, transcript or recording into decisions, owned action items and the recap, email or tasks the user wants. |
| [messaging](messaging/SKILL.md) | Message other people from the user's own accounts, such as WhatsApp, Messenger or Slack, and carry a delegated conversation through to its result. |
| [mortgage-comparison](mortgage-comparison/SKILL.md) | Compare home-loan offers on the same assumptions, with rate, APR, fees and monthly cost side by side, then follow through on the user's chosen next step. |
| [muse-early-access](muse-early-access/SKILL.md) | Use for questions about Muse's general early access program, requests to join it, checking or withdrawing a join request, and admission updates. |
| [muse-feedback](muse-feedback/SKILL.md) | Use for feedback and feature requests to the Muse team. Whenever your response tells the user you can't do a specific thing they wanted, or accepts them giving up on one, offer once to file feedback in that response. This covers ... |
| [muse_db](muse_db/SKILL.md) | Inspect database-backed Muse records for diagnosis and cross-table tracing when purpose-built product tools do not expose the needed state. |
| [music-discovery](music-discovery/SKILL.md) | Find the exact recording, recommend music, build or update a playlist and start playback on the device the user wants. |
| [place-discovery](place-discovery/SKILL.md) | Find and compare places to go, such as restaurants, cafes, shops, parks and attractions, with verified locations, hours and a map. |
| [restaurant-reservations](restaurant-reservations/SKILL.md) | Find a restaurant with a real available table, then book, change or cancel the reservation through its own booking route or a reservation platform. |
| [scheduling](scheduling/SKILL.md) | Find times that work across people, calendars and timezones, then place holds, send invitations, share booking links or book appointments the user asked for. |
| [self-awareness](self-awareness/SKILL.md) | Ground self-referential answers in the agent's actual filesystem. Use when the user asks who the agent is, what it can do, what it knows, what it remembers, what it has built, what services are connected, or what rules it follows. |
| [share-ideas](share-ideas/SKILL.md) | Publish a reusable native Muse Idea with idea.share when the user explicitly asks to share or publish an Idea or asks for a muse.ai/ideas link. Never offer it unprompted. Not for pages or write-ups, sending a result to someone, ... |
| [shopping](shopping/SKILL.md) | Use for any product question except groceries and prepared meals: find, reverse image search, shopping Instagram/Facebook/Marketplace links, buy, compare, or evaluate real products with prices, images, and product page URLs, ... |
| [smb-product-shots](smb-product-shots/SKILL.md) | Offers a small business owner or seller to polish, caption or share their own product images to their Instagram, Facebook Page or website. Marketplace listings offer touch-ups first, even when the user only asked for the listing. ... |
| [social-content-performance](social-content-performance/SKILL.md) | Analyze the user's own social posts and account metrics, explain what worked and recommend the next experiment. |
| [social-publishing](social-publishing/SKILL.md) | Plan, create and publish or schedule social posts once the user approves the exact copy and media, then verify each post went out. |
| [spoken-audio](spoken-audio/SKILL.md) | Send the user a voice note or voice message, narrate text for an artifact or scheduled task, or read supplied text aloud as an audio file. |
| [store-operations](store-operations/SKILL.md) | Run an online store's catalog, inventory, orders, refunds and fulfillment, changing only what the merchant asked and verifying each change. |
| [style-tryon](style-tryon/SKILL.md) | Shows the user wearing clothing, shoes, or wearable accessories from their shopping results, one item or 2-3 side by side, rendered from their own photo, then helps them buy their pick. Load it before replying with shopping ... |
| [subscription-status](subscription-status/SKILL.md) | Answer questions about the user's Muse subscription, plan, usage, tokens, reset timing, or available plans and prices, or verify information that references the Muse subscription. |
| [task-management](task-management/SKILL.md) | Capture, organize and update the user's tasks in their own task app, such as Todoist, Asana, Linear or Google Tasks. |
| [translation](translation/SKILL.md) | Translate text, documents or videos for the intended reader while preserving meaning, terminology and usable formatting. |
| [trip-planning](trip-planning/SKILL.md) | Plan a feasible trip in one living itinerary, coordinating flights, stays, transport, dining and activities while keeping ideas, choices and bookings distinct. Also covers a narrow airport, entry, transit, transfer or fast-track ... |
| [trip-transport](trip-transport/SKILL.md) | Get around on a trip: compare and book rental cars, trains, ferries, buses, bikes, rides and airport transfers, with the local rules that decide whether a choice works. |
| [wearables-comms](wearables-comms/SKILL.md) | Place a native call or text from the user's glasses to the right person, or answer, decline or cancel a call on them. |
| [wide-research](wide-research/SKILL.md) | Use when the user needs broad parallel research across many independent inputs with a shared output schema. |
| [workout-planning](workout-planning/SKILL.md) | Design a practical workout or training program and adjust it from completed sessions, effort and recovery. |

## Licensing

David Patton's own work in this repo is MIT, under the root
[LICENSE](LICENSE). Third party skills are mapped in
[THIRD-PARTY.md](THIRD-PARTY.md): the ones that claim MIT may be
redistributed under MIT terms, and the ones that state no license are all
rights reserved and are not cleared for redistribution until their
author's grant is on file. Check THIRD-PARTY.md before reusing any skill.

## MCP

Only one skill in this repo is mapped for MCP use:
[skills/software-development/github/](skills/software-development/github/),
whose `MCP.md` defines how its workflows map to MCP tools, prompts, and
resources. Everything else in this repo is agent instructions (SKILL.md
playbooks for an agent with tools), not MCP tools, and must not be served
as MCP tools without a mapping of its own.

## Publishing

A redacted snapshot publishes to the
[public mirror](https://github.com/David2024patton/custom-skills-public)
with one command from the private repo:

```bash
bash scripts/publish-public-mirror.sh
```

What the publish gate actually does, stated plainly: a maintained blocked
list of known private values is stripped and scanned for, pattern scans
look for credential and identifier shapes, and gitleaks scans the staged
tree against a documented baseline. Content the blocked list names is
dropped first, and index files are pruned of stale lines. That is a
maintained list plus scanners, not a guarantee: an identifier that is not
on the list and does not match a scanned shape can pass, which is why any
file new to a snapshot also gets a human read before it publishes. The
redaction map and the scope list live only in the private repo's
`scripts/` and never enter a snapshot.

For the release history and snapshot record, see [CHANGELOG.md](CHANGELOG.md) and [SNAPSHOT.md](SNAPSHOT.md). Pin a snapshot tag, do not track a moving branch.

## Provenance and upkeep

The working copies on the Muse VM live in `~/workspace/custom-skills/`.
This repo is the tracked home. When a skill changes, update both.
