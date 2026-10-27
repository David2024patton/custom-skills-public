# Repo-to-text pack

This reference defines the repo-to-text pack format (PACK-1): the standard study artifact for every repository a deep or exhaustive run studies under Gate G. A pack carries a header block (name, URL, stars as of date, license, last activity, no-secrets statement), What it is, Structure worth knowing, Technique inventory, Additions it suggests for our skills, and an Ingestion note.

## Pack template

# Repo-to-text pack: <owner>/<repo>

URL: <repo URL>
Stars as of date: <star count and the date observed>
License: <license, recorded from the repo's own LICENSE file>
Last activity: <release or commit recency>
Contains no keys, tokens, credentials, or personal data. Techniques and structure only; no code text is reproduced from the repository.

## What it is

<What the repo does, in plain language, from its README and primary sources.>

## Structure worth knowing

<Structure worth knowing: tree, configuration, or core module description, read beyond the README.>

## Technique inventory

<Techniques and architecture taken from the repo. Techniques and architecture only; never copy code text from any repo, whatever its license.>

## Additions it suggests for our skills

<Additions the repo suggests for our skills, named per skill.>

## Ingestion note

<How a later run ingests this pack instead of re-studying the repo. A pack is plain Markdown, self-contained, and safe to hand to any agent: it contains no keys, tokens, credentials, or personal data, and no code text from the repo.>

## Rules

1. "For every repo studied at deep or exhaustive effort, write a repo-to-text pack into the run folder at repos/NN-owner-repo.md, numbered in fit order."
2. "A pack is plain Markdown, self-contained, and safe to hand to any agent: it contains no keys, tokens, credentials, or personal data, and no code text from the repo."
3. "Packs are evidence, not decoration: the report must name which pack techniques it used or rejected, and packs are filed with the run so a later run can ingest them instead of re-studying the repo."
