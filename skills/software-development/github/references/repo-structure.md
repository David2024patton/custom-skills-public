# Repo Structure: Applying the Planned File Standard

This file is the pointer and the discipline. The content of the
standard (which files, their headers, the cross-reference law) lives
in the `github-repo-standard` skill and is its single source; nothing
of that content is copied here. The machine readable form the tooling
consumes is `github-repo-standard/assets/repo-standard-manifest.json`
in the repo root of this collection, and the tool is
`scripts/repo-structure.py` in this skill.

## The workflow

1. Audit before scaffold, always. Run the audit mode first and show
   its full output: present, missing, header missing, and
   cross-reference breaks. No write of any kind happens before the
   audit has been seen.
2. Show the scaffold plan before any write: which files will be
   created, from which templates, seeded with what real state from
   the target repo. Files that exist are never overwritten, in any
   mode.
3. Writes go through the normal PR workflow of this skill: branch,
   one commit per file group with conventional commit messages,
   PR, checks, merge under the usual confirmation rules. Never a
   direct push to a protected branch.
4. Audit again after the PR merges. A repo that fails audit after
   scaffold is reported as failed, in those words, with the failing
   checks named. There is no softer phrasing for it.

## Modes of the tool

- `audit` (default): read only. Exit 1 when the repo is non
  conformant, with the breaks listed.
- `scaffold`: dry run by default, printing the change list. With
  `--apply` it creates missing files only, seeded from the repo's
  README, git log, and tree, and writes the answers file
  `.repo-standard.yaml` (structure format version, template version,
  variables, date) at the repo root.
- `repair-headers`: dry run by default, printing the diff. With
  `--apply` it inserts a missing instruction header into an existing
  standard file. It inserts; it never replaces body content.

## Worked example EX-A6: audit, scaffold, re-audit

```bash
python3 scripts/repo-structure.py audit --repo ~/src/example
# exit 1: missing ENDGOAL.md, docs/MAP.md; PLAN sections S4 names no TODO phase
python3 scripts/repo-structure.py scaffold --repo ~/src/example
# dry run: would create ENDGOAL.md, docs/MAP.md from templates, seeded from README
python3 scripts/repo-structure.py scaffold --repo ~/src/example --apply
# created the two files on a branch; PR opened through the normal workflow
python3 scripts/repo-structure.py audit --repo ~/src/example
# after merge: exit 1 still, PLAN S4 cross-reference break remains, reported as failed
```

The last line is the discipline: the scaffold is not called done
while an audit break stands, and the remaining break is fixed in the
PLAN file itself, in a follow-up PR, before the repo is reported
conformant.
