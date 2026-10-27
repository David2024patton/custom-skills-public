# Security Policy

<!--
INSTRUCTIONS FOR THIS FILE (user and AI: read before editing. Keep this header.)

WHAT THIS FILE IS: the public security policy for this repo, at the
repo root as SECURITY.md. It tells a reporter how to disclose a
vulnerability privately and tells readers which versions get fixes.

RULES:
- The contact below is a placeholder until the project fills in its
  real private reporting channel. Never publish a personal email or
  phone number here unless the project owner chose it in words.
- No secrets, passwords, or tokens in this file, ever.
-->

## Supported versions

| Version | Supported |
| :--- | :--- |
| Latest release | Yes |
| Older releases | No, upgrade to the latest release |

Replace this table with the project's real support window when the
project makes releases on a different rule.

## Reporting a vulnerability

Do not open a public issue for a security problem.

Report it privately through the channel the project names here:
**<security contact: replace with the project's private reporting
channel, for example GitHub private vulnerability reporting on this
repo, before publishing this file>**.

Include what you found, the version or commit you saw it on, and the
steps that reproduce it. The project aims to acknowledge a report
within 3 business days and to agree on a disclosure timeline with
the reporter before anything is published.

## Scope notes

- Credentials, keys, and tokens never belong in this repo; if you
  find one committed, treat it as a live secret, report it through
  the private channel above, and do not copy it into an issue.
- Fixes land through the normal gate process: the commit gates run
  clean and the change is proven before it ships.
