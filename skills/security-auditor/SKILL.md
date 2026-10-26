---
name: security-auditor
description: Use before shipping: audit code for vulns and new exploits.
version: 1.0.0
license: MIT
hermes:
 tags:
 - security
 - audit
 - threat-intel
 - vulnerabilities
 - multi-tenant
 - code-review
---

# Security Auditor

Deep, repeatable security audit methodology for Hermes agents. Run it before shipping code, before infra changes, and whenever an owner asks "is this safe to expose". Two halves always travel together: a live threat intel refresh at the start of every run (section 1), and a fixed audit procedure (section 2) covering the same ground every time so nothing depends on the auditor's mood. The case study, playbooks, and verification rules support those two.

## 0. Ground rules for every run

- **Snapshot rule (read first):** the knowledge in this file is a snapshot of research performed on 22 October 2026. It is a starting point, never the answer. The live refresh in section 1 is the authoritative source each run, because advisories, exploited-in-the-wild status, and patched version numbers change within hours of publication.
- **No invented facts.** Every CVE ID, advisory, version number, and exploit claim in a report must carry a URL you actually fetched this run (`web_search`, `web_extract`, or `curl`). If you cannot fetch it, label it "unverified" or drop it. Never recall a CVE ID from memory.
- **Brand casing is exact and never normalized:** AlphaFlux, AlphaVision, AlphaSafe, iTaK, Patriot Pest Control. Same rule in code comments, reports, commits, and tickets.
- **Report hygiene:** plain ASCII only, no em dash characters, no smart quotes. Machine-parsed reports break on exotic punctuation.
- **Severity honesty:** never downgrade a finding to make a scan look green. The no-red law lives in the companion `commit-gates` skill; this skill defers to it rather than duplicating it.
- **Scope note:** AlphaFlux is multi-tenant. Every AlphaFlux run includes the route-by-route tenant isolation sweep in phase 6, no exceptions, even for "tiny" changes.

---

## 1. THREAT INTEL REFRESH (MANDATORY STEP 1 OF EVERY RUN)

Do this before opening a single source file. If the refresh fails or is skipped, the report opens with `THREAT REFRESH: INCOMPLETE (reason)` and every "pass" in it is provisional.

Why it is mandatory: vulnerability state moves faster than skill files. A dependency clean last week may now be in CISA KEV with ransomware use; an advisory may have gained a public exploit; a "fixed" version may have been reverted. The refresh closes that gap with evidence fetched today.

### Sources to query, in order

1. **NVD:** `https://nvd.nist.gov/vuln/detail/<CVE-ID>` for a specific ID; recency queries via `https://services.nvd.nist.gov/rest/json/cves/2.0?pubStartDate=<start>&pubEndDate=<end>&resultsPerPage=200` (120-day window max), filtered locally against inventory keywords.
2. **GitHub Security Advisories / GHSA:** `https://github.com/advisories?query=<package>` per direct dependency, or the advisory GraphQL API with a token. Cross-check **OSV** (`https://api.osv.dev/v1/query`, POST the lockfile-derived package list), which aggregates GHSA, Go, PyPI, npm, crates, Maven, Packagist.
3. **CISA KEV** (what is actually exploited): `curl -sL -o kev.json https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`, then read `catalogVersion`, `dateReleased`, `count`; diff `count` against your previous run and match new entries against inventory by vendor/product text.
4. **Vendor advisories** (authoritative for patched versions): the vendor page for every runtime in inventory, for example `https://www.php.net/archive/2026.php` for PHP, plus Go, Node.js, Rust, Python, database, web server, and hosting panel vendors.
5. **Project feeds** (earliest signal): oss-security (`https://www.openwall.com/lists/oss-security/`), RustSec advisory-db (`https://github.com/rustsec/advisory-db`), Go vulndb (`https://vuln.go.dev/`), and the project's own Dependabot/Renovate feed.
6. **Unbiased multi-engine search:** the owner's SearXNG at `https://search.itak.live/` aggregates multiple engines without a personalization bubble. Use its HTML endpoint with a browser User-Agent:
 `curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36" "https://search.itak.live/search?q=<query>+<cve>&format=html"` with queries like `"<CVE-ID>" exploit` or `<vendor> security advisory <month year>`.
7. **`web_search` / `web_extract`** as the general fallback for anything the direct endpoints do not answer.

### What to do with the results

- Build `[(advisory, affected component in THIS project, fixed version, source URL, fetched_at UTC)]` and map each item to the phase 1 inventory: no match becomes "not applicable (reason)", a match becomes a finding or an urgent patch task.
- Record feed freshness (`KEV catalogVersion 2026.10.21, fetched 2026-10-22T15:19Z`, `NVD last modified <date>`). Not decoration: a clean scan is only as good as the last update time of its feed.
- Paste the snapshot block into the report under `## Threat intel refresh (YYYY-MM-DD HH:MM UTC)`.
- If sources disagree (score, affected versions, exploit status), trust the primary vendor/project advisory and state which source was authoritative and why.

---

## 2. AUDIT PROCEDURE (RUN EVERY TIME, IN THIS ORDER)

Cheap whole-repo signal first; route-by-route work after inventory is known. Do not skip phases because a previous run was clean; re-run them and capture fresh output.

### Phase 1: Scope and inventory

Enumerate languages, frameworks, runtimes, services, containers, IaC, and third-party integrations (`git ls-files` by extension, lockfiles, Dockerfiles, compose files, CI configs, `ss -tulpn` for listeners when you have shell access). Note exposure: internet-facing vs internal, multi-tenant (AlphaFlux) vs single-tenant. Output: a component table every later phase references.

### Phase 2: Secrets in code AND in git history (gitleaks)

Secrets live in history long after they are deleted from HEAD. Scan both.

```bash
# Working tree + full history (v8 detect scans the commit history)
gitleaks detect --source . --redact --report-format json --report-path gitleaks-report.json
# Files only, for non-git directories
gitleaks dir --source . --redact --report-path gitleaks-dir.json
# Optional second engine for disagreement checking
trufflehog git file://. --only-verified
```

Treat every hit as live until proven otherwise: when it was committed, whether it still works, who can read the repo (visibility, fork policy, CI token scope). Also look where scanners do not: tracked `.env` files, test fixtures with real keys, config screenshots in docs, inline passwords in deploy scripts, cloud credentials in CI variables. Findings feed playbook 4.1: rotation first; history purge decision is the owner's.

### Phase 3: Dependency vulnerabilities, per stack

| Stack | Command |
|---|---|
| Go | `govulncheck ./...` |
| Rust | `cargo audit` (cargo-audit) |
| JavaScript/TypeScript | `npm audit --audit-level=high` (also `pnpm audit`, `yarn audit`) |
| Python | `pip-audit -r requirements.txt` (or against the active venv) |
| PHP | `composer audit` |
| Ruby | `bundle audit --update` |
| Java | OWASP Dependency-Check |
| .NET | `dotnet list package --vulnerable` |
| Elixir | `mix hex.audit` |

Interpretation rules: mark direct vs transitive (it changes the upgrade path, playbook 4.2); reachability is not a pass, so "we never call that function" needs evidence or stays a finding; an advisory fixed in the registry but not in the lockfile is still open; dev-only dependencies still count in CI or on machines with credentials (label `dev-dependency`).

### Phase 4: Container and infrastructure scan (trivy or equivalent)

```bash
trivy fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL .
trivy image --severity HIGH,CRITICAL --ignore-unfixed <image>:<tag>
trivy config . # IaC misconfiguration: Dockerfiles, compose, Terraform
```

Check by hand what scanners miss: mutable `FROM` tags, running as root, excess capabilities, secrets in layers, build tools left in the image; and orchestration exposure (published ports, host networking, privileged mode, writable rootfs, wildcard volume mounts). Name the tool and version behind any output (Docker Scout, Grype, Clair, Wiz are fine equivalents).

### Phase 5: Authentication and authorization review

Walk every auth flow with controls and code/config evidence: session issuance, rotation, expiry, invalidation on password and privilege change, token storage, replay resistance; password storage (modern KDF, per-user salt); rate limits on login/reset/OTP; no user enumeration; recovery no weaker than the login it protects; service-to-service auth on internal endpoints; TLS with no HTTP fallback; no secrets in URLs or client-side storage. Output: a flow list marked pass/fail with evidence.

### Phase 6: Tenant isolation, swept route by route (AlphaFlux and any other multi-tenant system)

Do not sample. Enumerate every route from the route registry, OpenAPI spec, or router files, then evaluate each with this checklist:

1. Identity comes from the verified session/JWT, never from client-supplied `tenant_id`, `org`, `account`, or header.
2. Every object fetch is scoped in the query itself (`WHERE tenant_id = $session_tenant`), not filtered after loading.
3. Update and delete statements carry the tenant predicate too (no read-scoped-then-blind-write).
4. Cache keys, ETags, and CDN variants include the tenant identifier.
5. Async work (queues, cron, webhooks, exports, email jobs) carries tenant context explicitly; a job that falls back to "no tenant filter" is a finding.
6. Search, autocomplete, and reporting apply tenant filters server-side, including pagination cursors.
7. File storage paths and object keys are unguessable per tenant and authorized on read, not just on write.
8. Admin, support-impersonation, and cross-tenant tools are authenticated, authorized, and audited.
9. Error behavior is consistent: a foreign resource returns the same 404/403 shape as a nonexistent one, so existence cannot be probed.
10. Rate limits and quotas are keyed per tenant, so one tenant cannot starve or brute-force another.

Output: a matrix `route | authn | tenant predicate (file:line) | evidence | verdict (pass/fail/not tested)`. Any `not tested` row is coverage debt, never a silent pass. Probe at least one request per route family with a two-account setup (tenant A token against a tenant B object) and attach the request/response.

### Phase 7: Injection

- SQL/NoSQL: parameterized queries or a genuinely parameterizing ORM; check string concatenation, `ORDER BY`/table-name interpolation, JSON paths.
- OS command: `exec`, `system`, backticks, `subprocess` with `shell=True`, template filters that shell out, archive extraction filenames.
- Template injection (SSTI): user input rendered as template code rather than data.
- Deserialization: `pickle`, `yaml.load`, `unserialize`, `readObject` on attacker-influenced data.
- Path traversal/file inclusion: normalize and allowlist; zip-slip in archives.
- Header/log/CSV formula injection; LDAP/XPath/expression-language injection where those stacks exist.
- Evidence per finding: sink at `file:line`, untrusted source, path between them.

### Phase 8: SSRF

Outbound request features: URL fetchers, webhook targets, import-from-URL, PDF renderers, link previews, configurable health checks. Verify a strict host/scheme allowlist (not a denylist), no redirects to internal addresses, DNS resolved-and-checked at request time (defeats rebinding), blocks for link-local and cloud metadata ranges (169.254.169.254, IMDSv2 hop protection), and no credential leakage in forwarded headers. Evidence: one request that makes the server fetch an internal address, or code proving it cannot.

### Phase 9: CSRF

Every state-changing request: token or strict Origin/Referer validation, appropriate `SameSite` posture, no side effects from GET. Findings include cookie-only auth on JSON APIs, wildcard CORS with `credentials=true`, and a cookie-borne token with no CSRF defense. Cover login, logout, password change, and uploads; consider second-order flows (change an email, then use it).

### Phase 10: XSS

Reflected, stored, and DOM-based paths. Check sinks (`innerHTML`, `document.write`, `insertAdjacentHTML`, `eval`, `dangerouslySetInnerHTML`, `| safe`, `{!! !!}`) and whether output encoding or autoescaping is actually on. Rich-text sanitizers must be allowlist-based; CSP should carry a nonce rather than `'unsafe-inline'`. Evidence: exact input, render point, and the executed payload or a test asserting encoding.

### Phase 11: Broken access control

IDOR/BOLA on every object ID; forced browsing to unlinked admin routes; missing function-level checks (the UI hides the button, the API still obeys); privilege escalation via role parameters, mass assignment, or tenant-admin vs platform-admin confusion; HTTP method override and path normalization tricks (`/admin/../admin`); wildcard CORS; multi-step flow bypass by calling a later endpoint directly.

### Phase 12: Rate limiting and abuse

Verify limits on login, password reset, OTP/MFA, registration, expensive search/report endpoints, file uploads, webhook fan-out, and credit/quota actions. Confirm keying (per IP, per user, per tenant), burst vs sustained behavior, `429` responses, and that limits hold across workers (shared store, not per-process memory). Evidence: a burst that trips the limit, or config plus a live test showing it does not.

### Phase 13: Logging without secret leakage

Verify logs never contain passwords, tokens, session IDs, cookies, full `Authorization` headers, API keys, payment data, or unnecessary PII, across application logs, access logs that record bodies, debug dumps, and error-reporter payloads (Sentry-style captures often include locals and headers). Verify audit logging exists for security-relevant events: auth successes/failures, permission denials, tenant-scope decisions, admin actions, secret access; without them playbook 4.4 is impossible. Verify log integrity: timestamps with timezone, attacker-controlled control characters neutralized (log injection), redaction applied at the source rather than hoped for downstream.

### Phase 14: Verification and regression

For every fix proposed or applied: re-run the exact command or request that failed, attach the new output, keep the failing one for the record. Run the project's own lint, typecheck, and test suite after changes; the companion `commit-gates` skill owns the no-red law, so hand the final gate check to it rather than inventing a second one.

---

## 3. REPORT FORMAT (PER FINDING)

Exactly these five fields, in this order, for every finding:

```
### [SEVERITY] Short descriptive title
- Severity: Critical | High | Medium | Low | Info (include CVSS vector + source URL if you scored it)
- Location: path/to/file.ext:123
- Exploit path: preconditions -> steps -> impact, written as an attacker would execute it
- Evidence: verbatim command output or request/response, with command line and timestamp
- Fix: concrete change (code/config), plus the regression test that keeps it fixed
```

Severity definitions: **Critical** = unauthenticated RCE, auth bypass, or full cross-tenant data disclosure; **High** = authenticated RCE, privilege escalation, or cross-tenant access to sensitive data; **Medium** = limited information disclosure or abuse needing preconditions; **Low** = hardening gap with no direct path; **Info** = observation or coverage debt.

The report also carries run metadata (UTC time, tool versions, feed freshness), the threat intel snapshot block, a findings summary sorted by severity, coverage notes (what was `not tested`), and open questions for the owner.

---

## 4. RESPONSE PLAYBOOKS

### 4.1 Secret found in git history

1. Capture evidence first: path, commit hash, first commit date, repo visibility, and whether the credential still validates (auth check only, nothing more).
2. Rotate immediately; assume compromise from the moment it entered shared history. Revoke, reissue, then review audit logs for use since the first commit date.
3. **History purge decision is the owner's, never the auditor's.** Present both options with consequences: (a) rotate only, keep history: simplest, safe once rotated, right for short-blast-radius secrets; (b) purge (`git filter-repo` or BFG): force-push, every collaborator re-clones, open PRs and local branches invalidated, CI caches and deploy keys may need reset.
4. Prevent recurrence: `gitleaks protect --staged` pre-commit hook, CI gate on every push, `.gitignore` for env files.
5. Report the rotation (with timestamp) and the owner's purge decision.

### 4.2 Vulnerable dependency

1. Take the fixed version from the advisory URL you fetched; check whether the vulnerable path is reachable in your usage.
2. Upgrade path: smallest bump containing the fix, changelog read for breaking changes, lockfile updated; for a transitive dependency decide between a parent bump or a pinned override.
3. Regression test: run the full suite plus targeted tests around the changed surface, because the point of the upgrade is proving behavior did not move. Attach suite output.
4. No fixed version: compensating control (disable the feature, WAF rule, input restriction, isolation), documented as temporary, with a re-test date.
5. Close with advisory URL, version before/after, and test output.

### 4.3 Exposed service

1. Enumerate reality: `ss -tulpn` (or `netstat -tulpn`) plus container port publishing (`docker ps`), against documented intent.
2. Host firewall (`ufw` as the common case): `ufw status verbose` and `ufw status numbered`; default inbound deny; only intended ports allowed (80/443, SSH from an allowlist or jump host); newly found allows get `ufw deny <proto>/<port>` plus a note on who added them. Re-verify from outside (`nmap -Pn -sV <host>` from a second machine) and attach that output.
3. Traefik/reverse proxy: routers bound to intended entrypoints only; no internal service reachable by guessing a `Host()` header; `exposedByDefault` off; dashboard not publicly routable; middleware IP allowlist and admin auth in place; TLS valid and not wildcarded over the wrong domain; dynamic config sources (docker labels, file provider) not influenceable by a tenant or untrusted container.
4. Cloud and edge: security groups, load balancer target scope, CDN/WAF rules. Provider console is ground truth unless IaC was just reconciled.
5. Close only after an external re-scan shows the service closed, output attached.

### 4.4 Suspected active exploitation (for example a critical runtime RCE such as PHP2Shell)

1. Isolate first if you cannot patch immediately: take the internet-facing service offline or behind network-level authentication. Patching immediately is always the preferred branch; isolation is the fallback, not a second choice.
2. Preserve logs before changing anything (web/WAF, application error, auth), plus current process tree (`ps -ef`) and outbound connections (`ss -tnp`).
3. Hunt the advisory's indicators (section 5.5 has the PHP2Shell list): odd multipart uploads to endpoints that never accept uploads, memory-exhaustion error spikes, worker segfaults, shells or downloaders spawned by worker PIDs, new files under web roots, unexpected outbound destinations from service accounts.
4. Rotate credentials that could have resided in process memory (session signing keys, API tokens, application DB passwords).
5. Report isolation/patch status, indicators checked with output, and an explicit "no evidence of compromise / evidence found" line with the time range covered.

---

## 5. CASE STUDY: PHP2Shell (CVE-2026-109618, CVE-2026-109619)

Researched live on 22 October 2026 by fetching the URLs below. This is the worked example of section 1 output, not a substitute for it; re-verify on any future run.

### 5.1 Verified facts

| Field | Value | Source fetched |
|---|---|---|
| Name | PHP2Shell (php2shell), the pair tracked together | https://www.php.net/archive/2026.php |
| CVEs | CVE-2026-109618 (RCE via OOM corruption, GHSA-w8hw-w9fx-j79w); CVE-2026-109619 (RCE via stale global state, GHSA-6wmf-4rv5-p3rp) | https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w and https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp |
| Disclosed | 21 October 2026 (release 14:00 UTC); details leaked publicly on 20 October 2026 ahead of coordinated disclosure | https://openwall.com/lists/oss-security/2026/10/21/6 and https://labs.beazley.security/advisories/BSL-A1233 |
| Severity | CVSS v4.0 9.2, Critical; CWE-416, CWE-755, CWE-824, CWE-1325 | https://nvd.nist.gov/vuln/detail/CVE-2026-109618 |
| Impact | Unauthenticated remote code execution as the web worker account over HTTP, plus process memory disclosure (credentials, API keys) | https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w and https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp |
| Fixed versions | PHP 8.5.12, 8.4.27, 8.3.36, 8.2.35 | https://www.php.net/archive/2026.php |
| EOL backports | Minimal source backports published for PHP 7.4, 8.0, 8.1; distributions and LTS vendors received patches in advance and ship their own backports; 8.1 and older get no upstream binary release | https://www.php.net/archive/2026.php and https://www.sophos.com/en-us/security-advisories/sophos-sa-20261021-php2shell |
| Exploit status | Public PoCs circulating on release day; WatchTowr, Hadrian, Patchstack, Cloudflare, Vega and Amazon reported in-the-wild exploitation attempts, some before patches landed; multiple vendors report exploitation in the wild | https://www.securityweek.com/php2shell-patches-land-as-first-exploitation-attempts-hit-sensors/ and https://www.sophos.com/en-us/security-advisories/sophos-sa-20261021-php2shell |
| Official alert | CISA urges immediate patching; had not observed exploitation at publication | https://www.cisa.gov/news-events/alerts/2026/10/21/critical-vulnerabilities-php-require-immediate-patching |
| KEV status | Absent from the KEV catalog at `catalogVersion 2026.10.21` (1754 entries), checked 2026-10-22T15:19Z; re-check every run, membership can change daily | https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json |

### 5.2 Mechanics

- **CVE-2026-109618 (OOM corruption):** PHP uses `longjmp()` to abort a request on out-of-memory. Some contexts make request memory reachable before it is fully initialized; when an allocation fails, shutdown later reads or branches on that invalid state. Multipart tricks (no usable content length, unlimited part headers, empty file controls evading `max_file_uploads`) reach OOM inside apparent limits. Apache mod_php is highest risk because it runs request shutdown even when startup failed, so an unauthenticated request hits the bug before any application code runs; FPM is treated as susceptible by source analysis, though the full exploit was demonstrated on mod_php.
- **CVE-2026-109619 (stale global state):** request-owned global state (error, session, object, extension) outlives its request, pointing at freed memory. A producer request (fatal error, OOM, upload-progress handling) publishes it; a later request on the same worker consumes it before normal initialization resets it. Confirmed paths: PHP 8.5 `fatal_error_backtraces` and session upload progress (on by default, no `session_start()` needed). Result: heap use-after-free, memory disclosure, RCE.
- **Shared root cause:** PHP could bail out mid-update of its own state and then trust the half-written state; the patch replaces OOM `longjmp()` with a delayed soft OOM plus a hard `_exit()` ceiling and resets wider request state at shutdown.

### 5.3 Escalation guidance (what to tell the owner)

1. **Patch immediately** to PHP 8.5.12, 8.4.27, 8.3.36, or 8.2.35, or to the distribution/LTS vendor package carrying the fix, prioritizing internet-facing systems (CISA says "immediately", internet-facing first).
2. **If you cannot patch immediately, isolate internet-facing PHP services until they are patched:** take them offline or behind network-layer authentication. CISA states organizations that cannot update immediately, or that run PHP 8.1 or earlier unsupported versions, should take PHP-based systems offline until they can be patched or updated. A WAF may help meanwhile but is not a fix.
3. Interim mitigations reduce specific attack paths only and never make an installation safe: `memory_limit=-1` enforced administratively, low `post_max_size`, `session.upload_progress.enabled=0`, `fatal_error_backtraces=0` on 8.5, rejecting `multipart/form-data` at the edge where uploads are unused, restarting every worker after any config change. In-process protections (RASP, app-embedded WAF agents) may never see the request on mod_php, because the trigger happens during request parsing.
4. EOL branches (7.4, 8.0, 8.1) have no upstream binary fix: apply the PHP security team's source backports, a vendor backport, or upgrade to a supported branch.

### 5.4 Detecting PHP on a host (including Docker images and third-party apps)

Inventory from runtime evidence, not asset records:

```bash
# Running processes: any of these mean PHP serves requests
ps -eo pid,user,args | grep -Ei '[p]hp(-fpm|-cgi)?|[p]hp[0-9]'
# Version from the binary itself (install paths are only a clue)
php -v ; php-fpm -v ; php-cgi -v # versioned variants too: php8.3 -v
# Installed packages
dpkg -l | grep -i php # Debian/Ubuntu
rpm -qa | grep -i php # RHEL family
apk info | grep -i php # Alpine
# Evidence from a live web request, from another machine (not the CLI)
curl -sI https://target.example/ | grep -iE 'x-powered-by|server'
# Effective config as the web SAPI sees it: CLI and FPM read different ini trees,
# so never answer "is it patched" from `php -i` alone
php-fpm8.3 -i | grep -E 'session.upload_progress.enabled|^memory_limit'
```

- **Docker images:** `docker ps` and `docker images` for inventory; `grep -RInE '^FROM[[:space:]]+php:' --include=Dockerfile .` for base images; `docker exec <container> php -v` for the truth inside; `trivy image --severity HIGH,CRITICAL <image>` to confirm. After patching, rebuild and recreate containers from the fixed base image; a restart does not load new code.
- **Third-party apps:** PHP ships inside panels and appliances (hosting control panels, CMS stacks, virtual appliances, hosted services) where prevalence is not directly observable, which CISA explicitly warns about. List every product that bundles PHP and confirm patch status with that vendor rather than assuming your own patch applied.
- **Backport caveat:** on several distributions and every EOL backport the package keeps the old version number and only the package release changes, so `php -v` alone cannot prove fix status. Verify the package changelog names CVE-2026-109618 and CVE-2026-109619, or confirm against the vendor's security notice (per-platform status tables: https://computingforgeeks.com/php2shell-cve-2026-109618-check-patch/).
- **Post-patch proof:** every PHP binary on the host (FPM, panel SCL builds, second branches) reports fixed; no process still maps a deleted library; Apache mod_php fully restarted rather than gracefully reloaded; effective `session.upload_progress.enabled=Off` read through the FPM binary; interim `memory_limit=-1` reverted; a request from another machine answered by the patched build.

### 5.5 Indicators to check (from the vendor advisory)

Review activity from 1 August 2026 onward, because reporting suggests the flaws may have been known to third parties before disclosure: multipart `form-data` POSTs to endpoints that do not normally accept uploads and requests containing `PHP_SESSION_UPLOAD_PROGRESS` (many CDNs do not log bodies, so use WAF or app-layer logs); spikes in memory-exhaustion errors or worker segfaults; child processes spawned by PHP or the web server; new or modified PHP files under web roots; outbound connections from PHP processes to unexpected destinations; successful administrative logins to affected applications since 1 August 2026.

---

## 6. VERIFICATION MINDSET

- **Every pass or fail claim carries command output:** command line, tool version, timestamp, and output (or exit code plus an explicit "0 findings" line). Findings carry failing output; fixes carry re-run output.
- **A clean scan is only as good as the last update time of its feed:** "no known vulnerabilities" must also say when the advisory data was last updated; if freshness cannot be established, downgrade the claim to "no findings against data fetched at <time>".
- **Untested is not passed:** phases you could not execute (no staging access, tool unavailable) go in a coverage section listing what is unverified and how to close it.
- **Two-source rule for versions:** the vendor advisory and a live check of the deployed artifact (binary, package, image) must agree before a component is marked patched.
- **Do not double up on the commit gate:** the companion `commit-gates` skill owns the no-red law (no change lands with failing gates). This skill feeds it findings; it does not re-implement gate logic.
- **Re-run the refresh before finalizing** if the audit ran hours long during an active disclosure window (PHP2Shell-scale events move within hours).

Every URL cited in this file was fetched live on 22 October 2026 (see the Source fetched column in 5.1). Fetch them again during the next run's threat intel refresh instead of trusting this list.
