# Revival research: recovering a defunct game

Use this chapter when the game already existed and died. The goal is evidence-backed rules and a buildable recreation spec, not nostalgia. The user is usually a veteran of the game: treat their memories as leads to verify, not facts.

## Workflow

1. Intake. Collect the game name, domains, user links, screenshots, and pasted pages. Ask one short deferred question about scope (faithful clone, remake, or both, and target version), then start researching without waiting.

2. Discover sources. For each domain, run `python scripts/wayback_cdx.py work/cdx <domain> <www.domain>` with filters, review the extension summary, tighten, then fetch with `python scripts/wayback_fetch.py` and convert with `python scripts/html_to_md.py`. The CDX index often returns 503 at first, and the script retries. Run large fetches in the background. See `source_hunting.md` for the source checklist, Wayback tricks, and evidence tiers.

3. Recover the official rules. Save help, manual, and changelog pages as Markdown under `research/`, and grep for equations, turn rules, costs, and item tables.

4. Reverse-engineer the fan tools. Fan calculators and simulators hold the real formulas. Map them with `python scripts/js_inventory.py`, extract formulas with line citations and data tables to JSON, and run the originals headless with `templates/headless_harness.js` to produce golden outputs. For three or more tool families, fan out to parallel sub-agents. See `reverse_engineering.md`.

5. Recover the look. Unpack the official image and skin packs and make contact sheets with `python scripts/contact_sheet.py`. Mirror any surviving live pages for the exact HTML and CSS. Recovered assets are research material and stay out of the shipped product unless the rights gate clears them.

6. Build the version history. Produce a timeline of every version or round with cited captures, plus a data-coverage matrix per version. Check the user's remembered numbers against it and correct them politely, with evidence. Recommend the best-documented ruleset.

7. Research relatives when they come up: forks, open-source sister games, successors, dev blogs, and genre comparisons for new subsystems. Record what the community liked and disliked.

8. Hand off to design. Feed the recovered rules into the main skill's design stage, starting from `templates/spec_outline.md` and `design_patterns.md`, with every recovered number as a config default and every gap marked as a design decision still to make.
