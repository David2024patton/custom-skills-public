# Master Control Library (one library, many frameworks)

Shared control set mapped across frameworks, EasyAudit-style. Evidence targets
are David's own repos and infra; adjust names per system under audit.
Mappings: SOC 2 = Trust Services Criteria CC-series; GDPR = article numbers;
ISO = 27001:2022 Annex A; NIST = CSF 2.0 function.practice.

| ID | Control | SOC 2 | GDPR | ISO 27001:2022 | NIST CSF 2.0 | Evidence to cite |
|---|---|---|---|---|---|---|
| C1 | Role-based access, least privilege | CC6.1-6.3 | Art 32 | A.5.15, A.8.2 | PR.AA-01 | auth/RBAC code file:line, role table |
| C2 | Authentication strength (MFA, sessions) | CC6.1 | Art 32 | A.8.5 | PR.AA-05 | login handler, session TTL config |
| C3 | Encryption in transit | CC6.7 | Art 32 | A.8.24 | PR.DS-02 | TLS config, HSTS, redirect enforcement |
| C4 | Encryption at rest, key custody | CC6.7 | Art 32 | A.8.24 | PR.DS-01 | DB/volume encryption, vault entries |
| C5 | Audit logging (who/what/when, retention) | CC7.2 | Art 30, 32 | A.8.15 | DE.CM-03 | audit log writer file:line, retention job |
| C6 | Change management (review, gates, trace) | CC8.1 | - | A.8.32 | GV.SC-08 | PR gates, commit-gates law, CI config |
| C7 | Vulnerability management (scan, patch SLA) | CC7.1 | Art 32 | A.8.8, A.8.9 | ID.RA-01 | threat-feed.sh, trivy cadence, patch log |
| C8 | Incident response (plan, breach clock) | CC7.4, CC7.5 | Art 33, 34 (72h) | A.5.24-5.26 | RS.RP-01 | IR plan file, on-call, clock owner |
| C9 | Backup and tested restore | CC7.4 | Art 32(1)(c) | A.8.13 | PR.IP-04 | backup job, last restore test record |
| C10 | Personal-data inventory (what/where/why) | - | Art 30 | A.5.34 | GV.RR-05 | data map doc, DB schema annotation |
| C11 | Lawful basis and consent | - | Art 6, 7 | A.5.10(a) | GV.PO-05 | consent capture (ad-tracking-pixels lens) |
| C12 | Data subject rights (access, erase, port) | - | Art 15-22 | A.5.10 | GV.PO-05 | DSAR route, erasure job file:line |
| C13 | Retention limits and deletion jobs | CC6.5 | Art 5(1)(e) | A.8.10 | PR.IP-04 | retention config, tombstone path |
| C14 | Tenant isolation (logical separation) | CC6.6 | Art 32 | A.8.5 | PR.AA-03 | tenancy tests, scoping middleware |
| C15 | Vendor and subprocessor management | CC9.2 | Art 28 | A.5.19, A.5.20 | GV.SC-04 | vendor list, DPAs, subprocessor page |
| C16 | Personnel offboarding, access revocation | CC6.2, CC6.3 | - | A.6.5 | PR.AA-02 | account lifecycle, key rotation record |
| C17 | Documented, versioned policy set | CC1.4, CC2.x | Art 24 | A.5.1 | GV.PO-01 | policy files, dated versions |
| C18 | Physical and media (inherited hosting) | CC6.4 | Art 32 | A.7.x | PR.PS-01 | provider SOC report named, scope noted |

ISO 42001 (AI management): scope-activated addendum for AI-feature runs (map
C1-C18 plus AI-specific items: model inventory, impact assessment, human
oversight of agent decisions) so one evidence pass also answers ISO 42001 and
ISO 27001 questionnaires together - the verify-once-map-everywhere rule.

Addenda when scope activates them: PCI-DSS (hosted processor SAQ-A, no card
data in our systems: document the processor and the redirect), FERPA/COPPA
(student records, under-13 data), A2P 10DLC (SMS campaign registration).

## Verdict vocabulary

PASS (evidence cited), GAP (smallest fix named), INHERITED (provider named with
their report), NOT-APPLICABLE (reason named). A control with no evidence and no
owner is a GAP, never a PASS.
