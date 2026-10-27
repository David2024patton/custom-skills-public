# Wording Standard: portable core, labeled local bindings

How skills and personas in this collection are worded for portability, so
an agent on another harness can execute them, while the owner's own
installs keep the local facts they need. Runtime-bound skills are the
labeled exception to that portability aim: the Muse built-ins in
README.md are bound to the Muse runtime and its install paths, and are
labeled as such. This standard is the authoring rule; two scripts check
and inventory it (`scripts/check-neutral.py`, `scripts/wording-scan.py`),
and the publish gate (`scripts/sanitize_snapshot.py`) remains the
value-level scrub. The three do different jobs and none replaces another.

## The three layers

1. **Neutral published core.** The skill as published: operations named, not
   products, machines, accounts, or private endpoints. Any agent with the
   capabilities the skill needs can run it cold.
2. **Published example configuration.** A `config.example` shape with named
   placeholders (`<your-search-endpoint>`, `github.credential_ref`) showing
   which values an installer supplies. Placeholders are names, never real
   values.
3. **Published local binding (values-free by rule).** The labeled local
   binding section at the end of a skill, published with the skill. A
   binding section may name roles and kinds, never values: no paths, repo
   names, hostnames, or private store filenames. Real values are supplied
   by the operator's own install outside the published text. A binding is
   never required to understand the neutral core.

## The binding-section standard

A skill that needs local facts carries exactly one binding section, at the
end of the file, in this form:

```markdown
## Local binding (YYYY-MM-DD)

- Bound fact: <what is bound, for example a search endpoint URL or a
  credential file location>
- Why it is bound: <the reason this install needs the concrete value>
- Portable assumption: <what the neutral core assumes instead, so an agent
  without this binding still knows what capability to use>
```

Rules:

- One binding section per file, always last, always date stamped. When a
  bound fact changes, update the date.
- Everything machine specific, account specific, or endpoint specific in a
  file lives inside its binding section. The same content outside the
  section is a wording defect, whatever file it sits in.
- A file with no local facts has no binding section. Do not add empty ones.
- Binding sections are exempt from the neutrality lint's path and runtime
  classes. They are never exempt from secret rules: a binding names where a
  credential lives, never the credential.
- Values-free rule: a binding section may name roles and kinds, never
  values. No paths, repo names, hostnames, or private store filenames
  appear in a binding section.

## Requirements blocks

Target for new and edited skills: every new or edited SKILL.md carries a
Requirements block near the top:

- The capabilities the executing agent needs, named as operations ("a web
  search tool", "shell access", "a GitHub CLI or API client"), not as one
  harness's tool names.
- Configuration keys by name only (for example `github.credential_ref`),
  never values.
- Anything the skill refuses to do without, stated as a refusal, not a hope.

Exception: when a tool is the skill's subject (the github skill teaches the
gh CLI; a Dokploy skill teaches Dokploy), the tool is named as subject
matter, and the Requirements block says which parts are subject matter and
which are execution needs.

Current state, scan dated 2026-10-26 on the private tree: 2 of the 297
SKILL.md files carry an exact Requirements heading, so the block above
is a target for new and edited skills, not a description of the whole
collection yet. The same scan run gave: check-neutral.py exit 1, with
227 violations in 67 files and no HARD-COUNT hits; wording-scan.py
totals were ABS-PATH 32, HARNESS-TERM 148, KEY-REF 15,
PRIVATE-ENDPOINT 2, and UNLABELED-BINDING 50 files, across 78 files
with hits. Those counts are the sweep backlog, printed here so the
gap between the target and the current tree is on record.

## Capability vocabulary

- Name the operation and let the executing environment supply its tool:
  "search the web", "read the file", "run the command", "delegate this
  envelope". Harness-specific tool names belong in a binding section or an
  adapter note, not in the method.
- Counts of the collection ("this repo holds N skills") are generated facts.
  They live in `registry.json` and in generated documents. A hand-written
  count in a skill or index is a defect the moment it is written.

## Enforcement and inventory

- `scripts/check-neutral.py` is the wording checker: rule classes
  PERSON-NAME, MACHINE-NAME, ABS-PATH, RUNTIME-LEAK, HARD-COUNT. It is
  run on demand and is not yet wired into the publish gates. It fails on
  violations in neutral core text and exempts labeled binding sections
  from ABS-PATH and RUNTIME-LEAK only.
- `scripts/wording-scan.py` is the inventory: it scans a tree and reports
  hit counts by class (HARNESS-TERM, ABS-PATH, PRIVATE-ENDPOINT,
  UNLABELED-BINDING, KEY-REF) as the sweep backlog. It reports; it does not
  gate.
- The full wording sweep applies cluster by cluster during fix work, using
  the scan report as the work list. Mass rewrites without the inventory are
  not how this standard gets applied.
