#!/usr/bin/env python3
"""Screenshot helper: shot.py <url> <out.png> [--mobile] [--full] [--width W] [--height H] [--wait MS]

Launches Playwright Chromium headless through this VM's egress proxy and
saves a screenshot. Starts the local auth-injecting forward proxy on
127.0.0.1:18080 if it is not already running. Proxy credentials come from
the environment at runtime; nothing secret is written to disk.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pwutil  # noqa: E402  (re-execs into the venv python if needed)

from playwright.sync_api import sync_playwright  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("out")
    ap.add_argument("--mobile", action="store_true")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--wait", type=int, default=1500, help="ms to wait after load")
    args = ap.parse_args()

    with sync_playwright() as p:
        browser = pwutil.launch(p)
        if args.mobile:
            ctx = browser.new_context(**p.devices["iPhone 15"])
        else:
            ctx = browser.new_context(
                viewport={"width": args.width, "height": args.height})
        page = ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(args.url, wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(args.wait)
        page.screenshot(path=args.out, full_page=args.full)
        browser.close()
    print("saved %s" % args.out)
    for e in errors[:5]:
        print("pageerror: %s" % e[:200])


if __name__ == "__main__":
    main()
