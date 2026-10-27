# Signature library

Checkable, describe-only signatures for known flaw classes. The critic never sends exploit traffic; a signature describes how to establish runtime state from evidence.

Each entry carries: the flaw IDs and scores (with the scoring disagreement rule stated where scorers diverge), the affected surface, the fixed releases, three-state semantics (OK 0, VULNERABLE 1, UNKNOWN 3), and the checks in priority order. An entry carries verified_as_of and expires 90 days later; an expired entry is flagged in the report header.

Entries:

- `SIG-PHP-2026-001.yaml`: the PHP2Shell pair, CVE-2026-109618 and CVE-2026-109619, fixed in PHP 8.5.12, 8.4.27, 8.3.36, and 8.2.35. The signature is runtime state, not a version string alone, because distro backports can fix without a version bump.

New signatures join this library in the same format: one file per signature, ID of the form SIG-<STACK>-<YEAR>-<NNN>, seeded by the worked example that proved the pattern.
