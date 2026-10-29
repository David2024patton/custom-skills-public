# The lies-green register (report L1-28)

Maintained register of known ways a tool reports green while
failing, skipping, or never running. Every gate wrapper in this
library normalises raw tool exits through its own checks, never
through the raw exit alone. Each entry names its countermeasure
in this library. Add an entry in the same commit that fixes a
new mode; never delete an entry, mark it superseded instead.

| # | Mode | Countermeasure in this library |
|---|------|--------------------------------|
| 1 | govulncheck in JSON, SARIF, or OpenVEX mode always exits 0, even with findings (L1-01) | common/vuln-scan.sh: verdict from the text run; the JSON run is an artefact whose exit is ignored and whose findings are parsed |
| 2 | mutmut exits 0 even when every mutant survives (L1-21) | python/mutation.sh parses mutants/mutmut-cicd-stats.json and manufactures the failure itself below the killed threshold |
| 3 | cargo audit warning classes (unmaintained, unsound, yanked) do not fail without --deny (L1-08) | common/vuln-scan.sh runs cargo audit --deny warnings; rust/policy.sh runs cargo deny check as the policy superset |
| 4 | Stryker ships thresholds.break: null, which never fails (L1-27) | js-ts/test-quality.sh fails when a Stryker config leaves break null or unset; the deliberate library value is break 60 on named critical modules |
| 5 | cargo-nextest silently drops doctests (L1-09) | rust/test.sh always runs a separate cargo test --doc lane beside nextest |
| 6 | `mojo test` invokes a command removed from the toolchain (L1-12) | mojo/test.sh never invokes it; TestSuite files run via mojo run, and a file without the TestSuite entry point fails |
| 7 | mypy silently skipped when no config exists (L1-19) | python/lint.sh runs the type gate unconditionally; a configured-but-missing binary is exit 2 |
| 8 | A project lint script passes with no rules configured, or warnings pass green (L1-22) | Web lint gates require a flat eslint.config.* for gate-owned runs and invoke with --max-warnings 0; a lint script that cannot be shown to run type-checked rules is a finding in js-ts/lint.sh |
| 9 | A dead `next lint` fallback invokes a removed command (L1-25) | nextjs/lint.sh never invokes next lint on any version; ESLint runs directly |
| 10 | Ruff missing used to fall back to pyflakes, a weaker check wearing the gate's name (L1-19) | python/lint.sh: Ruff missing is exit 2; the fallback is deleted |
| 11 | A secrets step that greps patterns and calls itself a scan (L1-30) | common/secrets-scan.sh: no scanner binary means DID-NOT-RUN, exit 2; the grep fallback is retired |
| 12 | A Prisma schema change shipped with no migration looks green to every code gate (L1-26) | prisma/migrate-check.sh: pure-git check fails a schema change with no accompanying migration |
| 13 | A coverage tool reporting a number with no threshold attached (L1-06, L1-10, L1-17, L1-20) | Coverage gates in this library parse the report and compare against a ratchet themselves; a number without a set break point is decoration, not a gate |
| 14 | osv-scanner offline mode records no database freshness (Cluster B) | Reports must stamp feed age; a clean result on stale intel is NO-FINDINGS-ON-STALE-INTEL, never PASS |

Exit semantics reminder: 0 pass, 1 fail, 2 tool missing or
did-not-run. A tool that cannot run is never a pass.
