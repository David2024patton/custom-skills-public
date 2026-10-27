---
name: "playwright"
description: "Drive a real headless Chromium with Playwright from this VM: screenshots, clicks, mobile viewport emulation, console error capture. Use when you need to see or interact with a live page, verify a UI change, or test desktop and mobile layouts."
author: David Patton
license: MIT
---

# Playwright

## Purpose

Scripted browser control on this VM for visual verification and interaction
testing: load a page, click through flows, emulate a mobile viewport, capture
screenshots and console errors. Faster and more precise than delegating to the
managed browser when you need pixels or DOM-level assertions.

## Tooling

- Python venv with Playwright installed: `~/workspace/.venvs/pw`
  (run scripts with `~/workspace/.venvs/pw/bin/python`; helpers re-exec
  into it automatically)
- Chromium binary: `/opt/meta-chromium/chrome` (system install; the
  Playwright CDN is blocked by the egress gateway, so `playwright install
  chromium` cannot fetch its own build)
- Egress: all traffic must go through the gateway proxy. Chromium cannot do the proxy auth handshake here. The proxy forwarder helper and the launch helper (`bin/localproxy.py` and `bin/pwutil.py`) live only in the operator's private copy and are not part of this published skill; in a private copy, `bin/shot.py` starts the forwarder automatically. In this published copy, configure the proxy yourself from the environment (for example a `PLAYWRIGHT_PROXY` value the operator sets) and pass it to the launch call below.
- Quick screenshot helper: `python3 ~/workspace/skills/playwright/bin/shot.py
  <url> <out.png> [--mobile] [--full] [--width W] [--height H] [--wait MS]`
  (`--mobile` emulates an iPhone 15 with touch)

## Launch pattern

Copy this block to start any script. Credentials never touch disk; the
forwarder reads them from the environment at runtime.

```python
import sys, os
from playwright.sync_api import sync_playwright

# In the operator's private copy, a local pwutil helper performs this launch
# through the local forward proxy. Here, launch directly and pass a proxy
# from the environment when one is configured.
_launch = {"executable_path": "/opt/meta-chromium/chrome", "headless": True,
           "args": ["--no-sandbox", "--ignore-certificate-errors"]}
if os.environ.get("PLAYWRIGHT_PROXY"):
    _launch["proxy"] = {"server": os.environ["PLAYWRIGHT_PROXY"]}

with sync_playwright() as p:
    browser = p.chromium.launch(**_launch)  # headless Chromium
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    # mobile: ctx = browser.new_context(**p.devices["iPhone 15"])
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.goto("https://example.com", wait_until="networkidle", timeout=45000)
    page.wait_for_timeout(1500)
    page.screenshot(path="/tmp/shot.png")
    browser.close()
```

Why these flags: `--no-sandbox` (root in container), `--ignore-certificate-errors`
(the gateway does TLS interception; curl trusts its CA, Chromium does not),
`executable_path` (Playwright's own Chromium cannot be downloaded here).

## Recipes

- **Click test**: `page.click("text=Log in as")`, then assert with
  `page.locator(".help-banner").is_visible()` or read `page.content()`.
  Prefer text locators over brittle CSS.
- **Auth-gated pages**: for the AlphaFlux console the login is passwordless
  OTP to the user's phone. David's standing preference is that the agent
  pulls the SMS code from the paired phone's texts itself (see the login notes in the operator's private copy;
  `references/login.md` is excluded from this published copy).
- **Waiting**: prefer `page.wait_for_selector(...)` or
  `page.wait_for_function(...)` over fixed sleeps for state changes.
- **Full-page docs**: `page.screenshot(path=..., full_page=True)`.

## Operating Rules

1. Never hardcode proxy credentials or any secret in a script or skill file.
   They live in the environment only.
2. Headless only. There is no display on this VM; `headless=True` always.
3. Do not use Playwright to bypass sign-in or abuse a site. Same rules as the
   managed browser: act only on the user's own services with their approval,
   keep request volume human-scale, stop on 429/403 rate-limit signals.
4. Screenshots are evidence, not decoration. Save them under `/tmp` for
   throwaway checks or `~/workspace/` when the user should keep them, and
   look at them with the read tool before claiming a visual result.
5. `browser.search` / `browser.open` are still the right tools for quick text
   lookups. Reach for Playwright when you need rendering, interaction, or a
   mobile viewport.
