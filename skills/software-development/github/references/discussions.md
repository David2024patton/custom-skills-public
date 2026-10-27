# Discussions: Triage and Conversion

Route here for GitHub Discussions work: triage, categories, answering,
and converting a discussion to an issue.

## Category discipline

Discussions live in categories the repo defines (announcements, ideas,
Q and A, general, or the repo's own set). Triage means every open
discussion is in the category its content belongs to: a bug report
sitting in Q and A is misfiled, and a feature idea is not a question.
Move or recategorize before answering where the tooling allows, and
say in a comment when you do.

## Triage pass

```bash
gh api graphql -f query='query { repository(owner: "<owner>", name: "<repo>") { discussions(first: 30, orderBy: {field: CREATED_AT, direction: DESC}) { nodes { number title category { name } answered isAnswered url } } } }'
```

For each unanswered discussion: answer it if the answer is known from
the repo's own docs or code, link the issue if it is a known bug, or
convert it (below) if it is actionable work. Mark the correct reply as
the answer on Q and A categories once the asker or the evidence
confirms it solves the question:

```bash
gh api graphql -f query='mutation { markDiscussionCommentAsAnswer(input: {discussionId: "<id>", commentId: "<id>"}) { discussion { isAnswered } } }'
```

Read the discussion back after marking; `isAnswered` in the response
is the proof.

## Converting to an issue

A discussion becomes an issue when it describes concrete, actionable
work the maintainers accept. Convert with linkage both ways: the issue
body names the discussion URL and number, and a discussion comment
names the new issue. Never let the conversion orphan the thread.

```bash
gh issue create --title "<title>" --body "Created from discussion #<N> (<URL>). <summary of the agreed work>"
gh api repos/{owner}/{repo}/issues/<ISSUE_NUMBER>/comments -f body="Tracked as issue #<ISSUE_NUMBER>."
```

## Done

Each discussion touched is read back in its new state (category,
answered flag, or linked issue), and conversions link both directions.
