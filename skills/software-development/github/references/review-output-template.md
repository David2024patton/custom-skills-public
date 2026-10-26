# Review Output Template

Use this as the structure for PR review summary comments. Copy and fill in the sections.

## For PR Summary Comment

```markdown
## Code Review Summary

**Verdict: [Approved ✅ | Changes Requested 🔴 | Reviewed 💬]** ([N] issues, [N] suggestions)

**PR:** #[number] - [title]
**Author:** @[username]
**Files changed:** [N] (+[additions] -[deletions])

### 🔴 Critical
<!-- Issues that MUST be fixed before merge -->
- **file.py:line** - [description]. Suggestion: [fix].

### ⚠️ Warnings
<!-- Issues that SHOULD be fixed, but not strictly blocking -->
- **file.py:line** - [description].

### 💡 Suggestions
<!-- Non-blocking improvements, style preferences, future considerations -->
- **file.py:line** - [description].

### ✅ Looks Good
<!-- Call out things done well - positive reinforcement -->
- [aspect that was done well]

---
*Reviewed by Hermes Agent*
```

## Severity Guide

| Level | Icon | When to use | Blocks merge? |
|-------|------|-------------|---------------|
| Critical | 🔴 | Security vulnerabilities, data loss risk, crashes, broken core functionality | Yes |
| Warning | ⚠️ | Bugs in non-critical paths, missing error handling, missing tests for new code | Usually yes |
| Suggestion | 💡 | Style improvements, refactoring ideas, performance hints, documentation gaps | No |
| Looks Good | ✅ | Clean patterns, good test coverage, clear naming, smart design decisions | N/A |

## Verdict Decision

- **Approved ✅** - Zero critical/warning items. Only suggestions or all clear.
- **Changes Requested 🔴** - Any critical or warning item exists.
- **Reviewed 💬** - Observations only (draft PRs, uncertain findings, informational).

## For Inline Comments

Prefix inline comments with the severity icon so they're scannable:

```
🔴 **Critical:** User input passed directly to SQL query - use parameterized queries to prevent injection.
```

```
⚠️ **Warning:** This error is silently swallowed. At minimum, log it.
```

```
💡 **Suggestion:** This could be simplified with a dict comprehension:
`{k: v for k, v in items if v is not None}`
```

```
✅ **Nice:** Good use of context manager here - ensures cleanup on exceptions.
```

## For Local (Pre-Push) Review

When reviewing locally before push, use the same structure but present it as a message to the user instead of a PR comment. Skip the PR metadata header and just start with the severity sections.

## Health Audit Variant

For the read-only repo health audit (`references/repo-health.md`), use
this shape instead of the PR summary:

```markdown
## Repo Health: [owner/repo]

**Audited as:** [account] on [date]. Read only; nothing was changed.

| Check | State | Evidence |
|---|---|---|
| Auth context | [ok or finding] | [command and result] |
| Default branch | | |
| Protection and rulesets | | |
| CI presence and recent pass rate | | |
| Code scanning | | |
| Secret scanning and push protection | | |
| Dependabot | | |
| Templates and LICENSE | | |
| Repo structure audit | | |

### Findings
- **[severity]** [finding], evidence: [the read that proved it]
```

## Diagnostic Findings Shape (machine findings)

Machine findings (from CI gates or a requesting-code-review export)
are posted as individual review comments in this shape, never as one
summary comment. Filter to changed lines before posting; a finding on
an untouched line belongs in the summary, not inline.

```json
{"file": "path/in/repo.py", "line": 42, "severity": "critical | warning | suggestion", "message": "what is wrong and why", "source": "ci-gate | requesting-code-review | scanner name"}
```

Posting discipline for this shape lives in `references/code-review.md`.
