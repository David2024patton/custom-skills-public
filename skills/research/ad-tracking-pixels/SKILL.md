---
name: ad-tracking-pixels
description: "Use to audit ad tracking pixels and server-side CAPI."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
  hermes:
    tags: [tracking, pixel, capi, gtm, conversion, advertising, attribution]
    related_skills: [critic-lens-ux, ui-visual-check, persona-content-marketing, ai-seo-aeo]
---

# Ad Tracking Pixels: client-side and server-side conversion tracking

## When to Use

When critiquing or auditing a website (use with `critic-lens-ux` / `ui-visual-check`), when standing up paid acquisition for a client (Patriot, AlphaFlux whitelabel customers), or when a marketing plan assumes conversions can be measured. If a business is running ads, it needs tracking; if it claims results without tracking, that claim is unbacked.

## The platform equivalents (all work the same way)

Every major ad network has a Meta-Pixel equivalent: a JS snippet in the header that drops cookies, tracks page views, listens for conversion events (form submits, checkouts), and builds retargeting audiences.

| Platform | Client-Side (browser) | Server-Side API (backend) | Standout / quirk |
|---|---|---|---|
| Meta (FB/IG) | Meta Pixel | Conversions API (CAPI) | Industry standard; deep event matching. |
| TikTok | TikTok Pixel | TikTok Events API | Tracks micro-interactions and video-to-cart heavily. |
| LinkedIn | LinkedIn Insight Tag | LinkedIn Conversions API | Free B2B website demographics (job titles, industries, companies). |
| X (Twitter) | X Pixel (Website Tag) | X Conversion API | Separates Universal Website Tag from single-event action tags. |
| Pinterest | Pinterest Tag | API for Conversions | Built around e-commerce catalog pins and checkout values. |
| Snapchat | Snap Pixel | Snap Conversions API | Rapid mobile web loads and app-install handoffs. |
| Reddit | Reddit Pixel | Reddit Conversions API (CAPI) | Retargeting high-intent niche subreddit researchers. |
| Google/YouTube | Google Tag (gtag.js) | Enhanced Conversions | Ties into GA4 and Google Ads. |

## The modern catch: browser pixels alone are not enough

Apple iOS App Tracking Transparency (ATT), Safari ITP, and ad blockers make browser-only pixels miss roughly 20-40% of conversions. Every platform now wants DUAL tracking:

1. **Browser pixel** - fires client-side (surface browsing, cookies).
2. **Server-side API (CAPI)** - fires from your backend/CRM when a lead submits or pays, bypassing ad blockers.
3. **Event deduplication** - both events sent with a matching `event_id` so the platform merges them and does not double-count.

## Keep the site fast: do NOT paste 6 pixels in the head

Bloats the DOM and hurts load. Standard practice is Google Tag Manager:
- **Client-side GTM:** one container script on the site; manage all tags inside GTM.
- **Server-side GTM (or a custom backend webhook):** your site sends ONE data stream to your own server, which fans it out to Meta/LinkedIn/TikTok behind the scenes, keeping the visitor's browser clean.

## The website-critique checklist (what to scan for)

Run this during `critic-lens-ux` / `ui-visual-check`:
- [ ] List every tracking tag present in the page source / GTM container (Meta Pixel, TikTok, LinkedIn Insight, gtag, etc). View the live network requests for collect/measure endpoints.
- [ ] Is there a **server-side/CAPI** layer, or browser-only? Browser-only = the 20-40% conversion gap. Flag it.
- [ ] **Event dedup** present (matching event_id browser + server)? Without it, conversions double-count or platforms refuse to optimize.
- [ ] Tags managed via GTM (good) vs raw pasted scripts (bloat + maintenance risk).
- [ ] Page-speed impact: how many tags fire on load, do they block rendering, do they fire before consent?
- [ ] **Consent:** do tags respect a cookie/consent banner (GDPR/CCPA)? Firing non-essential tags pre-consent is a compliance risk.
- [ ] Are conversion events actually wired (form submit, checkout) or is the pixel installed but never firing conversions?

## Verdict labels for tracking findings

- **MISSING**: a platform they advertise on has no pixel/CAPI at all.
- **BROWSER-ONLY**: pixel but no server-side fallback (under-counts conversions).
- **NO-DEDUP**: dual tracking without event_id matching (double-count / mis-optimize).
- **BLOCKING**: tags hurting page load or firing pre-consent (compliance + speed risk).
- **OK**: dual tracking, deduped, via GTM, consent-aware.

## Why it matters for David's businesses

- **AlphaFlux:** its whitelabel customers (small service businesses) run ads; a tracking setup is part of what the platform could offer, and every customer site audit should check this.
- **Patriot Pest Control:** runs its own campaigns (see `persona-content-marketing`, `persona-ecommerce-growth`); browser-only tracking means paying for clicks it cannot see convert.

## Source

Compiled from the platform tracking model David provided (Meta/TikTok/LinkedIn/X/Pinterest/Snapchat/Reddit/Google dual-tracking + GTM pattern), 2026-10. Re-verify platform-specific CAPI endpoints against each vendor's docs before implementation.
