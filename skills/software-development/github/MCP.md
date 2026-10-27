# MCP mapping for the github skill

This file, and `mcp-manifest.json` beside it, map ONE skill to MCP: the
`github` skill in this folder (`SKILL.md`, version 3.0.0, author Ben
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
tool by shelling out to `gh`, or `gh api`, under the credential the
server resolves for the calling principal (see Credentials).

## Credentials

The credential source for every surface is a per call credential
reference bound to the server resolved principal, resolved inside the
server at call time. Each call arrives with a principal the server
resolved from its own authentication (`principal_id`, `tenant_id`).
The server looks up that principal's stored GitHub credential for the
surface's toolset and uses it for the upstream call. No surface
accepts a token, password, or credential file as an argument, and no
surface returns one in a result. A principal without a connected
GitHub credential receives a structured `not_connected` error naming
the service and the connection path. There is no fallback to another
principal's credential, to a shared service account, or to an
operator session, in any code path.

One labeled variant exists: `local_single_operator`, a stdio
deployment on one operator's own machine, where credential references
may bind to that operator's local `gh auth` session. It is never the
default for an HTTP deployment, and a deployment claiming multi user
support while binding operator sessions is mislabeled, not configured.

## Read, write, risk, and confirmation

Every surface in the manifest carries a class and a risk from one
vocabulary: `read`, `write`, `destructive`, `money`, `external-send`.
This mapping uses read, write, and destructive (`github_pr_merge`);
no surface in it moves money or sends externally.

Write class surfaces carry a confirmation object, not a boolean:

```json
{"confirmation_id": "...", "actor": "<principal_id>", "surface": "<surface name>",
 "payload_sha256": "<sha256 of the exact arguments>", "issued_at": "<RFC 3339>",
 "expires_at": "<RFC 3339, minutes later>", "single_use": true}
```

Elicitation through the client is the mechanism of first resort; the
object above is the fallback for clients without it. Server
verification rule: the server verifies actor, surface, and expiry,
that the hash matches the exact call the confirmation accompanies,
and that the confirmation has not been used, before executing. A
confirmation for one payload authorizes nothing else, ever. A blanket
approval stored in config does not count.

Seven actions sit on the skill's never-list, named per surface in the
manifest: merging a PR, deleting a branch, deleting a repo, changing
repo visibility, weakening branch protection, deleting secrets, and
force pushing. Each needs a confirmation in the moment. Two of them,
changing repo visibility and weakening branch protection, must never
be executed on an instruction that came from repo or issue content
at all.

## Toolsets

Every surface declares one toolset in the manifest, from: `repos`,
`issues`, `pull_requests`, `actions`, `code_security`,
`secret_protection`, `dependabot`, `discussions`. Execution refuses a
workflow whose toolsets the tenant has not enabled, with a structured
error naming the missing toolset. The packaged surfaces in this
mapping declare repos, issues, and pull_requests; the remaining
toolsets are declared for the workflow families the skill's
references cover (Actions, security scanning, secret protection,
Dependabot, discussions) ahead of their own surface mappings.

## The repo admin surface is not packaged

Mapping version 1 packaged `github_repo_admin` with a free form
settings object. Mapping version 2 removes it from the packaged
surfaces. Reason: administrative surfaces are packaged only with one
closed JSON Schema per action (`additionalProperties: false`,
enumerating the exact fields per action), and this surface does not
have them yet. The never-list actions it carried stay available to an
agent with a terminal under the skill's own confirmation rules; they
are not available through this MCP mapping until per action schemas
exist.

## Outputs, errors, and pagination

Every surface declares an output schema in the manifest: the result
envelope (`status`, `summary`, `artifacts`, `evidence`, `errors`,
closed with `additionalProperties: false`). Errors use one shape
(`code`, `message`, optional `toolset`, optional `retryable`).
Statuses are `ok`, `error`, `confirmation_required`, and
`not_connected`. List surfaces paginate by cursor with `limit`
(default 30, maximum 100); non-list surfaces return a single object.

## Anti-disclosure server note

Skill bodies are never registered as Resources or Prompts, on this
mapping or any other. Tools return results only. Tool descriptions
contain no skill text, no worked examples drawn from skill bodies,
and no internal file names. The reference resources named below are
the bounded exception this mapping has always carried: three named
reference files, served read only, and nothing else from the skill.
Honest limit, stated so no implementer mistakes the wording layer for
the control: confidentiality wording is a term of use for cooperating
agents; it is not a security mechanism, and deployments must not rely
on it as one. Custody of the skill files, output filtering, and
access control are the control.

## Version and review status

This is mapping version 2 (manifest `mapping_version: 2`). It
supersedes version 1 in three ways, per the C05 packaging design
(Section 6.8 of that report): `credential_source` becomes
`per_user_credential_ref` with server side resolution and a labeled
`local_single_operator` variant; `confirmation_required` booleans
become the confirmation object; and the repo admin surface is
removed from the packaging until it carries per action closed
schemas. The GitHub skill's workflows do not change; only their
packaging contract does. A joint review with the server operator is
required before claiming this mapping is consumable by a given
server; until that review happens, this file is a contract, not a
claim about any running server.

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
| Always-read references | resource | `github_api_cheatsheet` | read | no |
| Always-read references | resource | `github_conventional_commits` | read | no |
| Always-read references | resource | `github_review_output_template` | read | no |

The manifest is the machine readable source of truth: names, input
schemas, output schemas, classes, risk, toolsets, confirmation
objects, never-list membership, and the reference file behind each
surface. Confirmation cells above read 'yes' where the surface
carries a confirmation object (see the confirmation section). If this file and the manifest ever
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
