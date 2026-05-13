# PRD - Acme Corp Internal Employee Portal

> Status: Draft  
> Last updated: 2026-05-11  
> Author: RFP Workflow (golden reference)  
> PM Owner: TBD  
> Engineering Owner: Tom Bauer (IT Lead)  
> Design Owner: TBD  

---

## Revision Notes

- Golden artifact for eval harness: aligned to `examples/sample-rfp.md` only; not a live stakeholder sign-off.

---

## Problem Alignment

### Problem Statement

Acme’s legacy intranet fragments employee tasks across multiple tools and weak discovery paths. Staff cannot reliably find colleagues, consume official news, access HR artifacts, or retrieve governed documents in one place. IT spends disproportionate effort on access tickets and identity sprawl instead of improving self-service.

### Problem Alignment

- **Employees** lose time context-switching and face inconsistent mobile experience.  
- **HR** cannot scale self-service for payslips, leave, and entitlements without duplicating data entry.  
- **Communications** lacks a single channel for rich-text organizational news with clear ownership.  
- **IT** must enforce Azure AD–centric security and EU data residency without bespoke per-app policies.

---

## High Level Approach

### Summary

Deliver a **mobile-responsive internal web portal** on **Azure**, replacing the intranet as the day-one destination for authenticated staff. The portal uses **Azure AD SSO via SAML 2.0**, integrates **Workday** as the system of record for employee data, and provides directory search, HR self-service, an HR/Communications-owned news feed, and a **department-scoped document repository** with RBAC. **All production data and processing remain in the EU** to satisfy GDPR expectations stated in the RFP.

### Proposed Solution

- **Identity:** SAML 2.0 federation to the existing Azure AD tenant; session and token handling documented for security review.  
- **Core modules:** Directory, HR hub, News, Documents, Admin.  
- **Data sync:** Scheduled and/or event-driven Workday integration for profiles, org hierarchy, and HR fields needed for payslips, leave, and entitlements (exact fields clarified in Open Questions).  
- **Governance:** RBAC by department (and extensible roles), audit-friendly access patterns, EU-region hosting and backups.

#### Proposed Solution Infographics

- INF-01: (eval placeholder) high-level context — User → Portal → Azure AD / Workday / EU storage.  
- INF-02: (eval placeholder) journeys — “Find colleague”, “Submit leave”, “Read news”, “Open governed doc”.  
- INF-03: (eval placeholder) MVP slice vs post-MVP (if any deferrals agreed).

### Narrative

An employee opens the portal on a phone or laptop, signs in once with corporate credentials, lands on a personalized home experience, searches the directory, checks payslip or leave balance synced from Workday, reads the latest Communications post, and opens a department folder document they are authorized to see—without VPN friction or duplicate passwords.

### Goals

| Goal | Metric | Target |
|------|--------|--------|
| Reduce intranet-related support tickets | Tickets tagged intranet/access/month | −30% within 6 months post-MVP |
| HR self-service adoption | Active users completing ≥1 HR action/month | ≥60% of headcount by month 3 |
| Trust in official news | Click-through on pinned announcements | Baseline + agreed uplift with Comms |
| Performance on constrained networks | Median LCP (lab: 10 Mbps profile) | ≤3s on critical landing path |
| Compliance posture | EU data residency + GDPR DPIA status | EU-only prod; DPIA complete before go-live |

### Non-goals

- Replacing Workday as HR system of record.  
- Public internet or customer-facing portal capabilities.  
- Full digital workplace suite (email, calendar replacement) unless explicitly added later.

---

## Solution Alignment

### Personas / User Segments

| Persona | Needs | Pain Points |
|---------|--------|---------------|
| Employee | SSO, directory, HR tasks, news, docs on mobile | Legacy UX, multiple logins |
| HR (Sarah Mitchell) | Self-service, auditability, policy-aligned content | Manual rework, inconsistent data |
| IT (Tom Bauer) | Azure AD, EU hosting, operability | Fragmented integrations |
| Communications | Rich-text publishing workflow | No single official channel |
| Content admins | RBAC, folder structure, lifecycle | Ad-hoc permissions |

### Key Features

- SAML 2.0 SSO against existing Azure AD tenant.  
- Searchable employee directory with profile detail pages.  
- HR self-service: payslips, leave submission, entitlements (UX depth per Open Questions).  
- News feed with rich-text posts; authoring restricted to HR and Communications roles.  
- Document repository: folders, upload/download, RBAC by department (and admin overrides).  
- Admin panel for users, roles, and content/news administration within portal scope.

### Key Flows

1. **Authenticate:** SP-initiated SAML → Azure AD → portal session.  
2. **Directory:** Search → results → profile (fields sourced from Workday + optional manual overrides policy).  
3. **Leave:** View balance → submit request → status tracking (approval chain TBD).  
4. **News:** List/detail → rich-text render; optional attachments policy TBD.  
5. **Documents:** Browse tree → download/upload per ACL → virus scan policy TBD.

### Key Logic

- **RBAC:** Department membership drives default document visibility; admin roles can grant cross-department read where policy allows.  
- **EU residency:** All application tiers, object storage, databases, logs, and backups in EU Azure regions; subprocessors list maintained for GDPR.  
- **Performance:** Budget for cold vs warm assets; CDN in EU if used; lab validation against 10 Mbps target in NFR.

---

## Launch Plan

### In scope

- FR-01–FR-10 and NFR-01–NFR-03 as enumerated in Requirements (traceable to sample RFP).  
- MVP delivery **within 12 weeks** from project kickoff (RFP constraint).

### Out of scope

- Features not listed in the RFP unless added by change control.  
- Non-EU processing of production personal data.

### 4.1 MVP Scope

- Azure AD SAML SSO end-to-end for employees.  
- Directory search + profiles backed by Workday sync (MVP field set).  
- HR: payslip view, leave request submit, entitlements view (exact parity with Workday UI deferred if legally acceptable).  
- News: create/edit/publish for HR + Communications; employee read.  
- Documents: folders, upload/download, department RBAC, basic admin.  
- Mobile-responsive layouts for iOS Safari and Android Chrome.  
- Admin panel for users/content within portal boundaries.

### 4.2 Post-MVP / Future Scope

- Advanced analytics on readership and HR funnel.  
- Deeper workflow automation for leave approvals beyond Workday defaults.  
- Optional native apps (not required by RFP).

### Key Milestones

| Milestone | Date | Exit Criteria |
|-----------|------|----------------|
| Discovery & DPIA kickoff | Week 2 | Stakeholder map, data inventory draft |
| Architecture sign-off | Week 4 | HLD + EU region decision recorded |
| MVP feature complete | Week 10 | All Must requirements implemented in staging |
| UAT | Week 11 | Exit criteria signed by HR + IT |
| Go-live | Week 12 | Production cutover with rollback plan |

### Operational Checklist

- EU region deployment, key vault, secrets rotation.  
- Monitoring, alerting, on-call runbooks.  
- Backup and restore tested for RPO/RTO targets (see Open Questions).  
- Security review for SAML metadata, TLS, session fixation/hijack controls.

---

## Requirements

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|---------------|----------|--------|
| FR-01 | Users authenticate via Azure AD SSO using SAML 2.0 | Must Have | SP in EU; metadata exchange with IdP |
| FR-02 | Employee directory with search and profile pages | Must Have | PII minimization on profile |
| FR-03 | HR self-service: view payslips | Must Have | Source: Workday |
| FR-04 | HR self-service: submit leave requests | Must Have | Workflow per Workday/HR policy |
| FR-05 | HR self-service: view entitlements | Must Have | Definitions aligned with HR |
| FR-06 | Company news feed with rich-text posts | Must Have | Authors: HR + Communications only |
| FR-07 | Document repository: folders, upload, download | Must Have | Virus scan policy TBD |
| FR-08 | Document RBAC by department | Must Have | Extensible roles in admin |
| FR-09 | Admin panel for user and content management | Must Have | Scoped to portal objects |
| FR-10 | Integration with existing Workday for employee data sync | Must Have | Incremental sync + reconciliation job |

## Non-Functional Requirements

| ID | Requirement | Category | Notes |
|----|---------------|----------|--------|
| NFR-01 | Initial portal load ≤3 seconds on a 10 Mbps connection | Performance | Define “initial” as LCP on home/dashboard |
| NFR-02 | Mobile-responsive on iOS Safari and Android Chrome | UX / Compatibility | Test matrix in QA plan |
| NFR-03 | All data remains within the EU; GDPR-aligned controls | Security / Compliance | Art. 28 DPA with Azure; DPIA |

### Acceptance Criteria (Epic/Feature level)

- AC-01: SAML login completes for test users; logout and session expiry behave per policy.  
- AC-02: Directory search returns ranked results within agreed latency SLO.  
- AC-03: Payslip and entitlement views reflect Workday source within sync SLA.  
- AC-04: Leave submission creates/updates Workday records without duplicate submissions.  
- AC-05: Unauthorized users cannot open documents outside their RBAC scope (negative tests).  
- AC-06: Lab performance run documents meeting NFR-01 under defined profile.

### Traceability Matrix

| Requirement ID | Story/Epic Ref | Test Ref | Notes |
|----------------|----------------|----------|--------|
| FR-01 | EPIC-AUTH | TC-SAML-01 | Metadata + assertion validation |
| FR-02 | EPIC-DIR | TC-DIR-01 | Search + profile |
| FR-03–FR-05 | EPIC-HR | TC-HR-01..03 | Workday-backed |
| FR-06 | EPIC-NEWS | TC-NEWS-01 | Authoring gates |
| FR-07–FR-08 | EPIC-DOCS | TC-DOCS-01..02 | RBAC matrix |
| FR-09 | EPIC-ADMIN | TC-ADM-01 | Role separation |
| FR-10 | EPIC-INT | TC-WDAY-01 | Sync reconciliation |
| NFR-01 | EPIC-PERF | TC-PERF-01 | 10 Mbps lab |
| NFR-02 | EPIC-UX | TC-UX-01 | Device matrix |
| NFR-03 | EPIC-COMP | TC-GDPR-01 | Region + subprocessors |

---

## Technical Considerations

### Architecture Notes

- Prefer managed Azure services in a **single EU geography** for app, API, DB, and blob storage; private connectivity to Workday APIs where available.  
- Stateless web tier behind Azure Front Door or Application Gateway (EU-only) as appropriate.

### Integrations / External Dependencies

| Dependency | Owner | Risk | Mitigation |
|------------|-------|------|------------|
| Azure AD (SAML IdP) | IT / Tom Bauer | Metadata drift | Change window + monitoring |
| Workday APIs | HR + IT | Rate limits / schema change | Contract tests, versioned adapters |
| Azure EU regions | IT | Misconfiguration cross-region | IaC guardrails, policy scans |

### Security & Privacy

- SAML hardening, secure cookies, CSRF protections for web actions.  
- GDPR: lawful basis documentation, RoPA update, subprocessors, DSR process for portal-held data.  
- Encryption in transit (TLS 1.2+) and at rest for storage and DB.

### Performance & Reliability Targets

- NFR-01 as above; error budgets for availability to be set with IT (not specified in RFP).

---

## UX / Content / Accessibility

### UX Principles

- Mobile-first layouts; clear IA for HR vs news vs documents.  
- Plain language for HR tasks; accessibility baseline **WCAG 2.1 Level AA** as stretch goal unless contractually fixed later.

### Design References

- To be produced in design phase; infographics placeholders in High Level Approach.

### Accessibility Requirements

- Keyboard navigable primary flows; semantic headings; focus management on modals.

---

## Risks & Trade-offs

| Risk | Impact | Likelihood | Mitigation | Owner |
|------|--------|------------|------------|-------|
| Workday API scope insufficient for MVP HR UX | High | Med | Early API spike; reduce MVP scope with HR | Eng + HR |
| 12-week timeline vs integration complexity | High | Med | Phase MVP; strict WBS; feature flags | PM |
| RBAC model ambiguity (department edge cases) | Med | Med | RBAC matrix workshop week 1–2 | IT + HR |

### Trade-off Decisions

- **Azure vs multi-cloud:** RFP prefers existing Azure footprint; single-cloud EU deployment accepted.  
- **Rich-text editor:** Choose one vendor component with security review rather than custom editor.

### Rollout Strategy

- Pilot cohort (e.g. one department + IT dogfood) then company-wide; kill switch for news if needed.

### Monitoring & Success Validation

- Synthetic login and home LCP from EU probes; Workday sync lag dashboards; 4xx/5xx budgets.

---

## Appendix

## Stakeholders

| Role | Name / Team | Responsibility |
|------|-------------|----------------|
| HR Director | Sarah Mitchell | HR self-service requirements |
| IT Lead | Tom Bauer | Auth, infra, EU hosting |
| Communications | Communications team | News content standards |
| Primary users | Employees (all staff) | Adoption and feedback |

## Constraints

- **Timeline:** MVP within **12 weeks** of kickoff.  
- **Tech:** No hard stack mandate beyond **Azure-aligned** infrastructure in RFP.  
- **Budget:** Not disclosed in RFP; scope subject to procurement clarification.

### Changelog

| Date | Decision | Owner | Notes |
|------|----------|-------|-------|
| 2026-05-11 | Golden PRD baseline for evals | Workflow | Matches `examples/sample-rfp.md` |

## Assumptions

- Azure AD tenant is already SAML-capable and Acme will provide SP metadata and attribute claims needed for directory and RBAC.  
- Workday exposes APIs or integration patterns sufficient for payslips, leave, entitlements, and directory sync for MVP, or HR accepts interim PDF/link-out where legally required.  
- “All data in EU” includes backups, logs containing PII, and support exports; non-EU support access is disabled or pseudonymized per policy.  
- Department RBAC can be derived from authoritative HR org data with periodic reconciliation.  
- Communications and HR will supply editorial guidelines and retention policy for news posts.  
- MVP does not require offline-first mobile unless Open Question resolves otherwise.

### Open Questions

- Exact **Workday objects and fields** for payslips, leave, and entitlements for MVP vs deferral.  
- **Leave approval workflow** entirely in Workday vs partial in portal.  
- **Document antivirus / DLP** tooling and whether client-side encryption is required.  
- **RTO/RPO** and backup retention for GDPR and business continuity.  
- **WCAG** contractual target (AA vs best effort).  
- Whether **budget cap** introduces mandatory scope cuts before week 4.

### FAQs

- Q: Can we host a non-EU CDN edge for static assets?  
  A: Only if it processes no PII and is contractually acceptable; default is EU-only.

- Q: Who approves cross-department document access?  
  A: Policy to be owned by IT + HR; implemented via admin role with audit trail.
