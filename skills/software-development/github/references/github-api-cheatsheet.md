# GitHub REST API Cheatsheet

Base URL: `https://api.github.com`

Run every call through `gh api`, which uses your existing `gh auth` session. Agents never handle a token directly (see `references/auth.md` in this skill).

Use the `gh-env.sh` helper in this skill to detect auth and the current repo. Paths here are relative to this skill folder, where `scripts/` and `references/` are siblings of `SKILL.md`:

```bash
source scripts/gh-env.sh
```

## Repositories

| Action | Method | Endpoint |
|--------|--------|----------|
| Get repo info | GET | `/repos/{owner}/{repo}` |
| Create repo (user) | POST | `/user/repos` |
| Create repo (org) | POST | `/orgs/{org}/repos` |
| Update repo | PATCH | `/repos/{owner}/{repo}` |
| Delete repo | DELETE | `/repos/{owner}/{repo}` |
| List your repos | GET | `/user/repos?per_page=30&sort=updated` |
| List org repos | GET | `/orgs/{org}/repos` |
| Fork repo | POST | `/repos/{owner}/{repo}/forks` |
| Create from template | POST | `/repos/{owner}/{template}/generate` |
| Get topics | GET | `/repos/{owner}/{repo}/topics` |
| Set topics | PUT | `/repos/{owner}/{repo}/topics` |

## Pull Requests

| Action | Method | Endpoint |
|--------|--------|----------|
| List PRs | GET | `/repos/{owner}/{repo}/pulls?state=open` |
| Create PR | POST | `/repos/{owner}/{repo}/pulls` |
| Get PR | GET | `/repos/{owner}/{repo}/pulls/{number}` |
| Update PR | PATCH | `/repos/{owner}/{repo}/pulls/{number}` |
| List PR files | GET | `/repos/{owner}/{repo}/pulls/{number}/files` |
| Merge PR | PUT | `/repos/{owner}/{repo}/pulls/{number}/merge` |
| Request reviewers | POST | `/repos/{owner}/{repo}/pulls/{number}/requested_reviewers` |
| Create review | POST | `/repos/{owner}/{repo}/pulls/{number}/reviews` |
| Inline comment | POST | `/repos/{owner}/{repo}/pulls/{number}/comments` |

### PR Merge Body

```json
{"merge_method": "squash", "commit_title": "feat: description (#N)"}
```

Merge methods: `"merge"`, `"squash"`, `"rebase"`

### PR Review Events

`"APPROVE"`, `"REQUEST_CHANGES"`, `"COMMENT"`

## Issues

| Action | Method | Endpoint |
|--------|--------|----------|
| List issues | GET | `/repos/{owner}/{repo}/issues?state=open` |
| Create issue | POST | `/repos/{owner}/{repo}/issues` |
| Get issue | GET | `/repos/{owner}/{repo}/issues/{number}` |
| Update issue | PATCH | `/repos/{owner}/{repo}/issues/{number}` |
| Add comment | POST | `/repos/{owner}/{repo}/issues/{number}/comments` |
| Add labels | POST | `/repos/{owner}/{repo}/issues/{number}/labels` |
| Remove label | DELETE | `/repos/{owner}/{repo}/issues/{number}/labels/{name}` |
| Add assignees | POST | `/repos/{owner}/{repo}/issues/{number}/assignees` |
| List labels | GET | `/repos/{owner}/{repo}/labels` |
| Search issues | GET | `/search/issues?q={query}+repo:{owner}/{repo}` |

Note: The Issues API also returns PRs. Filter with `"pull_request" not in item` when parsing.

## CI / GitHub Actions

| Action | Method | Endpoint |
|--------|--------|----------|
| List workflows | GET | `/repos/{owner}/{repo}/actions/workflows` |
| List runs | GET | `/repos/{owner}/{repo}/actions/runs?per_page=10` |
| List runs (branch) | GET | `/repos/{owner}/{repo}/actions/runs?branch={branch}` |
| Get run | GET | `/repos/{owner}/{repo}/actions/runs/{run_id}` |
| Download logs | GET | `/repos/{owner}/{repo}/actions/runs/{run_id}/logs` |
| Re-run | POST | `/repos/{owner}/{repo}/actions/runs/{run_id}/rerun` |
| Re-run failed | POST | `/repos/{owner}/{repo}/actions/runs/{run_id}/rerun-failed-jobs` |
| Trigger dispatch | POST | `/repos/{owner}/{repo}/actions/workflows/{id}/dispatches` |
| Commit status | GET | `/repos/{owner}/{repo}/commits/{sha}/status` |
| Check runs | GET | `/repos/{owner}/{repo}/commits/{sha}/check-runs` |

## Releases

| Action | Method | Endpoint |
|--------|--------|----------|
| List releases | GET | `/repos/{owner}/{repo}/releases` |
| Create release | POST | `/repos/{owner}/{repo}/releases` |
| Get release | GET | `/repos/{owner}/{repo}/releases/{id}` |
| Delete release | DELETE | `/repos/{owner}/{repo}/releases/{id}` |
| Upload asset | POST | `https://uploads.github.com/repos/{owner}/{repo}/releases/{id}/assets?name={filename}` |

## Secrets

| Action | Method | Endpoint |
|--------|--------|----------|
| List secrets | GET | `/repos/{owner}/{repo}/actions/secrets` |
| Get public key | GET | `/repos/{owner}/{repo}/actions/secrets/public-key` |
| Set secret | PUT | `/repos/{owner}/{repo}/actions/secrets/{name}` |
| Delete secret | DELETE | `/repos/{owner}/{repo}/actions/secrets/{name}` |

## Branch Protection

| Action | Method | Endpoint |
|--------|--------|----------|
| Get protection | GET | `/repos/{owner}/{repo}/branches/{branch}/protection` |
| Set protection | PUT | `/repos/{owner}/{repo}/branches/{branch}/protection` |
| Delete protection | DELETE | `/repos/{owner}/{repo}/branches/{branch}/protection` |

## User / Auth

| Action | Method | Endpoint |
|--------|--------|----------|
| Get current user | GET | `/user` |
| List user repos | GET | `/user/repos` |
| List user gists | GET | `/gists` |
| Create gist | POST | `/gists` |
| Search repos | GET | `/search/repositories?q={query}` |

## Pagination

Most list endpoints support:
- `?per_page=100` (max 100)
- `?page=2` for next page
- Check `Link` header for `rel="next"` URL

## Rate Limits

- Authenticated: 5,000 requests/hour
- Check remaining: `curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit`

## Common curl Patterns

```bash
# GET
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GH_OWNER/$GH_REPO

# POST with JSON body
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GH_OWNER/$GH_REPO/issues \
  -d '{"title": "...", "body": "..."}'

# PATCH (update)
curl -s -X PATCH \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GH_OWNER/$GH_REPO/issues/42 \
  -d '{"state": "closed"}'

# DELETE
curl -s -X DELETE \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GH_OWNER/$GH_REPO/issues/42/labels/bug

# Parse JSON response with python3
curl -s ... | python3 -c "import sys,json; data=json.load(sys.stdin); print(data['field'])"
```

## GraphQL: Projects v2 and Dependency Review

Projects v2 has no REST surface. The queries below are the ones
`references/projects.md` depends on, in this file's format.

```bash
# Project fields and option IDs
gh api graphql -f query='query { organization(login: "ORG") { projectV2(number: 1) { id fields(first: 30) { nodes { ... on ProjectV2SingleSelectField { id name options { id name } } ... on ProjectV2FieldCommon { id name } } } } } }'

# Items with content and status values
gh api graphql -f query='query { organization(login: "ORG") { projectV2(number: 1) { items(first: 50) { nodes { id content { ... on Issue { number title } ... on PullRequest { number title } } } } } } }'

# Add an item by content node ID, then read the items back to verify
gh api graphql -f query='mutation { addProjectV2ItemById(input: {projectId: "PROJECT_ID", contentId: "CONTENT_ID"}) { item { id } } }'
```

Dependency review (REST): the diff of dependencies between two refs,
used by `references/dependabot.md` before merging a version jump.

```bash
gh api repos/{owner}/{repo}/dependency-graph/compare/{base}...{head}
# Response lists changed dependencies with vulnerabilities and license data per change.
```
