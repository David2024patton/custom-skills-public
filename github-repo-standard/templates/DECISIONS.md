<!--
INSTRUCTIONS FOR THIS FILE (user and AI: read before editing. Keep this header.)

WHAT THIS FILE IS: the settled-decision log for this project. IDEA.md is
the raw capture of what David said; this file is only the calls that are
FINAL, so no one re-asks a settled question or quietly reverses a call.

EXACT STRUCTURE: one entry per decision, newest first, in this single
rolling file (never split it by year or topic):
## <YYYY-MM-DD>: <decision in one line>
- **Decided:** <what was picked>
- **Why:** <the reason, in plain words>
- **Consequences:** <what follows from the call: what changes, what
  it costs, what to watch>
- **Supersedes:** <the earlier call it replaces, or "none">
- **Status:** <active, or superseded by entry N, or reversed by
  entry N>
- **By:** David | <who, with David's approval noted>

RULES:
- A decision enters here the day it is made, in the same pass as any
  PLAN or TODO change it causes.
- Reversing a decision means a NEW entry that names what it supersedes;
  never edit an old entry into a different decision.
- When a later entry supersedes or reverses a decision, update the old
  entry's Status line to name the new entry; that Status update is the
  only edit an old entry ever gets.
- No secrets, passwords, or tokens in this file, ever.
-->
# DECISIONS: <Project Name>

<!-- Filled example entry, written in the format above. Replace it
with the project's first real decision, or delete it once real
entries exist. -->

## 2026-01-15: Example: session data is stored server side
- **Decided:** User sessions are stored server side, keyed by an
  opaque random token that the client holds and presents.
- **Why:** Server side storage lets a compromised session be revoked
  at once, which a self-contained client token cannot do.
- **Consequences:** The server needs a session store with expiry and
  cleanup from the first release, and every request pays one store
  lookup; token handling code must never log the token.
- **Supersedes:** none
- **Status:** active
- **By:** David
