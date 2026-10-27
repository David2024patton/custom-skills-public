# README and skill patterns adopted for David's repos

Patterns in our own words, distilled 2026-10-20 from public skill and
README libraries David picked. Sources and licenses are listed at the
bottom; nothing here is copied text. Where a source repo has no license,
only general ideas were learned from it and nothing was reproduced.

## Part 1: README design patterns

### Start from the story, not the styling

Before any layout work, write five lines: the audience, the value in one
sentence, the primary proof, the first action a new reader should
succeed at, and the visual theme. Design serves those five lines. Claims
without evidence (invented benchmarks, adoption numbers, testimonials,
features) never appear as decoration; real screenshots, real output, and
real diagrams beat generated or stock imagery every time.

### Reading order that works

1. Hero: project name in exact brand casing plus the value in plain
   language.
2. Proof: screenshot, captured output, or showcase, as high as it can
   legibly sit.
3. What it is: one short explanation.
4. Why it is different: the mechanism, not slogans.
5. How it works: a short process or architecture view.
6. How to use: install plus the first command, copied from commands that
   actually run.
7. Limits, compatibility, contributing, license.

Put the example before the long explanation. Cut repeated promises and
internal detail that does not help a reader adopt the project. A good
redesign usually makes the README shorter or clearer, not just prettier.

### Own the visual layer as SVG assets

- Hero, section banners, and diagrams live as hand-built SVG files in
  the repo (assets/readme/ is a good home), so they are deterministic,
  editable, and free of third-party rendering dependencies.
- Markdown remains the content layer: every heading, paragraph, command,
  table, and link is real text. Nothing essential is baked into an
  image, and every image carries alt text that keeps the page meaningful
  if the image fails to load.
- Screenshots and photos are PNG or WebP. Motion, when David approves
  it, is a GIF with the static SVG kept as the fallback; motion is never
  the default.

### GitHub canvas rules (how GitHub actually renders)

- Author SVGs on a 1200-unit-wide viewBox and embed at width 100%.
  Judge the result at roughly 900 CSS px, the desktop content width.
- Essential diagram text at least 20 SVG units, supporting labels at
  least 18. If a 360 px phone-width preview makes required labels
  unreadable, cut density, split the visual, or move detail into
  Markdown.
- System font stacks only. GitHub strips scripts, remote fonts,
  foreignObject, and most CSS, and it does not play animation embedded
  inside an SVG.
- Ship light and dark variants with a picture element keyed to
  prefers-color-scheme, and verify contrast in both. Centered title
  blocks use plain HTML alignment, which GitHub allows.

### One visual system per project

Freeze a compact art-direction spec per repo: palette (background,
foreground, primary, accent, muted), typography (system stack, scale,
weight contrast), shape language (corner radius, stroke, spacing grid),
one recurring motif taken from the project's own world, and a
composition mood (calm, editorial, technical, playful, cinematic). A
terminal tool's motif might be prompt and cursor marks; an OS project
might use its tile grid. The test: remove the project name and the hero
should still not fit any other project.

David's taste inside that freedom (stated 2026-10-19, corrected by David
2026-10-20): black and red are his favorite colors, a favorite scheme,
NOT a law and NOT the palette for everything; black and red on every
repo would get tiresome. What he does consistently like is a black
background with a bright color on top of it, so text and key elements
pop; readable bright text and real padding are part of that. Each
project picks its own palette and motif: black-plus-red where it fits
the project, other bright-on-dark schemes where it does not.

### Badges and dynamic widgets

- Static badges (build, license, language, key project facts) via the
  usual badge images, only when they are true.
- Dynamic widget services exist that render a live SVG from URL
  parameters: a skills strip (languages, frameworks, libraries, tools,
  software, with an option to include names) and a profile stats card
  (followers, repositories, stars, commits), themeable through a theme
  parameter. These suit a profile README or an about page.
- Treat any hosted widget as garnish with a failure mode: it is someone
  else's service (the best-known one has been unmaintained since 2024),
  so never let it carry essential information, and prefer our own static
  SVGs for anything the project depends on.

### Scope and verification

- Three modes: whole-README redesign, asset-only (build visuals, touch
  nothing else), and audit-only (report, edit nothing). Confirm the mode
  when it is not explicit; expand scope only with approval.
- Before pushing: render locally at GitHub width, inspect wide and
  narrow layouts, hunt for clipped SVG text, missing assets, oversized
  files, and weak contrast in either color mode. Report what changed,
  what was intentionally left plain, and what was left untouched.

## Part 2: Agent skill-writing patterns

### The description does the triggering

The frontmatter description is the only part of a skill an agent reads
before deciding to load it. Write it to state the capability and list
the distinct situations that should trigger it, one trigger per
genuinely different branch, synonyms collapsed. Put the concept word
the user will actually say early. If a trigger rule matters, it lives in
the description, not buried in the body.

### Shape of a skill that fires correctly

- Imperative procedure with decision points, not an essay about the
  topic. The job of a skill is that the agent takes the same process
  every run, not that it produces identical output.
- Every step ends on a completion criterion that is checkable (done
  versus not done is decidable) and exhaustive where it matters ("every
  modified file accounted for", not "produce a list").
- A named stop condition, plus When to use and When NOT to use lists,
  plus a verification block phrased as falsification: what observation
  would prove the skill was misapplied or the run failed.
- Spend words only where they change behavior. Assume the agent is
  already good at general reasoning; state direction and constraints,
  and add mechanics only where a demonstrated failure demands them.

### Organize for progressive disclosure

- SKILL.md stays short. Long schemas, catalogs, provider notes, and
  variant guidance move into linked reference files that load only when
  a pointer in the skill fires. Reusable output material lives in
  assets or templates; fragile repeatable operations live in scripts.
- Keep a concept's definition, rules, and caveats under one heading so
  reading one part brings its neighbors with it.
- Split a skill only when it earns the cost: a distinct trigger word, a
  different invoker, or a step sequence so long that later steps tempt
  the agent to rush the current one.

### Examples teach the problem

An example earns its place by teaching recognition: the recurring
problem, its smell and symptoms, how it was spotted. The specific fix
applied that day rots as code changes and can mislead next time; the
problem description stays true. When in doubt, state what was broken
and how it was noticed, and stop there.

### Metadata, indexing, and validation

- Frontmatter: name, description, version, license, and tags or domain
  where the platform supports them.
- One folder per skill: SKILL.md plus optional references/, scripts/,
  assets or templates/. Group folders by category (engineering,
  authoring, security) and ship a small install or link script so the
  collection installs in one command.
- Big libraries index themselves: a machine-readable index mapping each
  skill to its purpose, tags, and any external framework it serves (for
  a security library, mappings to recognized control frameworks), so
  agents search the index instead of guessing.
- Validate by use: run the skill cold with a fresh agent on a realistic
  task, ideally the weakest model that will run it, and keep small eval
  cases per skill that can be re-run after edits. A skill that only
  drives correct behavior on the model that authored it is too fragile.
- A cheap validation script in CI (frontmatter present, fields sane,
  links resolve) catches broken skills before they ship.

## Sources and licenses (studied 2026-10-20)

- dzhng/skills (MIT): skill factory library; source of the
  trigger-description, progressive disclosure, examples-teach-the-problem,
  and validate-by-use guidance.
- oil-oil/beautify-github-readme (MIT): README design skill; source of
  the story-first method, SVG asset discipline, canvas numbers, and the
  verify pass.
- Jurredr/github-widgetbox (MIT): dynamic README widgets; source of the
  skills-strip and profile-stats widget patterns and the theme
  parameter idea.
- amazingloft999-droid/mattpocock-skills (MIT): engineering skills from
  a practitioner dotfiles repo; source of the phased procedure shape,
  feedback-loop discipline, and category-plus-format-file layout.
- tjboudreaux/cc-thinking-skills (MIT): thinking-model skills; source
  of the When to use / When NOT to use / stop condition / falsification
  block shape and per-skill eval contracts.
- mukul975/Anthropic-Cybersecurity-Skills (Apache-2.0): 800-plus
  framework-mapped security skills; source of the rich frontmatter
  metadata and machine-readable index patterns.
- thomast1906/github-copilot-agent-skills (no license file found, all
  rights reserved by default): Copilot agents and skills collection;
  only general organizational ideas were taken (agents beside skills,
  a CI validation script, a package manifest), and no text or code was
  copied from it.
