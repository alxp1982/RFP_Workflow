# Sample RFP Input

Use this file to test the workflow:
`#file:examples/sample-rfp.md`

---

## Client: Acme Corp
## Project: Internal Employee Portal

### Overview
Acme Corp requires an internal employee portal to replace the existing intranet.
The portal should provide single sign-on via the company's existing Azure AD
tenant, a self-service HR section, a company news feed, and a document
repository with role-based access control.

### Requirements

1. Authentication via Azure AD SSO (SAML 2.0).
2. Employee directory with search and profile pages.
3. HR self-service: view payslips, submit leave requests, view entitlements.
4. Company news feed with rich-text posts, authored by HR and Communications.
5. Document repository with folders, upload/download, and RBAC by department.
6. Mobile-responsive design (iOS Safari and Android Chrome).
7. The portal must load within 3 seconds on a 10 Mbps connection.
8. All data must remain within the EU (GDPR compliance).
9. Integration with existing Workday instance for employee data sync.
10. Admin panel for user and content management.

### Constraints
- Timeline: MVP in 12 weeks.
- Tech stack: no hard preference, but existing infrastructure is Azure.
- Budget: not disclosed.

### Stakeholders
- Sarah Mitchell (HR Director) - owns HR self-service requirements.
- Tom Bauer (IT Lead) - owns authentication and infrastructure.
- Communications team - owns news feed content.
- Employees (all staff) - primary end users.
