# Runtime signatures (P-15)

Describe-only runtime-state signatures. The critic never sends exploit
traffic; a signature is checked as runtime state (the version that
serves, the SAPI in use, the patch state), never as a version string
alone, because distro backports can fix a flaw without a version bump.
A backport claim holds only with a vendor attestation naming the
signature ID, the vendor, and the vendor advisory ID, in that order
(see scripts/common/runtime-version.sh).

| ID | Flaw | File |
|---|---|---|
| SIG-PHP-2026-001 | PHP2Shell pair: CVE-2026-109618, CVE-2026-109619 | SIG-PHP-2026-001.yaml |
| SIG-PHP-2024-001 | PHP CGI argument injection: CVE-2024-4577 | SIG-PHP-2024-001.yaml |

Each entry names what it is NOT, so lookalike flaws are never merged:
attribution discipline is part of the library's job. New signatures
follow the same format (id, name, verified and expiry dates, per-CVE
GHSA and KEV state, affected scope, fixed releases per branch, the
three-state semantics, checks, and a not_this line).
