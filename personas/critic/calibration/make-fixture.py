#!/usr/bin/env python3
# make-fixture.py - builds the clean fixture artifact the calibration
# ground truth points at (P-07, D-32).
#
# The ground truth (ground-truth.json) names locations such as
# fixture-app/code/module-01.txt:13. Those locations exist only if the
# fixture tree exists and every module file carries EXACTLY 12 clean
# lines, so a seed appended by seed-runner.py lands with its defect on
# line 13. This generator writes that tree deterministically:
#
#   python3 make-fixture.py [--out DIR]     (default: ./fixture-app)
#
# The clean content is deliberately ordinary and defect-free for the
# lens it belongs to: authenticated handlers and parameterised queries
# for code, sourced figures for claims, error and empty states for ux,
# disclosed and substantiated copy for growth, complete notices for
# compliance. A few lines are cross-reference anchors: the original
# wording, full-year figures, and governing commitments that the
# cross-file seeds in seed-bank.json point at from sibling modules.
# If you edit the content, keep the 12-line shape and re-check the
# anchors, or the runner will refuse to score (it verifies the
# injected line against the ground truth on every run).
# Python 3 standard library only.
import argparse, sys
from pathlib import Path

CODE_COMMON = [
    "import os",
    "from app.db import db",
    "from app.auth import require_auth",
    "",
    "@require_auth",
    "def get_profile(req):",
    "    return db.execute('SELECT name, email FROM users WHERE id = ?', [req.user.id])",
    "",
    "def health(req):",
    "    return {'status': 'ok'}",
    "",
    "CHECKSUM = hashlib.sha256(payload).hexdigest()  # integrity check only, never for passwords",
]
CODE_SPECIFIC = {
    1: "Routes are registered here; every handler above the health check sits behind require_auth.",
    2: "Input validation helpers live here; handlers reject unexpected fields before touching the db.",
    3: "Background jobs module; jobs read secrets from the environment, never from source.",
    4: "Upload handling: filenames are regenerated server-side before any storage call.",
    5: "Rate limiting: limiter = RateLimiter('5/minute'), wired into the login route in module-01.",
    6: "Session handling uses the framework's signed session store; no custom deserialisation.",
    7: "File downloads resolve names against an allowlist of generated ids before opening anything.",
    8: "Worker config mirrors the web config; both read the payment key from the environment.",
}
CLAIMS_COMMON = [
    "Onboarding completion is 61 percent for the March cohort (source: product analytics, March 2026 export).",
    "The pricing page lists the monthly and annual prices side by side (source: pricing page, checked 2026-10-01).",
    "Support response time is quoted as a median, not a mean (source: support dashboard, Q3 2026).",
    "Every figure in this document names its source inline, in the same sentence.",
    "Comparisons name the competitor, the date, and the test conditions.",
    "Quotes are reproduced verbatim from the cited transcript or memo.",
    "Survey claims name the sample size next to the percentage.",
    "Old figures are labelled with their year wherever they are quoted.",
    "Superlatives are used only where a cited benchmark supports them.",
    "Causation language is reserved for controlled experiments.",
    "Windows are stated in full (month and year at both ends) for every trend.",
    "The reference list at the end of the pack is the only citation authority.",
]
CLAIMS_SPECIFIC = {
    1: "Module 01: claims pack introduction and method note.",
    2: "Module 02: full-year revenue grew 9 percent in 2025 (source: audited accounts, FY2025).",
    3: 'Module 03: from the all-hands notes, the CEO said, "We aim to ship the redesign in March if testing holds."',
    4: "Module 04: the 2023 analytics export is archived here and labelled historical wherever it is cited.",
    5: "Module 05: survey method note; the onboarding survey had 412 respondents in April 2026.",
    6: "Module 06: the retention cohort chart is observational and is described as a correlation.",
    7: "Module 07: vendor claims are tagged with the vendor's interest wherever they appear.",
    8: "Module 08: references and transcripts index for the whole pack.",
}
UX_COMMON = [
    "Every form in this spec defines loading, error, and success states.",
    "Error messages are written in plain language with a next step.",
    "Tap targets are at least 48px in both dimensions.",
    "Status is always shown with a text label as well as a colour.",
    "Body text contrast is 7 to 1 or better against its background.",
    "Images that carry information have alt text written for them.",
    "Every list defines an empty state with an action.",
    "Dialogs can be dismissed with the Esc key and return focus to the opener.",
    "Focus order follows the reading order of the page.",
    "Motion respects the reduced-motion setting.",
    "Long operations show progress and a way to cancel.",
    "Destructive actions ask for confirmation in words, not colour.",
]
UX_SPECIFIC = {
    1: "Palette and type scale are defined in this module; all contrast pairs were checked against it.",
    2: "The chart component pairs every image with a data table, per the pattern in this module.",
    3: "Checkout flow overview; the error behaviour is inherited from the shared form rules above.",
    4: "Account pages overview; empty states follow the shared list pattern.",
    5: "Invoice list behaviour is specified here, including its empty state.",
    6: "Settings pages overview; dialogs follow the shared dismissal rules.",
    7: "Modal patterns are defined here and reused by the checkout dialog.",
    8: "Icon set notes; icons are decorative unless paired with a label.",
}
GROWTH_COMMON = [
    "Sponsored content always carries the #ad disclosure in the first line.",
    "Scarcity claims quote the real inventory count and its date.",
    "Comparisons cite the benchmark, the lab, and the run date.",
    "Testimonials run with full name, company, and written permission on file.",
    "Prices state the renewal price wherever an introductory price appears; terms sit on the pricing page.",
    "Every campaign brief names one audience and one takeaway.",
    "Guarantees are limited to what the refund policy actually promises.",
    "Add-ons at checkout are opt-in and start unticked.",
    "Urgency copy is used only for dated offers with a real end date.",
    "Claims in ads meet the same evidence bar as claims in docs.",
    "Influencer briefs include the disclosure requirement in writing.",
    "Screenshots in ads are from the current shipping version.",
]
GROWTH_SPECIFIC = {
    1: "The brief template lives here: audience, single takeaway, evidence, disclosure.",
    2: "Fulfilment notes are referenced by the landing pages from this module.",
    3: "Module 03: fulfilment is print-on-demand; there is no warehouse stock count.",
    4: "Creator roster and the standard disclosure wording live here.",
    5: "Pricing page copy is maintained here with its terms alongside.",
    6: "Checkout options are specified here; add-ons start unticked by design.",
    7: "Social proof library: every quote here has a permission record number.",
    8: "Renewal pricing table: introductory and renewal prices are printed together.",
}
COMPLIANCE_COMMON = [
    "Privacy contact for all data questions: privacy@example.com, answered within 30 days.",
    "The privacy notice names a contact for rights requests on its first page.",
    "Consent checkboxes always start unticked; consent is an affirmative act.",
    "Retention periods are stated per data category in the retention schedule.",
    "Marketing consent is requested separately from account creation.",
    "International transfers are named in the notice with their safeguards.",
    "The incident plan commits to notifying affected users within 72 hours of a confirmed breach.",
    "Age-restricted features sit behind the age gate described in the onboarding spec.",
    "Parental consent is collected before any account is opened for a child.",
    "Every collection point states its purpose next to the field.",
    "Data subjects can export or delete their data from the settings page.",
    "The data map is reviewed quarterly against the live product.",
]
COMPLIANCE_SPECIFIC = {
    1: "This module holds the master privacy notice and its contact block.",
    2: "The consent texts live here; each purpose has its own separate consent line.",
    3: "The data map lives here; every entry names its purpose and retention period.",
    4: "Onboarding data collection is mapped here, including the age gate step.",
    5: "Processor list and transfer safeguards are recorded here.",
    6: "Module 06: the governing incident commitment is notification within 72 hours of a confirmed breach.",
    7: "Rights-request handling (access, export, deletion) is specified here.",
    8: "Retention schedule per category is maintained here.",
}

LENSES = {"code": (CODE_COMMON, CODE_SPECIFIC), "claims": (CLAIMS_COMMON, CLAIMS_SPECIFIC),
          "ux": (UX_COMMON, UX_SPECIFIC), "growth": (GROWTH_COMMON, GROWTH_SPECIFIC),
          "compliance": (COMPLIANCE_COMMON, COMPLIANCE_SPECIFIC)}

def module_lines(lens, idx):
    common, specific = LENSES[lens]
    lines = list(common)
    lines[11] = specific[idx]
    assert len(lines) == 12, f"{lens} module {idx} has {len(lines)} lines"
    return lines

def main():
    ap = argparse.ArgumentParser(description="Build the calibration fixture artifact (P-07)")
    ap.add_argument("--out", default="fixture-app")
    args = ap.parse_args()
    out = Path(args.out)
    count = 0
    for lens in LENSES:
        for idx in range(1, 9):
            p = out / lens / f"module-{idx:02d}.txt"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("\n".join(module_lines(lens, idx)) + "\n", encoding="utf-8")
            count += 1
    print(f"fixture written: {count} module files under {out} (12 clean lines each; seeds land on line 13)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
