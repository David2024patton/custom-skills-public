# Projects (v2): Boards, Fields, and Iterations

Route here for project boards and roadmaps: items, fields, views, and
iteration planning. Projects v2 is GraphQL only; there is no REST
surface and the `gh` porcelain is thin, so work through `gh api
graphql` with the patterns here and in the cheatsheet.

## Fields and items

```bash
# Project fields
gh api graphql -f query='query { organization(login: "<org>") { projectV2(number: <N>) { id title fields(first: 30) { nodes { ... on ProjectV2FieldCommon { name dataType } } } } } }'
# Items with their field values
gh api graphql -f query='query { organization(login: "<org>") { projectV2(number: <N>) { items(first: 50) { nodes { id content { ... on Issue { number title state } ... on PullRequest { number title state } } fieldValues(first: 20) { nodes { ... on ProjectV2ItemFieldSingleSelectValue { name } ... on ProjectV2ItemFieldTextValue { text } } } } } } }'
```

## Adding issues and PRs

```bash
gh api graphql -f query='mutation { addProjectV2ItemById(input: {projectId: "<project-id>", contentId: "<issue-or-pr-node-id>"}) { item { id } } }'
```

Get node IDs from the issue or PR itself (`gh issue view <N> --json
id`). Read the item list back after adding; the new item's presence in
a fresh read is the proof, not the mutation response alone.

## Setting a field value

```bash
gh api graphql -f query='mutation { updateProjectV2ItemFieldValue(input: {projectId: "<project-id>", itemId: "<item-id>", fieldId: "<field-id>", value: {singleSelectOptionId: "<option-id>"}}) { projectV2Item { id } } }'
```

## Iteration planning and status updates

- Iterations are a field type, not a separate object: read the field's
  configuration to learn the current iteration windows before moving
  items between them.
- A status update is a dated post on the project (GraphQL
  `createProjectV2StatusUpdate`); write it like a report: what moved,
  what is blocked, what changed since the last update, each claim
  backed by an item read from this session.
- Views are presentation. Changing a view never changes item data;
  say which one you changed.

## Done

Every add, move, or field change is verified by a fresh items read,
and status updates cite item states read in the same session.
