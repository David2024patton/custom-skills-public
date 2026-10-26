---
name: language-knowledge
description: "Use to load the curated library map for a language."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
  hermes:
    tags: [knowledge-base, libraries, reference, awesome-lists, gitingest, language]
    related_skills: [research-lens-stack, persona-sdlc-builder, exec-scripts, hermes-harness]
---

# Language Knowledge Base: curated library maps

## When to Use

Before picking a library, tool, or approach in a language, load that language's digest so the choice is grounded in the curated best-of list instead of memory. Also load before a build to know what already exists (do not rebuild what an awesome-list entry already solves). This is the reference `research-lens-stack` points at when it says "where to look."

## What a digest is

Each `knowledge/<lang>.md` is a gitingest text digest of an awesome-list repo: summary, directory tree, and the full curated list of libraries with one-line descriptions. It is a MAP of the best libraries per language, not a tutorial. It answers "what is the best library for X" so the builder does not pick from thin air.

## Load ONLY your language (token economics)

mimo.v2.6-flash has a 1M token window, but that is per-language, not all-at-once. Real sizes from the live ingest:

| Digest | Size | ~Tokens | Fits with headroom? |
|---|---|---|---|
| go (awesome-go) | 632 KB | ~158K | yes |
| python (awesome-python) | 532 KB | ~133K | yes |
| java (awesome-java) | 390 KB | ~97K | yes |
| cpp (awesome-cpp) | 218 KB | ~54K | yes |
| awesome (master index) | 108 KB | ~27K | yes |
| c (awesome-c) | 100 KB | ~25K | yes |
| dart (awesome-dart) | 16 KB | ~4K | yes |
| javascript (30-seconds-of-code) | 3.7 MB | ~926K | NO, too big to load whole |

Rules:
- Load ONE language digest per task (two small ones max). go + python together is ~291K, fine; adding javascript blows the window.
- The javascript/30-seconds digest is code snippets and is 926K alone. Load it selectively (re-ingest with `-s` size cap or `-i` include patterns) rather than whole.
- Do not load a digest for a language you are not using. It burns window for nothing.

## Add a language (ingest on demand)

```bash
cd knowledge
python ingest.py <github-url> <label>     # single
ingest.py --batch                          # curated priority set
```
Uses gitingest (`pip install gitingest`) to turn any GitHub repo into a prompt-ready digest. Prefer awesome-list repos (curated library maps). For a language not yet ingested, run this first, then load the result.

## Where the value lands

A digest entry is a lead, not proof. When a library name surfaces that fits the task, hand it to `research-lens-stack` to verify the real repo: stars vs last-push, actual LICENSE file, maintenance, and a machine-access path. The digest says what exists; the stack lens says whether it is any good and safe to adopt.

## Adding awesome lists by category

The master index `knowledge/awesome.md` lists every category (lang-agnostic and per-language). To extend coverage for a category David works in, ingest that category's canonical awesome list with the command above. Prioritize David's stack first: Go, Dart, Rust, Python, JS, PHP, C, C++, C#, Mojo.
