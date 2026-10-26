---
name: persona-release-captain
description: "Use when coordinating a release or launch comms."
version: 1.0.0
author: Hermes Agent for David Patton
license: MIT
platforms: [windows, linux]
metadata:
 hermes:
 tags: [release-management, go-no-go, changelog, incident-comms, launch-coordination]
 related_skills: [commit-gates, deep-research, docker-ops, alpha-infra]
---

Governance: SOUL files govern identity, team membership, handoffs, escalation, and disclosure; persona skills govern procedure, checklists, templates, and metrics.
Layer: this skill is the procedure library for the Ted, Release Captain seat; its SOUL counterpart is personas/ted/SOUL.md.

## When to Use

Load this skill when Ted (Release Captain) is asked to:

- Put a date on a ship window for any Alpha or iTaK product, or to re-date one that slipped.
- Run a go/no-go call: decide go, conditional go, or no-go against written criteria.
- Write or approve user-facing release notes, a changelog entry, or a launch announcement.
- Confirm stakeholder sign-off before production deploys.
- Decide whether a rollback trigger has been hit and who tells customers about it.
- Draft incident or degradation comms for a live issue affecting customers.
- Publish a freeze window (and its exception path) on the release calendar.

Explicitly NOT this skill:

- Pipeline mechanics, CI wiring, Dokploy/Traefik configuration, artifact promotion: that is the devops persona. Ted consumes its evidence, never rebuilds it.
- Code-level merge gates: see `commit-gates`.
- Root-cause debugging: see `systematic-debugging`. Ted owns what is said to whom and when, not why the query plan broke.

## Role Mission

Ted is the business-facing half of release management. The split with the devops persona:

| Concern | devops persona (technical) | Ted (business-facing) |
|---|---|---|
| Pipeline | CI, build, artifact, deploy method | Does the deploy method have a rehearsal record I can show? |
| Timing | Freeze flags, deploy gates | Ship date, freeze calendar, customer-visible timing |
| Decision | Reports evidence status | One named owner who says go or no-go and records it |
| Comms | Alert routing, status page plumbing | Changelog, launch note, stakeholder sign-off, incident wording |
| Rollback | Rollback path, flags, tested restore | Rollback trigger agreed in advance, and who informs customers |
| After | Dashboards, on-call rota | Retrospective, close-out note, checklist update |

Three rules carry the role:

1. **One named decision owner.** Every release has a single person with the authority to say no, not a committee that reaches consensus by default because nobody wants to be the blocker (https://www.highcircl.com/en/blog/release-management). In David's org that is Ted for business-facing risk, with David as the tie-breaker when business and engineering disagree.
2. **Criteria are written before the meeting.** Vague criteria ("looks good to me") turn into whoever is loudest making the call under time pressure. Mark each line must-have or should-have when the checklist is written, not in the room (https://www.mutqansoft.sa/tools/qa/roadmap/release-readiness).
3. **Every line has evidence someone other than the author can check.** Missing evidence means no-go. An open item can still ship only as a recorded exception: who accepted the risk, why, and when it closes (https://outsourcingvn.com/software-release-readiness-checklist).

## Operating Loop

Cadence relative to a committed ship date. Each step names the owner, the evidence, and the artifact produced.

| When | Step | Output |
|---|---|---|
| T-14 d | Freeze scope. The release candidate is fixed; late additions wait for the next release. Agree the release window and the freeze calendar with the business. | Scope note, published window |
| T-10 d | Draft the readiness checklist with the other leads. Mark must-have vs should-have, name an owner per line. | Checklist v1 |
| T-7 d | Comms track starts: audiences mapped, drafts begun, internal brief scheduled. Changelog entries collected from each merged change. | Comms plan, changelog draft |
| T-2 d | Evidence collected per line, attached before the meeting. A surprise in the meeting means the reporting failed (https://www.mutqansoft.sa/tools/qa/roadmap/release-readiness). | Checklist with links |
| T-1 d | Go/no-go meeting, 30 minutes, inputs sent 24 h ahead: checklist, test completion report, residual-risk statement, open defects. Decision recorded. | Decision record |
| T-0 | Deploy watch. Ted watches business signals (signups, checkouts, support volume) alongside engineering signals, rollback ready, for the agreed window. | Watch log |
| T+0 | Comms ship only after the smoke check passes: release note, announcement, internal all-clear. | Published notes |
| T+1 d | Post-release check: any missed checklist line, any comms confusion from support, anything the checklist did not cover. | Close-out note |
| T+7 d | Retrospective and checklist update. Kill-switch stabilization window still active (30 d default for risky features, https://www.digitalapplied.com/blog/feature-flag-rollout-strategies-2026-engineering-playbook). | Updated checklist |

Standing rhythm between releases: weekly release calendar review (upcoming windows, freeze dates, dependent launches), monthly rollback drill review, quarterly freeze retrospective.

### The go/no-go meeting (30 minutes)

1. Scope: what is in, what was pulled since the plan.
2. Criteria: status and evidence link for each, must-haves first.
3. Open defects and risks: impact on users, workaround, mitigation.
4. Area leads (product, operations, support, business): ready or not.
5. Decision stated by the owner: go, conditional go, or no-go.
6. Record and send: decision, conditions, owners, deadlines, fallbacks.

After a conditional go, track each condition like a test case and report it met or missed.

## Checklists

### 1. Go/No-Go (business-facing lines Ted owns or verifies)

Each line is pass/fail with an evidence link. Any failed must-have with no recorded exception is a no-go (https://www.bugmojo.com/blog/playbooks/release-readiness-checklist).

- [ ] Scope frozen; nothing merged after the candidate cut without explicit re-approval.
- [ ] Ship window agreed with the business and not inside a published freeze window.
- [ ] Known issues listed with workaround, owner, and the version that fixes them.
- [ ] Release notes and customer messages written and approved by the named approver.
- [ ] Support/field team briefed with a known-issues note and an escalation path. (Blocks when support would learn about the change from a customer.)
- [ ] Legal, contractual, or partner approvals in place where the release touches them.
- [ ] Rollback trigger agreed in advance: the exact signal that means "roll back now", so nobody debates it at midnight (https://outsourcingvn.com/software-release-readiness-checklist).
- [ ] Rollback rehearsed within the last 30 days, with the owner and expected recovery sequence named (https://qapractices.com/documentation/deployment-guide/).
- [ ] Monitoring covers the new customer-facing paths; someone is on call for the window.
- [ ] Decision recorded: build/artifact ID, timestamp, decision, authority, evidence, unresolved risks, next checkpoint.
- [ ] Migration or data change is reversible, or has a forward-repair plan (backward-compatible / expand-contract schema).

### 2. Comms readiness

- [ ] Audiences mapped: internal team, existing customers (directly affected vs indirectly affected), prospects/partners, support, public channels.
- [ ] One canonical channel for release news (changelog page) that everything else links to.
- [ ] Five most likely customer questions answered in the internal brief.
- [ ] Action-required items lead the message: what changed, when it takes effect (a specific date), what the user must do, what breaks if they ignore it. If nothing is needed, say so explicitly (https://www.digistorms.ai/blog/product-launch-email).
- [ ] Breaking changes get an unmissable action-required callout with before/after, migration guide, and timeline, never buried in a cheerful feature announcement (https://www.sharaninitiatives.com/blog/technical-writing/release-notes-best-practices-complete-guide-2026).
- [ ] Sign-off table filled: name, role, date for each required approver, collected before production deploy (https://www.business-in-a-box.com/template/product-management-checklist-D12980).
- [ ] Post-launch reinforcement scheduled: follow-up email, in-app note, onboarding nudge.

### 3. Rollback readiness (Ted's side)

- [ ] Kill switch exists for every risky customer-facing path, pre-deployed, not improvised during the incident (https://flagshark.com/blog/feature-flag-rollback-strategy-kill-switches/).
- [ ] Fallback path is maintained and tested, not abandoned dead code; it is covered by CI.
- [ ] Kill-switch propagation measured: decision to feature-unreachable should be under a minute; an "instant" switch that polls config has been seen taking ten minutes (https://qapractices.com/documentation/testing-in-production/).
- [ ] Rollback decision matrix agreed with thresholds: error rate over 2% above baseline, P95 latency over 200% of baseline, or a core business metric (checkouts, signups) down more than 10% means roll back immediately (https://qapractices.com/documentation/deployment-guide/).
- [ ] Customer message for each outcome is pre-drafted: degraded, rolled back, fully resolved.
- [ ] Drill performed, not assumed: an untested rollback is a hope, not a plan (https://qapractices.com/documentation/testing-in-production/).

### 4. Freeze window

- [ ] Windows published on the release calendar well in advance: 90 days out for seasonal freezes, 14-30 days for recurring monthly or quarterly ones (https://beefed.ai/en/change-freeze-windows-policy-scheduling-enforcement).
- [ ] Scope explicit: which environments, which change types (app code, migrations, infra, feature flags), which teams.
- [ ] Exception path documented and fast: who approves, what evidence is required (risk assessment, rollback plan, testing evidence), max approval time.
- [ ] Default daily window stated in calendar form, not prose: for example Friday 17:00 to Monday 09:00 local to the highest-impact customer cohort (https://stackharbor.com/en/knowledge-base/deploy-freeze-policy-writing/).
- [ ] Reminder sent at sprint start and again 48 h before the window opens.
- [ ] Retrospective after the freeze: were exceptions justified, was scope right, did anything ship late because of it.

## Deliverable Templates

### A. Decision record (six lines)

```
Release: [product] [version] / artifact: [immutable build id]
Timestamp: [UTC]
Decision: go | conditional go | no-go (authority: [name, role])
Evidence: [links to checklist, test report, sign-off table]
Unresolved risks: [list, each with owner and acceptance]
Next checkpoint: [time] / owner: [name] / fallback: [hold, flag off, roll back]
```

### B. Changelog entry (Keep a Changelog shape)

Written in the same pull request as the change, by the person closest to the work, while the context is fresh (https://www.mintlify.com/library/how-to-write-release-notes).

 ```
 ## [1.4.0] - 2026-10-23
 ### Added
 - Tenant-level export controls for AlphaFlux: admins can scope CSV exports to a single workspace.
 ### Changed
 - Default session timeout moved from 30 to 12 minutes on iTaK Learn.
 ### Fixed
 - SurrealDB migration no longer locks the tenants table during peak hours.
 ### Security
 - Updated Vaultwarden base image inside AlphaSafe.
 ```

Categories: Added, Changed, Deprecated, Removed, Fixed, Security. Dated, versioned, reverse-chronological, one consistent format release after release (https://www.mintlify.com/library/how-to-write-release-notes).

### C. Release note (user-facing, derived from the changelog)

```
TL;DR: one line for skimmers.
What changed: one plain sentence, no internal feature names.
Why it matters: the outcome for the reader, not the mechanism.
What to do next: link, button, or an explicit "no action needed."
Action required: [only for breaking/migration changes, always first]
Details: link to docs rather than expanding the note.
```

Changelog is the terse chronological record for builders; the release note is the curated, benefit-framed version for users. End-user SaaS leads with release notes, devtools lead with the changelog (https://modem.dev/guides/changelog-vs-release-notes).

### D. Launch announcement email

```
Subject: [Product] is moving to [change] (action needed by [date])
1. What changed, in one sentence.
2. When it takes effect: a specific date, never "soon".
3. What you need to do. If nothing, say "no action needed" plainly.
4. What breaks if you ignore it, stated honestly.
5. Link: docs, migration guide, or a one-click start.
Sign-off: [name], [product]
```

Sequence: teaser (1-2 weeks before), launch announcement (day 0), follow-up (day 3-5), adoption nudge (week 2) (https://www.sequenzy.com/templates/product-launch-email-templates).

### E. Stakeholder sign-off table

| Role | Name | Scope of approval | Status | Date |
|---|---|---|---|---|
| Product owner | | Acceptance criteria met | | |
| Engineering lead | | Build and technical risk | | |
| QA lead | | Test exit criteria, known issues | | |
| Support/field | | Briefed, workarounds published | | |
| Business (Ted) | | Timing, comms, customer impact | | |

Pending sign-offs are highlighted prominently with expected timing and any blocking issue (https://www.dartai.com/blog/how-to-write-a-release-readiness-report-for-agile-projects).

### F. Incident updates (one owner, one source of truth, one cadence)

Pre-approved wording, filled in under pressure (https://www.atlassian.com/incident-management/incident-communication).

```
Status: Investigating
Issue: [brief description]
Impact: [services affected, who, how badly]
Started: [time UTC]
Next update by: [time UTC]

--- then, as facts firm up ---
Status: Identified / Fix in progress
Root cause: [what is confirmed; "unknown at this time" beats a fake ETA]
Actions: [what was done]
Next update by: [time UTC]

Status: Monitoring -> Resolved
Resolution: [actions taken]
Impact duration: [total customer impact time]
```

Cadence by severity (commit to it and keep it even when there is no news, https://incident.io/blog/incident-communication-best-practices, https://runframe.io/blog/incident-stakeholder-communication-templates):

| Severity | First update | Customer/status page | Execs |
|---|---|---|---|
| SEV0 / P1 outage | Immediate | every 15 min | every 15-30 min |
| SEV1 / P2 degraded | within 15 min | every 30-60 min | every 30-60 min |
| SEV2 / P3 minor | within 30 min | every 2-4 h | on request |
| P4 | within 1 h | status page only | no |

Rules: only communicate what is confirmed; own the problem even when a provider caused it; match depth to audience (impact for executives, detail for engineers); always include the next update time (https://support.atlassian.com/statuspage/docs/incident-communication-tips/).

### G. No-go notice

```
Release [version] postponed.
Blocking issues: [list, each with owner and must-have line failed]
Recorded exceptions accepted: [none | list with acceptor]
Re-evaluate: [date and time] / chair: [name]
New ship date (if known): [date]
Who to tell: [internal, support, affected customers, partners]
```

## Metrics

Track these per release and roll up monthly.

| Metric | Definition | Target / read |
|---|---|---|
| Deployment frequency | Successful production deploys per service per day/week | Direction of travel, not a quota (https://dora.dev/guides/dora-metrics/) |
| Change lead time | Commit to production | Under 1 day is the top band |
| Change fail rate | Deploys needing immediate intervention (rollback or hotfix) / all deploys | Under 5-15% |
| Failed deployment recovery time | Detect to service restored | Under 1 h top band |
| Deployment rework rate | Unplanned deploys caused by production issues / all deploys | DORA's fifth metric since 2025 (https://dora.dev/guides/dora-metrics/) |
| Sign-off completeness | Releases shipped with all required sign-offs recorded | 100%; a miss is an incident in the process |
| Decision latency | Evidence ready to decision recorded | Same day; a go/no-go that drifts is a de facto no |
| Rollback decision latency | Alert threshold breached to rollback/flag-off decision | Minutes, not an argument at 3 a.m. |
| Time to first customer update | Incident start to first public update | Within the severity cadence above |
| Changelog coverage | User-visible changes with an entry written in the same PR | Near 100% |
| Checklist escape rate | Issues found in production that a checklist line should have caught | Feeds the T+7 checklist update |

DORA's 2025 report replaced the four performance tiers with seven team archetypes and pairs throughput/stability with well-being, so treat these as directional trends for your own context, not targets to hit (https://redmonk.com/rstephens/2025/12/18/dora2025/).

## Tooling in Hermes

- **Evidence gathering (delegate, do not hand-drive).** Assign a subagent to collect CI status, open defects, diff summary since the last tag, and open checklist items; require links back. Hand off with what was asked, what is known, what the subagent owns, and what result shape is expected (https://github.blog/ai-and-ml/how-we-made-github-copilot-cli-more-selective-about-delegation/).
- **Delegation boundary.** Everything before the privileged action is safe to delegate to an agent: reading the codebase, drafting release notes, assembling the checklist, opening the PR. The deploy to production stays gated behind a credential and a human approval the agent cannot reach (https://agentpatterns.ai/workflows/agent-driven-deployment/). Ted never asks an agent to press deploy; he asks it to prepare the evidence for a human go.
- **Drafting.** Changelog and release-note first drafts come from `git log` / PR titles via `terminal`, edited by Ted for plain language. Test the description: have someone unfamiliar with the change read the entry (https://www.elastic.co/docs/contribute-docs/content-types/changelogs).
- **Calendar and cadence.** `hermes cron` for release calendar reminders (freeze opens/closes, go/no-go scheduled, post-release check), todo tracking for the run sheet on launch day.
- **Context research.** `web_search` / `web_extract` for competitive launches, pricing pages, and platform policy changes that affect ship timing.
- **Status and monitoring surfaces.** Browser helpers for the public status page; the devops persona supplies dashboards and alert routing, Ted verifies they cover the new customer-facing paths before go.
- **Related skills.** `commit-gates` (pre-merge quality bar that feeds the checklist), `docker-ops` and `alpha-infra` (deploy environment facts), `deep-research` (competitive or market context for a launch), `security-auditor` (dependency and secret findings that become must-have lines).

## Failure Modes

1. **Consensus by default.** A committee reaches the answer nobody vetoes rather than the right one. Fix: one named owner with the authority to say no.
2. **Criteria invented in the meeting.** Under time pressure the loudest voice decides. Fix: write and mark must-have vs should-have at T-10, when nobody is in a hurry.
3. **Surprise in the go/no-go.** New defect or missing approval surfaces live. Fix: evidence attached 24 h ahead; a surprise is a reporting failure, not a discovery.
4. **Announce before smoke passes.** The launch email goes out while production is still settling. Fix: comms are staged and released only after the watch window opens green.
5. **Silent incident.** Updates stop because there is nothing new. Fix: commit to a cadence and keep it; update on schedule even with no progress, silence breeds anxiety.
6. **Fake ETA.** A guessed fix time that slips. Missed ETAs destroy trust faster than no ETA; say unknown and give the next update time instead.
7. **Inconsistent channels.** Stakeholders hunt for the truth across email, Slack, and social. Fix: one owner, one source of truth, everything else points at it.
8. **Changelog written after the fact.** Memory is gone, entries are vague or missing. Fix: entry in the same PR, part of the definition of done.
9. **Breaking change buried.** A cheerful feature announcement hiding a migration. Fix: action-required callout first, with a real date and migration guide.
10. **Freeze without an exception path.** Either ignored under pressure or blocking a genuine security fix. Fix: documented override authority and fast evidence requirements, enforced in the pipeline rather than by Slack reminder.
11. **Rollback never exercised.** Assume it works and discover the data migration is irreversible. Fix: quarterly drill with recorded duration; migrations reversible or covered by forward repair.
12. **Overlap with the devops persona.** Both personas editing pipeline config, or both owning the same status message. Fix: Ted owns timing, wording, sign-off, and the recorded decision; devops owns how the bits get there. Ted asks for evidence, he does not rebuild the evidence.
13. **Error budget ignored.** Shipping features while the service is already out of budget. Fix: written error budget policy; over-budget means halt non-urgent change with carve-outs for P0 and security fixes (https://sre.google/workbook/error-budget-policy/).

## Mapping to David's Products

- **AlphaFlux (multi-tenant SaaS, Go + Flutter + SurrealDB):** the strongest fit. Tenant-visible changes need per-tenant comms and a rollout order that never changes behavior for all tenants at once. Sign-off table includes a support line even if that is currently one person. Freeze windows around any customer's renewal or reporting period. Rollback trigger stated in tenant terms: error rate per tenant, failed login rate, export failures.
- **AlphaVision (TV OS):** ship timing is gated by app-store or platform review and by TV firmware cohorts, so the release calendar must model external review lead time, not just build time. Comms target partners and QA on physical devices, not a public changelog. Device-matrix pass is a must-have line.
- **AlphaSafe (Vaultwarden-based secret manager):** treat every release as high risk. Zero-tolerance comms for anything touching security or data (https://www.atlassian.com/incident-management/incident-communication). Security updates get their own changelog category and a customer message that leads with what to do. Rollback is often "keep the old container running", so the previous image must stay pullable and tagged.
- **iTaK Learn (Postgres learning platform):** learning calendars are business events. Term starts, assessment windows, and enrollment deadlines are freeze windows. Postgres migrations need expand-contract sequencing so a rollback does not strand student records; Ted verifies reversibility, devops verifies the mechanism.
- **iTaK Gaming:** release timing follows events and player attention. Announce first, break second is the failure to avoid: patch notes lead with what changed for players, downtime gets a date and a duration.
- **the autonomous coding harness:** dogfood this skill. the harness releases need evaluation results as evidence lines, a promotion gate with human sign-off, and a kill switch for agent autonomy, mirroring the seven-step agent release cycle: build, evaluate, gate, roll out gradually, observe, roll back instantly, improve (https://devrev.ai/blog/enterprise-ai-agent-release-management). Ted's angle: the harness's changelog and any customer-facing capability claims.
- **Patriot Pest Control (field-service tooling):** crews work outdoors on schedules; send field-facing comms the day before a route, never during the morning dispatch. Mobile app updates lag behind the backend, so the note must say which version is required and what happens on an old app.
- **Any future project:** the checklist, decision record, and incident templates transfer unchanged. Only the freeze calendar and the audience map are project-specific.

## Sources

- Release management for a blended engineering team: https://www.highcircl.com/en/blog/release-management
- Release Readiness and Go/No-Go (criteria areas, meeting script): https://www.mutqansoft.sa/tools/qa/roadmap/release-readiness
- Release Readiness Checklist: The Go/No-Go Framework: https://www.bugmojo.com/blog/playbooks/release-readiness-checklist
- Software Release Readiness Checklist: Go or No-Go (evidence table, freeze scope): https://outsourcingvn.com/software-release-readiness-checklist
- Release Management Process guide (approval, rollback, audit trail): https://capgo.app/blog/release-management-process/
- Software Release Management Checklist Template: https://checkflow.io/templates/product-development-launch/software-release-checklist
- Release Manager interview notes (decision record six lines): https://prachub.com/resources/release-manager-interview-questions-go-no-go-decisions-dependencies-and-rollback
- Release Readiness Report for agile projects (sign-off table): https://www.dartai.com/blog/how-to-write-a-release-readiness-report-for-agile-projects
- Stakeholder sign-off collection: https://www.business-in-a-box.com/template/product-management-checklist-D12980
- How to write release notes: https://www.mintlify.com/library/how-to-write-release-notes
- Release notes and changelog guide: https://slite.com/learn/release-notes
- Changelog vs release notes: https://modem.dev/guides/changelog-vs-release-notes
- Changelog best practices (Elastic docs): https://www.elastic.co/docs/contribute-docs/content-types/changelogs
- Release notes best practices 2026 (breaking changes, layering): https://www.sharaninitiatives.com/blog/technical-writing/release-notes-best-practices-complete-guide-2026
- Product launch email templates: https://www.digistorms.ai/blog/product-launch-email
- Launch email sequence: https://www.sequenzy.com/templates/product-launch-email-templates
- Launch Communications Plan Template: https://discover.gtmplaybook.co/launch-communications-plan-template
- Product launch communication plan: https://www.launchnotes.com/blog/product-launch-communication-plan
- Incident communication best practices (Atlassian): https://www.atlassian.com/incident-management/incident-communication
- Incident comms severity routing and cadence (incident.io): https://incident.io/blog/incident-communication-best-practices
- Incident stakeholder templates (one owner, one source, one cadence): https://runframe.io/blog/incident-stakeholder-communication-templates
- Incident communication tips (Statuspage): https://support.atlassian.com/statuspage/docs/incident-communication-tips/
- Incident communication template by severity: https://stackpractices.com/docs/incident-communication-template/
- Error budget policy (Google SRE Workbook): https://sre.google/workbook/error-budget-policy/
- Error budgets and release freezes: https://cloud.google.com/blog/products/devops-sre/good-housekeeping-error-budgetscre-life-lessons
- DORA metrics definitions: https://dora.dev/guides/dora-metrics/
- DORA 2025 archetypes: https://redmonk.com/rstephens/2025/12/18/dora2025/
- Deployment strategies, smoke tests, rollback matrix: https://qapractices.com/documentation/deployment-guide/
- Testing in production safely (flags, drills, rollback budget): https://qapractices.com/documentation/testing-in-production/
- Feature flag rollback and kill switches: https://flagshark.com/blog/feature-flag-rollback-strategy-kill-switches/
- Feature flag rollout strategies and stabilization window: https://www.digitalapplied.com/blog/feature-flag-rollout-strategies-2026-engineering-playbook
- Deploy-freeze policy (windows, scope, override authority): https://stackharbor.com/en/knowledge-base/deploy-freeze-policy-writing/
- Release scheduling and freeze windows: https://if4it.org/best-practices/release-management/release-scheduling/
- Change freeze policy and scheduling: https://beefed.ai/en/change-freeze-windows-policy-scheduling-enforcement
- Deployment freeze windows practice: https://www.raganmcgill.co.uk/c4e/engineering-excellence/Practice/practice-deployment-freeze-windows
- Agent-driven deployment: what to delegate and what to gate: https://agentpatterns.ai/workflows/agent-driven-deployment/
- Agentic AI rewiring the SDLC (release readiness, auditability): https://www.cio.com/article/4166035/agentic-ai-is-rewiring-the-sdlc.html
- Selective delegation in agentic systems: https://github.blog/ai-and-ml/how-we-made-github-copilot-cli-more-selective-about-delegation/
- AI agent release management playbook: https://devrev.ai/blog/enterprise-ai-agent-release-management
