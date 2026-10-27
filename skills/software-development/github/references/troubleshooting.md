# Troubleshooting: Symptom Index

General symptoms across this skill. CI specific failures live in
`references/ci-troubleshooting.md`; auth failures in
`references/auth-and-identity.md`.

| Symptom | First read | Usual cause and route |
|---|---|---|
| `gh auth status` fails mid-session | `gh auth status` | expired or switched login; auth reference, identity section |
| Writes land under the wrong account | `gh api user --jq .login` | multiple logins on the host; switch and read back (auth reference) |
| Merge button blocked, reason unclear | `gh pr view --json mergeable,mergeStateStatus,reviewDecision` plus the protection read | required check, review, or unresolved thread; `references/rulesets-protection.md`, `scripts/gh-pr-ready.sh` |
| PR shows green in the list but a check failed | `gh pr checks <PR>` run yourself | list badges are cached; never report CI from a list |
| Push rejected, non-fast-forward | `git fetch` then `git status` | the branch moved; rebase or merge deliberately, never force push without never-list confirmation |
| Release published but assets missing | `gh release view <TAG> --json assets` | assets upload before publish; `references/releases.md` |
| Search returns nothing for a known repo | `gh search repos "repo:owner/name"` | `gh repo view` can fail on repos that exist; search is the fallback (github-research skill notes the same pitfall) |
| Rate limit stops a sweep | `gh api rate_limit` | wait for the reset window; sweeps resume, they do not hammer (`references/search-playbooks.md`) |
| Ruleset blocks an action protection allows | `gh api repos/{owner}/{repo}/rulesets` | rulesets layer over branch protection; read both before concluding |

Every row ends in a read. A symptom explained without its first read
being run is a guess, and is reported as one.
