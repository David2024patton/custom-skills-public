---
name: github-repo-standard
description: "GitHub Repo Standard (David Patton): every repo David owns carries the same standard file set so any project can be picked up cold."
version: 1.0.0
author: David Patton
license: MIT
platforms: [linux, macos, windows]
---

# GitHub Repo Standard (David Patton)

Every repo David owns carries the same skeleton so any project can be picked
up cold, by him or by an agent, and stay on track. Use this skill when:
creating a repo, starting a project, doing a docs pass on a repo, writing or
refreshing a README, or whenever a repo is missing its standard files.

Application of this standard to a live repo is performed by the github skill's repo structure workflow; this skill remains the content owner.

## The standard set (non-negotiable)

Repo root: TODO.md, IDEA.md, PLAN.md, ENDGOAL.md, STATUS.md,
DECISIONS.md, CHANGELOG.md, REFERENCES.md, README.md. In docs/:
RULES.md, RUNBOOK.md, MAP.md. Every file carries its instruction header
from the templates.

The machinery files (also part of the standard set, at the repo root
unless the path says otherwise; a template for each lives in this
skill's templates/ folder at the same relative path):

- .gitignore: what never enters the repo (secrets, build output,
 local state). One combined template covering the stacks this
 standard serves, trimmed per repo; lockfiles are committed on
 purpose and are never listed in it.
- .editorconfig: charset, line endings, and indentation, so
 whitespace agrees across machines and editors before the gates run.
- .gitattributes: text files normalize to LF in the repo and binary
 formats are marked binary, so diffs and gates behave the same on
 every machine.
- CODEOWNERS: who must review what, with the sensitive paths (gate
 scripts, workflow files, the rules page) named explicitly.
 Placeholder owners are replaced with the repo's real owners in the
 first pass; an unresolved CODEOWNERS file enforces nothing.
- SECURITY.md: how to report a vulnerability privately, which
 versions get fixes, and the rule that a committed secret is treated
 as a live secret.
- .github/pull_request_template.md: the change description standard
 for every PR (a standalone first line, context, non-goals, and
 proof links).
- .github/workflows/gates.yml: the commit-gates CI proof layer (the
 same file the commit-gates skill ships in its templates/), running
 the gates whole-tree on pull requests and on pushes to the default
 branch, with an actionlint step over the workflow files themselves
 and the commit message re-check over the PR commit range.

Optional PR automation: a repo may add a dangerfile or platform
equivalent that enforces the checkable standard rules on every PR.
A repo that runs no PR automation says so explicitly in
docs/RULES.md; silence is not a statement, so the choice is written
down either way.

The four planning files:

1. **TODO.md**: the super-detailed task list. Phases, checkboxes, every item
 small enough to verify. An item is only checked when its proof exists
 (a test, a log line, a bench note, a live check), and the proof is named
 on the item or in the project docs. Emulation-proven and bench-proven
 are marked differently; never blur them. Every item carries a stable ID
 (T-<phase>.<n>) and names the PLAN.md section it serves (see the
 cross-reference law below).
2. **IDEA.md**: David's idea capture, as full records. When David talks,
 dictates, or drops a thought about the project in any chat, it lands in
 IDEA.md as a categorized entry: date AND time, David's words, Lulu's
 reply or assessment at the time, and a stats line (what it would take,
 effort, value, depends on). Summaries are marked as summaries; quotes
 are used only where his exact words are on record. Ideas are never
 silently dropped; an idea leaves active status only by moving into
 TODO.md (status MOVED with the TODO item id) or by David killing it
 (marked KILLED with the date, kept for the record). Newest first.
3. **PLAN.md**: the whole product plan, step by step: what the software or
 site is, who it serves, the architecture, the build order, and how each
 step maps to TODO.md items (name the TODO phase on each step). Sections
 are numbered (S1, S2, ...) so TODO items can point at them. Shelf repos
 from the harvest (~/workspace/google-org-harvest/USE-IT.md) are worked
 into the plan wherever they fit, named on the step that uses them. When
 the plan changes, PLAN.md changes first, then TODO.md follows.
4. **ENDGOAL.md**: the project's end state, in plain words: what the
 finished thing is and does, experienced by the person using it, and
 the observable conditions that prove it is reached. TODO and PLAN
 serve this file; work continues until the end goal is reached. Sourced
 from David's stated vision and the project's record, never invented,
 and updated the same day he restates it.

## The jump-back-in files

5. **STATUS.md**: the living right-now snapshot (proven state, in
 flight, blocked and on whom, next three moves with TODO ids). Updated
 at the end of every work session on the project, in the same pass as
 the work it reports.
6. **DECISIONS.md**: the settled-decision log, kept as a single
 rolling file. Every entry carries: the decision, the date, why, a
 Consequences line (what follows from the call: what changes, what
 it costs, what to watch), what it supersedes, a Status field
 (active, superseded by entry N, reversed by entry N, where entry N
 is the later entry that replaced or reversed it), and by whom.
 Settled questions are never re-asked; reversing a call takes a new
 entry naming what it supersedes, and the old entry's Status line
 is updated to point at the new entry.
7. **docs/RUNBOOK.md**: build, run, deploy, verify, where things live
 (credential storage pointers by NAME only, never values), and the
 gotchas with their fixes. Commands copied from the working build.
8. **CHANGELOG.md**: what shipped, dated, newest first, one entry per
 milestone with its proof or commit. Git history is the raw record;
 this is the readable one.
9. **docs/MAP.md**: the whole project laid out: every node (page,
 screen, module, engine, service, external) in a grid table, every
 link in a table traced both ways (the connection and its backlink),
 a Mermaid diagram of the same, and the main flows in words. Planned
 nodes are marked (planned). A rendered visual version is generated
 from this file for David. When a module or link changes, MAP changes
 in the same commit.

10. **REFERENCES.md**: every link David posts about the project, with
 the answer to it: what it is, its license, the verdict (TAKE,
 RETROFIT, REFERENCE, SKIP) with the reason, and where the takeaway
 went (a TODO id, an IDEA entry, the shelf). Filed the same day the
 link is posted, skips included; the skip reasons are the value.

## Cross-reference law (TODO and PLAN coordinate)

- PLAN.md sections are numbered S1, S2, S3... and each build step names
 its TODO phase.
- Every TODO item has a stable ID (T-<phase>.<item>) and ends with
 (PLAN S<n>) naming the plan section it serves.
- The point: an agent can read ONE TODO item plus its ONE plan section
 and know the job, without reading either whole file. Keep item IDs and
 section numbers stable once published; renumber only in a deliberate
 pass that updates both files together.

Templates for all three live in this skill's templates/ folder. Seed them
from the project's real state, never from boilerplate alone: read the
repo, its goal file, and the chat brief first.

## The rules page

Every repo also carries **docs/RULES.md** (template in templates/RULES.md):
the build law in one page. Modularity (grid and tiles), build 20 years
ahead, debugging and linting in every module from birth, limits as config
never constants, version fields in data formats, interface seams at
change-prone boundaries, check the take-shelf before building anything
(~/workspace/google-org-harvest/USE-IT.md), security gates, atomic commits,
verify before done, exact brand casing, no em dashes in prose or docs.

## README standard

A README is the project's face; it should look like innovation, not a
default template. Full pattern set: README-PATTERNS.md in this folder
(story-first design, SVG asset discipline, GitHub canvas rules, widgets).
The load-bearing rules:

- Story before styling. Write down the audience, the one-sentence value,
 the primary proof, and the first successful action before touching
 layout. Never invent adoption, benchmarks, or features as decoration.
- Reading order: hero (name in exact casing + plain-language value),
 then proof (a real screenshot, output, or diagram), then what it is,
 why it is different (mechanism, not slogans), how it works, how to use
 it (quickstart copied from real build commands), limits and license.
 The example comes before the long explanation.
- The hero carries the proof: fold a real screenshot, diagram, or output
 into the first screen when it stays legible; otherwise a concise title
 block with the proof board immediately under it.
- Visual assets are SVG files the repo owns, under assets/readme/:
 hero, section banners, architecture and workflow diagrams. All copy,
 commands, tables, and links stay in Markdown, never baked into images.
- GitHub canvas: SVG viewBox 1200 units wide, embedded at width 100%,
 judged at about 900 CSS px render width; essential diagram text at
 least 20 units, labels at least 18; system fonts only (GitHub strips
 scripts, remote fonts, and foreignObject; animation inside SVG does
 not play, so motion is a GIF plus a static SVG fallback, opt-in only).
- One visual system per repo, derived from the project itself: a small
 palette (background, foreground, primary, accent, muted), a type
 scale, and one recurring motif from the project's own world. Never
 the same template across repos.
- Art direction follows David's taste (corrected by David 2026-10-20): black and red are his favorite scheme, not a law and not every repo's palette; his standing preference is a black background with a bright color on top so things pop, and each project picks its own palette and motif inside that preference (full note in README-PATTERNS.md). Light and dark variants via a picture element with
 prefers-color-scheme; contrast verified in both modes.
- Badges only when true: build status, license, language, and the
 project's own key facts. Dynamic widget strips (skill icons, profile
 stats) are optional garnish served by third-party hosts; the README
 must stay fully meaningful if they never load, and every image gets
 real alt text.
- A module map (the grid): the project's modules and what each owns.
- Links to TODO.md, PLAN.md, IDEA.md, and docs/RULES.md near the top.
- Verify before pushing: render locally at GitHub width, wide and
 narrow (360 px), check clipped text, missing assets, file sizes, and
 dark/light contrast.
- Scope discipline: whole-README redesign, asset-only, or audit-only.
 Confirm the mode with David when it is not explicit, and make the
 smallest change in that mode that meaningfully improves the page.

## Brand casing (exact, everywhere: docs, READMEs, code comments, UI)

| Name | Exact form |
| :--- | :--- |
| AlphaVision | capital A, capital V, rest lowercase |
| AlphaFlux | capital A, capital F |
| iTaK | lowercase i, capital T, capital K (iTaK Learn, iTaK Gaming) |
| the harness | capital M only |
| Patriot Pest Control | full name wherever there are words, never just "pest control" |

## Writing skills (guidance for ~/workspace/custom-skills)

When a job creates or revises a skill of our own, hold it to this bar
(patterns distilled from the public skill libraries studied 2026-10-20;
full notes in README-PATTERNS.md):

- The frontmatter description is the trigger: it is the only part read
 before the skill loads, so it states what the skill does and the
 distinct situations that should fire it, one trigger per branch, with
 the key concept word front-loaded. Trigger rules never hide in the body.
- Procedures, not essays: imperative steps, each ending on a completion
 criterion an agent can actually check, exhaustive where it matters.
- Progressive disclosure: keep SKILL.md short; push long schemas,
 examples, and variant detail into linked reference files, reusable
 output material into templates or assets, and fragile repeatable
 operations into scripts.
- Give the skill a When to use, a When NOT to use, an explicit stop
 condition, and a short verification block that says what would falsify
 a run. This shape keeps agents from over-applying a skill.
- Examples document the problem (the smell, the symptom, how it was
 spotted), not the fix that happened to be applied; fixes go stale,
 problem recognition does not.
- Frontmatter carries name, description, version, and license; a skill
 folder is SKILL.md plus optional references/, templates/, scripts/.
- Validate by use before calling a skill done: a fresh agent applies it
 cold to a realistic task, ideally on the weakest model that will run
 it. A skill that only works for the model that wrote it is too fragile.
- Large collections get a machine-readable index (name, purpose, tags)
 so skills can be searched and mapped instead of remembered.

## Procedure: new repo

1. Create the repo with the full standard set from the templates in the
 same first pass as the code scaffold (the four planning files,
 STATUS, DECISIONS, CHANGELOG, README, docs/RULES.md, docs/RUNBOOK.md,
 docs/MAP.md), including the machinery files in the same first pass
 (.gitignore, .editorconfig, .gitattributes, CODEOWNERS, SECURITY.md,
 .github/pull_request_template.md, .github/workflows/gates.yml), with
 the placeholder owners and contacts in CODEOWNERS and SECURITY.md
 replaced by the repo's real ones. Every file carries its instruction
 header from the template; never strip it.
2. Seed from the project's real brief: ENDGOAL from David's stated vision,
 PLAN sections numbered with build steps, TODO items with IDs and
 (PLAN S<n>) tags, IDEA with anything he has already said.
3. Run the commit-gates skill before the first push.

## Procedure: retrofit an old repo

When this skill meets a repo that predates the standard, set it up in
place; do not wait to be asked repo by repo:
1. Ingest the repo: README, docs, code layout, existing task lists. Then
 ingest the record: the project's goal files, memory, and past
 conversations, for what David wants and has talked about.
2. Inventory which standard files exist and their state, and check for
 the machinery files in the same inventory (.gitignore, .editorconfig,
 .gitattributes, CODEOWNERS, SECURITY.md,
 .github/pull_request_template.md, .github/workflows/gates.yml);
 missing machinery files are added in the retrofit pass, and
 placeholder owners or contacts left standing in CODEOWNERS or
 SECURITY.md count as missing. Preserve every real fact already in
 the repo; the standard files absorb existing content, they never
 overwrite it with boilerplate.
3. Derive ENDGOAL.md from the README and the feature set, plus anything
 the user wants or has talked about in the record. Where sources
 disagree or the record is thin, write the end state at the level the
 record supports and name the gap as an open question in PLAN.
4. Rebuild PLAN.md with numbered sections and the shelf repos worked in;
 retrofit TODO.md with stable IDs and (PLAN S<n>) tags without touching
 checkbox states or wording; convert IDEA.md to the v2 record format
 honestly (summaries marked, times only where recorded).
5. Add the instruction header to any standard file that lacks one.
6. Backfill the jump-back-in files from the record: STATUS from the
 current state, DECISIONS from the decisions on record, RUNBOOK from
 the existing deploy/bench/ops docs, CHANGELOG from the git history,
 MAP from the module layout and the links between them (planned nodes
 marked (planned)).
7. Push per file through the repo's normal path, fetch-verify, and
 report what was created, what was converted, and what is parked.

## Safety (always on)

- No passwords, API keys, tokens, or secrets in ANY repo file, doc, or
 script, ever. Credentials live in secure storage only and reach people
 through secure links, never pasted into files or chat.
- Local-only files that hold access details (for example an ACCESS.md)
 are never committed and never quoted.
- Secret scanning (betterleaks or gitleaks) is part of the commit gates;
 a scan hit stops the commit.
- When retrofitting, if existing files contain a secret, stop, flag it
 for David, and do not republish it in the new files.

## Linked skill: commit gates

Nothing commits unless the gates pass. The gate law, the per-language
debugging and linting standards, the security checks, and the ready-to-
fire scripts live in the linked skill: ~/workspace/custom-skills/
commit-gates/SKILL.md, with its scripts library at
~/workspace/custom-skills/commit-gates/scripts/ organized by language.
This skill defers to that one for everything about proving code before
it lands.

## Hard rules

- Never invent project facts for these files. If the plan is unknown, the
 PLAN.md says what is decided and names the open questions.
- TODO checkboxes reflect proofs, not optimism.
- David's words in IDEA.md stay his words; editing is formatting only.
- No em dashes anywhere in these files.
