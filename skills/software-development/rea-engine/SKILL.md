---
name: rea-engine
description: "Use when a claim depends on a shipped artifact rather than source: analyzing a built bundle, APK, binary, Electron or JavaScript application as shipped, comparing two shipped versions for changed behavior, extracting stack and API surface from a product available only as a build, or building the observed behavior inventory of a compiled artifact before a critique. Wraps the external REA engine (morluto/rea) as a pinned, on-demand tool. Skip for ordinary source-repository architecture analysis."
version: 1.0.0
author: David Patton
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [reverse-engineering, evidence, artifacts, rea, wrapper]
    related_skills: [persona-skeptic, critic-lens-code, reverse-engineering-saas, rea-ci-tests-audit, github-research]
---

# REA Engine (wrapper)

This unit wraps [REA](https://github.com/morluto/rea) (Reverse Engineer
Anything, by morluto, MIT) as an external, version-pinned engine for
this pipeline. The engine itself is never vendored and never embedded:
its code, its dependency notices, and the third-party analysis engines
it drives stay outside this repository. What lives here is the calling
discipline, plus REA's own instructions-only skill bundle under
`references/bundle/` (upstream text, MIT, see the LICENSE and
PROVENANCE.md there) for the agent that drives it.

## The pin

- Server: `rea-agents` **6.8.0** (npm `latest` verified 2026-10-27).
- Skill bundle: version **50** (frontmatter of the bundled
  `reverse-engineer-anything` skill at the intake commit).
- The two version lines are independent upstream. Pin them together;
  bump deliberately, never by drifting to `@latest`. REA ships
  breaking changes inside minors, so an unpinned call is a standing
  breakage subscription.
- Runtime gate: Node `^22.23.4 || ^24.22.1 || >=26.12.1`. Node 23 and
  25 are explicitly unsupported upstream. REA needs no API keys; it
  runs locally.

## Doors, in order of preference for this pipeline

1. **CLI one-shots (default).** No server, no registration, Evidence
   JSON on stdout:

   ```bash
   npx -y rea-agents@6.8.0 --version
   npx -y rea-agents@6.8.0 analyze-javascript-application <path> --detail summary --evidence_output <file>
   npx -y rea-agents@6.8.0 doctor
   ```

   Prefer summary delivery with an evidence bundle on disk; complete
   Evidence is large. Other one-shots cover web bundles, native and
   managed artifacts, firmware, captures, and the `compare-*` family
   for version-to-version behavior diffs.

2. **MCP server (gated).** Registered upstream in the MCP registry as
   `io.github.morluto/rea`, stdio transport:

   ```bash
   npx -y rea-agents@6.8.0 mcp
   ```

   Register it only behind a gate that routes artifact-shaped
   questions to it. REA's own `setup` command writes client
   configuration only after showing a read-only dry-run plan and
   receiving approval; keep that behavior, never bypass it.

3. **Skill bundle (reference).** `references/bundle/` teaches the
   driving agent REA's own method and scoping. Installing it registers
   nothing.

## When to call it

- A claim depends on a shipped binary or package: what does this
  bundle, APK, or build actually do.
- Version comparison of shipped artifacts (changed behavior between
  two builds), via the CLI `compare-*` commands.
- Stack and API-surface extraction from a product available only as
  a shipped artifact.
- The pre-critique behavior inventory of a compiled artifact (the
  Critic's observed-behavior map), when the artifact ships compiled.

## When not to call it

- Ordinary source-repository architecture analysis. REA's own skill
  states this boundary plainly: available source beats shipped
  artifact inference. The default source-review path stays with the
  repo's own tools and critics.
- Inside a multi-critic fan-out as a resident toolset. REA's full
  tool schemas measure around 110k tokens before any analysis; five
  resident copies would crowd out the critique itself. One REA seat,
  invoked on demand for a named question (an inventory or evidence
  step), is the design center.

## Engines are bring-your-own

Static JavaScript analysis needs no engine. Native work needs Ghidra,
Hopper, or IDA; Android needs JADX and Java; packet work needs tshark
(Wireshark 4.x); signal work needs sigrok-cli; WASM needs WABT;
firmware needs Binwalk or Unblob. Those engines carry their own
licenses, including GPL and commercial terms. They are the operator's
to install and license; nothing about them enters this repository.

## Provenance and credit

Wrapper text: David Patton, MIT (this repo's license). Bundled
upstream text and the engine: morluto, MIT, credited in this repo's
CREDITS.md and in PROVENANCE.md in this folder. Runtime proof at
intake (sandbox, Node v24.22.1, 2026-10-27): `rea-agents@6.8.0
--version` printed `6.8.0`, exit 0; `--help` listed the command
surface including `mcp`, `setup`, `doctor`, and
`analyze-javascript-application`.
