# MANIFEST


## Contents

| Path | What | Count | Source |
|------|------|-------|--------|
| `skills/` | Hermes pipeline skills (persona, critic, instrument, research, business) | 115 SKILL.md (recount 2026-10-26) | orchestrator profile `skills/` |
| `personas/` | one `SOUL.md` per Hermes persona profile | 23 | profiles `*/SOUL.md` |
| `knowledge/` | curated per-language digests (language-knowledge) | 9 files | this package, `knowledge/` folder |
| `context/` | context-loading + domain-fanout notes | 1 | this package |
| `QA-LOOP.md` | the build law: the 7-phase loop, critic checklist, fix loop, visual gate | 1 | this package, repo root |
| `IDEA.md` | idea capture (user's words verbatim) | 1 | this package, repo root |
| `bootstrap.sh` | rebuild a fresh Hermes install from this package | 1 | this package |
| `collection-router/` | the router skill plus routing-overrides.yaml (the only hand written routing data) | 2 | this package, repo root |
| `registry.json` + `skill-aliases.json` | machine generated registry and alias map (scripts/build-registry.py) | 2 | generated, this package |
| `WORDING-STANDARD.md` | wording law: portable core plus labeled local bindings | 1 | this package, repo root |

Top-level folders not listed above (`golang-*`, `youtube`, `shopping`, the Muse built-ins, ...) are
the repo's pre-existing skills collection, unchanged. See `README.md` for the full source-grouped
index of those.

## Script packs

12 language packs, each `qa.sh` (grouped so related frameworks share a pack):
`c`, `cpp`, `csharp`, `flutter` (+dart), `go`, `java`, `js` (+react), `mojo`, `php` (+laravel), `python`, `rust`, `swift`.

Instruments (shared): `security/` (threat-feed.sh = live CISA KEV + CVE; secret-scan.sh), `web/` (browser-check.sh).

## Pipeline skills to know

- `persona-skeptic` + `critic-lens-code` / `-claims` / `-ux` / `-growth` : the adversarial critics.
- `exec-scripts`, `ui-visual-check`, `final-auditor`, `ideation-research` : the gates.
- `domain-fanout`, `language-knowledge`, `hermes-harness` : context + setup control.
- `ad-tracking-pixels`, `social-presence-audit`, `seo-reference`, `ai-seo-aeo` : business/marketing.
- the 18 `persona-*` skills : one per business + SDLC role.

## Two layouts, and which copy governs

This repo holds skills in two layouts, and both are normal here:

- Flat skills at the repo root (one folder per skill, Muse style): most of the
  collection, including the `golang-*` and `local-golang-*` sets and the
  Muse built-ins.
- Pipeline skills under `skills/` (grouped by category, Hermes pipeline
  style): the `persona-*` role skills, the critics, the gates, and the
  research and business skills indexed above.

Three skills exist in both layouts: `github-repo-standard`, `commit-gates`,
and `deep-research`. For those, one copy is canonical and the other is a
pointer file that names it:

- `github-repo-standard`: canonical at `github-repo-standard/` (repo root).
- `commit-gates`: canonical at `commit-gates/` (repo root).
- `deep-research`: canonical at `skills/deep-research/`.

The canonical copy governs. A pointer is never edited into a second version;
fixes land in the canonical copy only.

The Go skills are the standing exception to the duplicate rule: the
`golang-*` folders are upstream snapshots of samber/cc-skills-golang and
the `local-golang-*` folders are David's local working variants of the same
skills. Both sets are kept on purpose, the folder name is the identity, and
the two sets are not interchangeable.

## Use it

Read `QA-LOOP.md` first (it is the build law). Then `bash bootstrap.sh <hermes_home>` to install on
a fresh machine, or copy individual skills into a profile's `skills/` dir. Verify the critic and one
script pack before trusting any gate. Credentials are never included; enter them per install.
