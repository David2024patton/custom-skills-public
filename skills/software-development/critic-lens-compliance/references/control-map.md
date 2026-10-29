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
| C7 | Vulnerability management (scan, patch SLA) | CC7.1 | Art 32 | A.8.8, A.8.9 | ID.RA-01 | scripts/common/vuln-scan.sh output, scripts/intel-refresh.py stamps (KEV, EPSS, OSV ages), patch log |
| C8 | Incident response (plan, breach clock) | CC7.4, CC7.5 | Art 33, 34 (72h) | A.5.24-5.26 | RS.RP-01 | IR plan file, on-call, clock owner |
| C9 | Backup and tested restore | CC7.4 | Art 32(1)(c) | A.8.13 | PR.IP-04 | backup job, last restore test record |
| C10 | Personal-data inventory (what/where/why) | - | Art 30 | A.5.34 | GV.RR-05 | data map doc, DB schema annotation |
| C11 | Lawful basis and consent | - | Art 6, 7 | A.5.10(a) | GV.PO-05 | consent capture records; the in-bundle MMS checks (checklist item GROWTH-MMS-001) for the tracking surface the consent governs |
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

## Framework addenda: the same controls, mapped

One evidence pass answers every framework in the run's scope: each control
below carries the addendum framework's own reference for the duty it
discharges. A control not listed under a framework imposes no duty under
that framework in this library; verdicts still use the vocabulary below,
per framework column.

### CCPA / CPRA (California)

| Control | CCPA reference |
|---|---|
| C1 | §1798.150 (reasonable security duty behind the private right of action) |
| C5 | §1798.130 (records supporting rights responses) |
| C10 | §1798.100(b) (notice at collection: categories and purposes) |
| C11 | §1798.100(b), §1798.120 (notice; opt-out of sale or sharing) |
| C12 | §1798.100 (know), §1798.105 (delete), §1798.106 (correct), §1798.121 (limit sensitive data) |
| C13 | §1798.100(a)(3) (retention period or criteria, disclosed) |
| C15 | §1798.140 (contractor and service-provider contract terms) |

### FERPA (student education records, 34 CFR Part 99)

| Control | FERPA reference |
|---|---|
| C1 | §99.31 (disclosure only under a named condition), §99.20 (rights transfer at 18) |
| C2 | §99.31 (authentication before disclosure) |
| C5 | §99.32 (record of disclosures, kept with the record) |
| C10 | §99.10 (parent or eligible student inspection) |
| C12 | §99.20 to §99.22 (amendment of inaccurate records, hearing) |
| C15 | §99.31(a)(1)(i)(B) (school-official exception: vendor under direct control) |
| C17 | §99.7 (annual notification of rights) |

### COPPA (children under 13, 16 CFR Part 312)

| Control | COPPA reference |
|---|---|
| C1 | §312.8 (confidentiality and security of children's data) |
| C4 | §312.8 (security program, encryption in custody) |
| C10 | §312.4 (direct notice: what is collected and why) |
| C11 | §312.5 (verifiable parental consent before collection) |
| C12 | §312.6 (parental review, refusal, and deletion) |
| C13 | §312.10 (retain only as reasonably necessary, then delete) |
| C15 | §312.8 (service providers bound to the same duties) |

### PCI-DSS v4 (SAQ-A scope: hosted processor, no card data in our systems)

| Control | PCI-DSS reference |
|---|---|
| C1 | Req 7, Req 8 (access by business need; identification) |
| C2 | Req 8 (authentication, MFA where the processor requires it) |
| C3 | Req 4 (encryption of cardholder data in transit; here: the hosted redirect) |
| C5 | Req 10 (logging of access to the payment integration) |
| C6 | Req 6 (change control over the integration) |
| C7 | Req 6, Req 11 (patching and scanning of the storefront surface) |
| C8 | Req 12 (incident response, including processor notification duties) |
| C15 | Req 12 (third-party service provider management: the processor's AOC on file) |
| C17 | Req 12 (the SAQ-A itself, completed and dated) |

### HIPAA (scope-activated: only when health data enters scope)

| Control | HIPAA reference |
|---|---|
| C1 | §164.312(a) (access control), §164.308(a)(4) (access authorization) |
| C2 | §164.312(d) (person or entity authentication) |
| C3 | §164.312(e) (transmission security) |
| C4 | §164.312(a)(2)(iv), §164.312(e)(2)(ii) (encryption) |
| C5 | §164.312(b) (audit controls), §164.308(a)(1)(ii)(D) (activity review) |
| C7 | §164.308(a)(1) (risk analysis), §164.308(a)(5)(ii)(B) (malicious-software protection) |
| C8 | §164.308(a)(6) (incident procedures), §§164.400 to 164.414 (breach notification) |
| C9 | §164.310(d)(2)(iv) (data backup plan) |
| C16 | §164.308(a)(3)(ii)(C) (termination procedures) |
| C17 | §164.316 (documented, versioned policies) |

### CMMC Level 2 (scope-activated: defense contracting; NIST SP 800-171 Rev 2 practices)

| Control | CMMC / 800-171 reference |
|---|---|
| C1 | 3.1.1, 3.1.2 (AC: limit access to authorized users and transactions) |
| C2 | 3.5.1, 3.5.3 (IA: identification, multifactor authentication) |
| C3 | 3.13.1, 3.13.8 (SC: boundary protection, cryptographic protection in transit) |
| C4 | 3.13.10, 3.13.16 (SC: key management, protect stored CUI) |
| C5 | 3.3.1, 3.3.8 (AU: audit records, protection of audit information) |
| C6 | 3.4.1, 3.4.2 (CM: baselines and controlled change) |
| C7 | 3.11.2, 3.14.6 (RA: periodic scanning; SI: monitoring) |
| C8 | 3.6.1, 3.6.2 (IR: incident handling and reporting) |
| C9 | 3.8.9 (MP: backup of CUI on protected media) |
| C15 | 3.12.1 (CA: periodic assessment of controls) |
| C16 | 3.9.2 (PS: personnel termination and transfer actions) |
| C17 | 3.12.4 (CA: system security plan), 3.12.2 (plans of action) |
| C18 | 3.10.1, 3.10.2 (PE: physical access limits and monitoring) |

## Verdict vocabulary

PASS (evidence cited), GAP (smallest fix named), INHERITED (provider named with
their report), NOT-APPLICABLE (reason named). A control with no evidence and no
owner is a GAP, never a PASS.
