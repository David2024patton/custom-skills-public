---
name: ui-visual-check
description: "Use to browser-test a UI and screenshot every state."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
  hermes:
    tags: [ui, visual, browser, screenshots, accessibility, qa]
    related_skills: [critic-lens-ux, dogfood, persona-skeptic, flutter]
---

# UI Visual Check: The Real-Browser Gate

## When to Use

Run this on anything with a screen after the code critic passes, and before ship. It is required even when the code is clean, because clean code can still render a broken screen. Its screenshots go in the report so David sees and approves the result himself.

## The check (ordered, nothing skipped)

1. **Launch the real app in a real browser.** Not a description, not a mock, the running app. Use the stack's run command plus a browser driver. If it will not boot, that is a finding, not a blocker to work around.

2. **Sign in as a real user.** Walk the actual authenticated flow, not a static page load.

3. **Every width.** Desktop, tablet, and phone. Screenshot each. Look for overlap, clipping, overflow, horizontal scroll, invisible fonts, broken layout.

4. **Every control.** Click every link, button, form, and route. No dead ends. No console errors. No failed network requests. Capture the browser console and network log.

5. **Every state.** Screenshot loading, empty, error, success, disabled, and long/odd content. Designers ship the happy path; the user lives in the edge cases.

6. **Accessibility pass.** Semantic structure, heading order, contrast, keyboard operability end to end, visible focus, no keyboard traps, labeled controls, alt text, screen-reader path for every sighted-only state.

7. **Role separation where it applies.** Admin, agency, and customer shells are different products and must look it. Confirm no role sees another's data.

8. **The 90-year-old test.** David's bar is extreme simplicity. If a capable novice cannot use it cold, it fails regardless of what the code says.

## Output

- A report folder of timestamped screenshots, one per screen per state per width.
- A console and network error log, or an explicit clean statement.
- A findings list by severity, each with the screenshot that proves it.
- The go-ahead only when every state is captured AND clean, or the defects are listed for the owning persona to fix and re-check.

## Failure modes this exists to catch

- Reviewing a mock or a description instead of the running app.
- Happy-path-only and desktop-only review.
- Raw backend errors or JSON leaking to the screen.
- Accessibility bolted on at the end instead of designed in.
- A go-ahead with no screenshots, so David cannot see what he is approving.

## Tooling

Use the browser tooling available in the runtime (headless or headed), drive real clicks and navigation, capture screenshots to disk, and read the console via the driver. For Flutter web, test both engines where they ship. Wire the screenshot folder into the run's report directory.
