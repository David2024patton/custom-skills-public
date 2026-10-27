---
name: critic-lens-ux
description: "Use when skeptic reviews web, app, or UX work."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
  hermes:
    tags: [critic, ux, usability, accessibility, web-performance, design-review]
    related_skills: [persona-skeptic, dogfood, flutter, popular-web-designs]
---

# Critic Lens: Web, App, UX, and Design

## When to Use

This lens is a checklist every critic carries: in a Critic family run, all five full-spectrum critics load it alongside `persona-skeptic` and work it in full, on every artifact, whatever the artifact type. On artifacts of its shape (a screen, flow, wireframe, live site, or design), this lens's findings lead the merged report. On an artifact with no UI surface, every critic works this checklist against what exists and reports the surface absent. This lens attacks from the position of the real user and the platform constraints, not the designer's intent.

## Nielsen's 10 usability heuristics (the standing checklist)

For every screen or flow, walk all ten and note violations by severity:

1. **Visibility of system status.** Does the user know what is happening after every action. Loading, saving, errors, empty states.
2. **Match between system and real world.** Language the user uses, not internal jargon. Familiar sequences.
3. **User control and freedom.** Undo, cancel, back, escape from any state. No trapped user.
4. **Consistency and standards.** Same action same place everywhere. Platform conventions honored. Brand casing exact.
5. **Error prevention.** Constraints before validation. Confirmation on destructive acts.
6. **Recognition rather than recall.** Options visible, not memorized. Context and defaults present.
7. **Flexibility and efficiency of use.** Shortcuts for experts, guidance for novices.
8. **Aesthetic and minimalist design.** Nothing competing for attention. No decorative clutter.
9. **Help users recognize, diagnose, recover from errors.** Plain language, no raw backend errors or JSON on screen, a way forward.
10. **Help and documentation.** Searchable, task-focused, minimal.

## Accessibility (WCAG 2.2, non-negotiable for David)

- Semantic structure, correct heading order, labeled controls.
- Keyboard operable end to end. Visible focus. No keyboard traps.
- Contrast ratios at threshold. Text that scales without clipping.
- Images with alt. Videos with captions. Forms with associated labels and error association.
- Every state visible to a sighted user has a screen-reader path.

## Real-user path audit

- Walk desktop, tablet, and phone widths. Clipped text, overlap, overflow, horizontal scroll, invisible fonts.
- Every loading, empty, error, success, disabled, and long-content state.
- Click every link, button, form, and route. No dead ends, no console errors, no 404s.
- Role separation where it applies: admin, agency, and customer shells must look like different products; no role sees another's data.

## Web performance (Core Web Vitals)
- LCP, INP, CLS. Slow first paint, janky interaction, layout shift.
- Unbundled assets, render-blocking resources, runtime CDN fetches for text or fonts (a build that depends on one is not done).

## What the UX skeptic always demands

- **Evidence from the real thing.** A screenshot or a live walkthrough, not a description of the design. "It should work" is not a review.
- **The empty and error states.** Designers show the happy path. The user lives in the edge cases.
- **The 90-year-old test.** David's bar is extreme simplicity. If a capable novice cannot use it cold, it fails.

## Output additions (append to the core contract)
- **Heuristic violation ledger.** Numbered by severity, each: heuristic number, what the user hits, the fix.
- **Accessibility findings.** WCAG criterion, the barrier, the assistive tech affected.
- **Path failures.** Broken route, dead button, clipped layout, missing state.

## Failure modes this lens exists to catch

- Happy-path-only review. Desktop-only review.
- Raw backend errors or JSON leaking to the screen.
- A design that reads well in a mock and collapses on a real phone or with real long content.
- Accessibility bolted on at the end instead of designed in.

## Mandatory marketing-surface checks (website critiques)

For ANY website or landing-page critique, also scan:
- [ ] **Ad pixels / conversion tracking** (Meta, TikTok, LinkedIn, Google, server-side CAPI, dedup, GTM, consent). Use skill `ad-tracking-pixels` for the full checklist. Missing or browser-only tracking is a real conversion gap.
- [ ] **Local business listing / social presence** (if the site belongs to a local business): Google Business Profile completeness + currency, Facebook/Instagram/LinkedIn presence, NAP consistency. Use skill `social-presence-audit`.
Do not return a website verdict while skipping these: an attractive page that cannot measure conversions, or a business with a stale Google listing, is not actually done.

## Refinement pass additions (P-18)

- **Safety levels (CS-13).** Live-surface walks run under the declared environment level (L1 to L4) and action classes (A0 to A5, A5 forbidden everywhere). Any action above read passes the four-point write gate (location, audience, undo, ledger) and lands in the run ledger with its before-value.
- **Hidden-writes catalogue.** Autosave, toggles, drag, read receipts, and persisted view changes are writes. Audit every walked path for them; a "we only read" claim about a session that touched them is FALSE.
- **Barriers (CS-14).** Product-shaped artifacts get ship-readiness barriers in the report (category, what it blocks, severity, evidence); a blocks-launch barrier caps the verdict at fix-first.
- **Not tested.** This lens's return ends with a Not tested list.
