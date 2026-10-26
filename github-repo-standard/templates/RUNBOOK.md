<!--
INSTRUCTIONS FOR THIS FILE (user and AI: read before editing. Keep this header.)

WHAT THIS FILE IS: the operations book for this project, at docs/RUNBOOK.md.
How to build it, run it, deploy it, verify it, and where everything lives,
so anyone can operate the project without tribal knowledge.

EXACT STRUCTURE:
- "## Build": the real commands, copied from the working build.
- "## Run locally": how to start it and what you should see.
- "## Deploy": where it is hosted, how a deploy happens, how to roll back.
- "## Verify": the checks that prove it works after a change or deploy.
- "## Where things live": hosts, services, dashboards, and WHERE
  credentials are stored (names of vault entries or connectors only).
- "## Gotchas": the traps already learned the hard way, each with its fix.

RULES:
- NEVER a credential value in this file: no passwords, keys, or tokens.
  Pointers to secure storage only.
- Commands are copied from what actually works; if a command changes,
  this file changes in the same commit.
- No secrets, passwords, or tokens in this file, ever.
-->
# RUNBOOK: <Project Name>

## Build
<commands>

## Run locally
<commands and expected output>

## Deploy
<hosting, deploy path, rollback>

## Verify
<checks>

## Where things live
<hosts, services, credential storage pointers by name only>

## Gotchas
- <trap> (fix: <fix>)
