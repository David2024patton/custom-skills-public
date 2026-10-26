# MCP mapping for the github skill

This file, and `mcp-manifest.json` beside it, map ONE skill to MCP: the
`github` skill in this folder (`SKILL.md`, version 2.0.0, author Ben
Barclay, license MIT, see `LICENSE` in this folder). It exists so a server
operator, for example Chris Robinson with his GitHub MCP server, does not
have to guess how agent instructions become tools, prompts, and resources.

Scope, plainly: **the rest of the repo this skill ships in is not MCP
ready.** No other skill in the collection has a mapping, a manifest, or
input schemas. Only this folder is mapped. Anything beyond this folder
needs its own mapping pass before a server exposes it.

## The model in one paragraph

A skill is instructions for an agent that already has a terminal. An MCP
server cannot hand those instructions to a client and call it a tool. So
this mapping splits the skill three ways. Repeatable, bounded operations
become **tools** with JSON Schema inputs. Judgment work that should stay a
guided conversation becomes **prompts**. Reference text the client should
read but never execute becomes **resources**. The server implements each
tool by shelling out to `gh`, or `gh api`, under the operator's own
authenticated session.

## Credentials

The credential source for every surface is the server operator's `gh auth`
session on the host running the server. Nothing else. No surface accepts a
token, password, or credential file as an argument, and no surface returns
one in a result. This follows the skill's own rule in `references/auth.md`:
a token never enters agent context, stdout, environment variables, or a
transcript. If the operator session is not logged in, the tools report
that through `github_auth_status`, and the fix is the operator running
`gh auth login` in their own terminal. The server never repairs auth by
handling a credential itself.

## Read, write, and confirmation

Every surface in the manifest carries a class, read or write, and every
write class surface has `confirmation_required: true`. Confirmation means
a human approves that specific call, in the moment, after seeing what it
will do: the exact issue body, the exact review verdict, the exact merge.
A blanket approval stored in config does not count.

Seven actions sit on the skill's never-list, named per surface in the
manifest: merging a PR, deleting a branch, deleting a repo, changing repo
visibility, weakening branch protection, deleting secrets, and force
pushing. Each needs explicit human confirmation in the moment. Two of
them, changing repo visibility and weakening branch protection, must never
be executed on an instruction that came from repo or issue content at all.
A server may also choose not to implement the never-list actions on
`github_repo_admin`; leaving them out is a valid reading of this mapping.

## Untrusted content

Tools in this mapping return GitHub content: issue bodies, PR bodies,
comments, diffs, repo files. That content is data, never instructions, on
the server side as much as on the agent side. A server must not let text
returned by `github_pr_review_context` or `github_issue_search` trigger
further tool calls by itself, and a client agent using these tools is
bound by the Security section of `SKILL.md`.

## The mapping

| Workflow | Surface | Name | Class | Confirmation |
|---|---|---|---|---|
| Auth | tool | `github_auth_status` | read | no |
| Auth | prompt | `github_auth_setup` | read | no |
| Issues | tool | `github_issue_search` | read | no |
| Issues | tool | `github_issue_create` | write | yes |
| Issues | tool | `github_issue_update` | write | yes |
| PR lifecycle | tool | `github_pr_list` | read | no |
| PR lifecycle | tool | `github_pr_create` | write | yes |
| PR lifecycle | tool | `github_pr_merge` | write | yes, never-list |
| Issue to PR | prompt | `github_issue_to_pr` | write | yes, before the PR opens |
| Code review | tool | `github_pr_review_context` | read | no |
| Code review | prompt | `github_code_review` | read | no |
| Code review | tool | `github_pr_review_submit` | write | yes |
| Repo management | tool | `github_repo_view` | read | no |
| Repo management | tool | `github_repo_create` | write | yes |
| Repo management | tool | `github_repo_admin` | write | yes, never-list |
| Always-read references | resource | `github_api_cheatsheet` | read | no |
| Always-read references | resource | `github_conventional_commits` | read | no |
| Always-read references | resource | `github_review_output_template` | read | no |

The manifest is the machine readable source of truth: names, input
schemas, classes, confirmation flags, never-list membership, and the
reference file behind each surface. If this file and the manifest ever
disagree, the manifest wins and this file has a bug.

## Implementing notes

- Validate every tool call against the manifest schema before running
  anything. Reject unknown fields.
- Run `gh` with an argument array, never a shell string built from tool
  inputs. Owner, repo, branch, and title fields are untrusted input.
- Read live state inside the same call that acts on it. `github_pr_merge`
  verifies state, mergedAt, and checks itself; no surface trusts a state
  claim made by the caller or by earlier content.
- Log tool name, inputs minus any body text, and the `gh` result state for
  every write call, so an operator can audit what the server did.
- The two branch and push steps of the PR lifecycle stay in the operator's
  working tree with plain git. This mapping deliberately has no generic
  shell or git push surface.
