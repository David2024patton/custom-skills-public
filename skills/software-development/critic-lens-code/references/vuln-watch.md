# Vulnerability Watchlist (seed snapshot)

Seed date: 2026-10-27. This file is a SEED SNAPSHOT, not a live feed.
It is never current on its own. Before any scan, every critic must
refresh current vulnerability knowledge for the artifact's stack via
live research and update its working copy of this list (see the refresh
step in the critic-lens-code SKILL.md). The refresh applies to all five
critics in a family run, not to a designated code critic. An item below proves only what
its source stated on the date verified. If a detail is not in the
source, it is not in this file.

How to read an entry: name and identifier as the source states them,
affected stack and versions as stated, how a critic checks for it, the
source name, and the date verified in this repo.

## 1. PHP2Shell: CVE-2026-109618 and CVE-2026-109619 (PHP)

- What: Two critical flaws in the PHP interpreter itself. Per the PHP
  Group coverage, both can allow unauthenticated remote code
  execution. CVE-2026-109618 is an out-of-memory handling error that
  can leave request memory only partly initialized;
  CVE-2026-109619 is internal request state surviving after its
  memory is freed (stale global state, use-after-free class). Both
  carry a CVSS v4.0 score of 9.2 as stated by the PHP Group.
- Discovery as reported: security firm Calif found the flaws using
  OpenAI's GPT-5.6 Sol under OpenAI's Patch the Planet initiative;
  Wiz independently found them using Gemini 4 Argon and GPT-5.6 Sol.
- Affected as stated: every PHP release before the fixed releases in
  its branch, in installations serving web requests (PHP-FPM, Apache
  with mod_php, php-cgi, FrankenPHP, LiteSpeed named). mod_php is
  rated highest risk. Fixed releases, released 2026-10-21:
  PHP 8.5.12, 8.4.27, 8.3.36, 8.2.35. PHP 8.1 and older receive no
  project release; minimal source backports for 7.4, 8.0, and 8.1
  were prepared as stated.
- Status as stated: CISA added both to its Known Exploited
  Vulnerabilities catalog on 2026-10-26.
- How a critic checks: run `php -v` on every runtime, container
  image, and host that serves web requests; anything below the fixed
  release for its branch is a Critical finding. Check the version
  the web server actually loads, not just the CLI binary. Grep
  Dockerfiles, CI images, and hosting panels for pinned PHP tags.
  Updating is the only complete fix as stated; session upload
  progress off is a stopgap only, not a fix.
- Sources: USA TODAY (2026-10-21 live coverage, PHP Foundation and
  OpenAI statements), The Hacker News (CISA confirms active
  exploitation of PHP2Shell flaws, October 2026), DEV Community
  summary of the PHP advisories (CVE-2026-109618 and
  CVE-2026-109619: what to check and how to update).
- Verified: 2026-10-27.

## 2. Brotli decoder flaw: CVE-2026-111497 (Node.js, Python, PHP on Windows, Bun, other Brotli embedders)

- What: An out-of-bounds write in Google's Brotli decoder: a crafted
  Brotli stream can corrupt decoder memory, leak sensitive memory,
  crash the process, or potentially run arbitrary code, per the NVD
  entry as reported. Also tracked as Broccoli2Shell, HTTP2Shell,
  and Node2Shell in coverage. Rated 9.2 in the siliconnoon summary
  of the advisory data.
- Discovery as reported: reported by OpenAI Codex Security
  researchers Khai Tran and Sylvie Mayer.
- Affected as stated: Google Brotli versions 1.0.3 through 1.0.9,
  1.1.0, and 1.2.0; fixed in Brotli 1.0.10, 1.1.1, and 1.2.1.
  Node.js fixed in 22.23.4, 24.22.1, and 26.12.1 (released
  2026-10-21); Node.js 20 is end of life and gets no fix. Bun
  patched in 1.4.4. Python packages Brotli and brotlicffi carry the
  same decoder per the GitHub advisory GHSA-9v8h-qqgm-4m35 as
  reported. PHP Windows builds 8.5.12-1, 8.4.27-1, 8.3.36-1, and
  8.2.35-1 address it where the cURL extension does automatic HTTP
  response decompression; Go-cgo bindings inherit the bug from the
  same C source per the Broccoli2Shell census.
- How a critic checks: any artifact that decompresses Brotli data
  it did not produce is in scope, including HTTP clients that
  auto-decode a `Content-Encoding: br` response and servers that
  parse compressed request bodies. Run `node -v` on every runtime
  and image; check Python environments for the Brotli and
  brotlicffi packages and their versions; check vendored or cgo
  Brotli copies, which no package audit of the top-level project
  will surface. Rebuild containers and standalone executables on
  the fixed runtime; a patched binary on disk does nothing for a
  process still running the old one.
- Sources: The Hacker News (CISA confirms active exploitation
  article, Brotli section, October 2026), The Tech Lane
  (HTTP2Shell: CVE-2026-111497, citing the Node.js October 2026
  security release notes and the NVD entry), siliconnoon
  (CVE-2026-111497: patched in Node, Bun, Envoy).
- Verified: 2026-10-27.

## Refresh log

- 2026-10-27: seed created with the two items above, each verified
  from the named sources on this date.
