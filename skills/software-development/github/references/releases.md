# Releases: Tags, Notes, and Publishing

Route here for cutting a release or fixing release notes. The short
create commands in `references/repo-management.md` defer to this file
for the full discipline.

## Hard rules

- Draft first. A release is created as a draft, checked, then
  published. Publishing is a write the user confirms in the moment.
- Notes come from merged PRs, grouped by label, and are checked
  against the repo's CHANGELOG if it keeps one. A release whose notes
  contradict the changelog is not published until they agree.
- Assets are checked before publishing: names, sizes, and a checksum
  where the project publishes one. An asset uploaded after publish is
  a new fact to report, not a silent fix.
- Publish is verified by a fresh read. The create response is not
  proof of the published state.

## Flow

```bash
git tag -l 'v*' | tail -5                       # prior tags, naming pattern
gh pr list --state merged --search "merged:>=<last-release-date>" --json number,title,labels
gh release create v<X.Y.Z> --draft --title "v<X.Y.Z>" --notes-file notes.md
gh release view v<X.Y.Z> --json isDraft,tagName,assets   # check the draft
gh release upload v<X.Y.Z> ./dist/<asset>       # assets before publish
gh release edit v<X.Y.Z> --draft=false          # publish, after confirmation
gh release view v<X.Y.Z> --json isDraft,publishedAt,url  # read back: published
```

Notes structure, label based: features, fixes, documentation, and a
breaking changes section first when any merged PR carries that label.
Every note line names its PR number.

## Done

The release is read back as published with its URL, the notes match
the merged PR list and the changelog, and the asset list in the final
read matches what was meant to ship.

## Worked example EX-A5: a release from merged PRs

Last release v1.3.0 shipped 2026-10-01. The merged PR list since then
has 9 PRs: 4 features, 3 fixes, 1 docs, 1 breaking change. Notes are
drafted in that shape, the draft release is created and read back, the
built asset and its checksum file are uploaded and appear in the
draft's asset list, the user confirms, publish runs, and the final
read shows `isDraft: false` with the published URL. The repo
CHANGELOG entry for v1.4.0 lists the same 9 PRs.
