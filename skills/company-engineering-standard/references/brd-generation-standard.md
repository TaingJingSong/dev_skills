# BRD Generation Standard
## Business Requirement Document

---

## Document Identity

| Field             | Value                                                        |
|-------------------|--------------------------------------------------------------|
| Cover abbreviation | **BRD**                                                     |
| Full title        | BUSINESS REQUIREMENT DOCUMENT                                |
| Document ID format | BRD-[NNN]                                                   |
| Related docs      | FRD, PRD, SRS, TRD                                          |
| Footer label      | Business Requirement Document (BRD)                         |

---

## Cover Page

```
INNOTECH SOLUTION CO., LTD          [PROJECT TITLE]
Make Growth Simple with Innovative Technology   [italic, teal]
BRD – [PROJECT TITLE]               [large bold teal]
BUSINESS REQUIREMENT DOCUMENT       [subtitle]

[Cover metadata table]
Standard Form | Reusable Template
Professional template for software, system, platform, and process improvement projects
```

---

## Required Sections (in order)

### 1. Document Control
Key-value table. See document-style-guide.md §10.

### 2. Revision History
4-column table: Version | Date | Prepared By | Description of Changes

### 3. Purpose of the Document
Narrative paragraph. State why this BRD exists and what decision or delivery it supports.

### 4. Background / Business Context
Narrative covering:
- Current situation or operating model
- Existing pain points, inefficiencies, or risks
- Business opportunity or reason for change
- Expected business value or strategic benefit

### 5. Objectives
Numbered table (No. | Objective) listing 3–6 measurable business outcomes.

### 6. Scope
#### 6.1 In Scope
Bullet list of included items.
#### 6.2 Out of Scope
Bullet list of explicitly excluded items.

### 7. Stakeholders
Table: Stakeholder Name | Role / Department | Responsibility

### 8. Business Problem Statement
One concise paragraph describing the core business problem.

### 9. Proposed Solution Overview
Narrative describing the high-level proposed approach (not technical design).

### 10. Business Requirements
Table: Req. ID | Category | Business Requirement Description | Priority | Acceptance Criteria
- IDs format: BR-001, BR-002 …
- Priority values: High / Medium / Low / Must Have / Should Have / Nice to Have

### 11. Assumptions
Bullet list.

### 12. Constraints and Dependencies
#### 12.1 Constraints
#### 12.2 Dependencies

### 13. Risks and Issues (High-Level)
Table: No. | Risk / Issue Description | Likelihood | Impact | Mitigation / Note

### 14. Success Criteria / Acceptance Criteria
Table: No. | Criteria | Measurement / KPI

### 15. Reference Documents
Table: Document Name | Type | Version | Remarks

### 16. Glossary and Abbreviations
Table: Term / Acronym | Meaning | Notes

### 17. Approval / Sign-Off
Table: Name | Title / Role | Signature | Date (3+ rows)

---

## Table Column Widths (A4 content width = 9027 DXA)

| Table                  | Column Widths (DXA)             |
|------------------------|---------------------------------|
| Document Control (KV)  | 2800 + 6226 = 9027              |
| Revision History       | 900 + 1500 + 2000 + 4626 = 9027 |
| Stakeholders           | 2500 + 2500 + 4026 = 9027      |
| Business Requirements  | 800 + 1200 + 4226 + 800 + 2000 = 9027 |
| Risk Table             | 400 + 2826 + 1200 + 1200 + 3400 = 9027 |
| Approval               | 2500 + 2026 + 2500 + 2000 = 9027 |

---

## Language and Tone

- Write in professional business-analysis language
- Use "The system shall…" for mandatory requirements
- Use "It is assumed that…" for assumptions
- Avoid technical jargon (save for TRD/SRS)
- All placeholder text removed before delivery
