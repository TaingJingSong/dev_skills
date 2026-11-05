# UAT Generation Standard
## User Acceptance Testing Document

---

## Document Identity

| Field              | Value                                                    |
|--------------------|----------------------------------------------------------|
| Cover abbreviation | **User Acceptance Testing (UAT)**                        |
| Full title         | UAT PERIOD: FROM: … TO: …                               |
| Document ID format | UAT-[NNN]-[YYYY]                                         |
| Related docs       | BRD, PRD, FRD, SRS, API Spec, UXUI, Security Guidelines |
| Footer label       | User Acceptance Testing (UAT)                            |

---

## Cover Page

```
INNOTECH SOLUTION CO., LTD          [PROJECT TITLE]
[INNOTECH SOLUTION CO., LTD         [PROJECT TITLE]  — repeated as per template]
Make Growth Simple with Innovative Technology   [italic, teal]
User Acceptance Testing (uat) [PROJECT TITLE]  [large bold teal, mixed case as per template]
UAT PERIOD: FROM:…… TO: ……          [subtitle]

[Cover metadata table — includes DOCUMENT STATUS and Confidentiality rows]
Standard Form | Reusable Template
(UAT) Standardized Template
```

---

## Required Sections (in order)

### 1. Document Control
Key-value table. Owner: Technical Lead / Product Manager / Business Owner. Contributors row included.

### 2. Revision History (Document Control Table 2)
Extended revision table: Version | Date | Prepared By | Reviewed By | Approved By | Status

### 3. Purpose
Use this template to plan, execute, track, and sign off business user acceptance testing before production go-live.

### 4. Project Overview
Key-value table:
- Project Background
- UAT Objective
- In Scope
- Out of Scope

### 5. Stakeholders and Roles
Table: Name | Role | Responsibility | Contact / Remark
Roles: Business Owner, PM, QA Lead, End User, Technical Lead

### 6. System Overview
Concise description of the system: major modules, primary users, external systems, deployment context, operating model.

### 7. UAT Schedule
Table: Phase | Activity | Start Date | End Date | Owner | Remarks
Phases: Preparation | Environment Setup | Test Execution | Defect Retesting | Sign-Off

### 8. UAT Entry Criteria
Bullet list:
- Functional development is completed for agreed scope
- Test environment is available and stable
- Master data / sample data is prepared
- Training or walkthrough has been provided
- FRD / SRS / process flows are approved and baseline-controlled
- Defects from prior rounds are resolved or accepted for retest

### 9. UAT Exit Criteria
Bullet list:
- All critical and high-priority test cases are executed
- No open critical defects remain unresolved
- Medium / low defects are documented with agreed action plan
- Stakeholder sign-off is obtained
- UAT report is reviewed and accepted

### 10. Test Environment Details
Table: Item | Details
Items: Environment URL | Database | Test User Accounts | Access Method | Reset / Refresh Procedure

### 11. Test Data Requirements
Table: Module / Feature | Test Data Required | Data Source | Prepared By | Status

### 12. UAT Test Case Register
Table: Test Case ID | Feature / Module | Test Scenario | Test Steps | Expected Result | Actual Result | Status | Tested By | Date | Remarks
- IDs: UAT-[MODULE]-001, UAT-[MODULE]-002 …
- Status values: Pass / Fail / Blocked / Not Tested / Deferred

### 13. Defect / Issue Log
Table: Defect ID | Test Case ID | Defect Description | Severity | Priority | Status | Reported By | Date Reported | Assigned To | Resolution | Closed Date
- Defect IDs: DEF-001, DEF-002 …
- Severity: Critical / High / Medium / Low
- Status: Open / In Progress / Fixed / Retest / Closed / Deferred

### 14. UAT Test Execution Summary
Table: Module | Total TCs | Passed | Failed | Blocked | Not Tested | Pass Rate %

### 15. Defect Summary
Table: Severity | Count | Open | Closed | Deferred

### 16. Outstanding Items and Action Plan
Table: No. | Item Description | Owner | Due Date | Status | Notes

### 17. UAT Sign-Off Declaration
Narrative statement confirming that UAT has been completed and the system is / is not ready for production.

Include go-live recommendation: Go / No-Go / Go with Conditions

### 18. Approval / Sign-Off
Table: Name | Title / Role | Signature | Date (minimum 4 rows: business owner, PM, QA lead, technical lead)

---

## Table Column Widths

| Table                   | Column Widths (DXA)                                   |
|-------------------------|-------------------------------------------------------|
| Document Control (KV)   | 2800 + 6226 = 9027                                    |
| Revision History        | 900 + 1500 + 1500 + 1500 + 1500 + 1626 = 9027       |
| Test Case Register      | 1000+1200+2000+1500+1500+1500+800+1000+900+626 = 12026 → use 9pt, scale |
| Defect Log              | 800+900+2000+900+800+900+900+900+900+1200+1026 → split or scale |
| Execution Summary       | 1500+1200+900+800+800+900+2926 = 9027 (approx)       |
| Approval                | 2500 + 2026 + 2500 + 2000 = 9027                    |

Note: Test Case Register and Defect Log are wide tables. Use 9pt font (size: 18) and abbreviate headers. Consider landscape orientation for these sections if needed.
