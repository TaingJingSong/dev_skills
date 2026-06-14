# Data Dictionary Generation Standard

---

## Document Identity

| Field              | Value                                                       |
|--------------------|-------------------------------------------------------------|
| Cover abbreviation | **DATA DICTIONARY**                                         |
| Full title         | STANDARD FORM                                               |
| Document ID format | DD-[NNN]                                                    |
| Related docs       | BRD, PRD, FRD, API Spec, UXUI, Security Guidelines         |
| Footer label       | Data Dictionary (DD)                                        |

---

## Cover Page

```
INNOTECH SOLUTION CO., LTD          [PROJECT TITLE]
[INNOTECH SOLUTION CO., LTD         [PROJECT TITLE]  — repeated as per template]
Make Growth Simple with Innovative Technology   [italic, teal]
DATA DICTIONARY                     [large bold teal]
STANDARD FORM                       [subtitle]

[Cover metadata table — includes DOCUMENT STATUS and Confidentiality rows]
data DICTIONARY | Standard Form
For software systems, integrations, reporting, and data governance projects
Purpose: Use this template to define standard data entities, fields, definitions,
formats, ownership, validation rules, and mapping references consistently.
```

---

## Required Sections (in order)

### 1. Document Control
Standard key-value table. Related Documents: BRD / PRD / FRD / API Spec / UXUI / Security Guidelines.

### 2. Revision History
4-column: Version | Date | Prepared By | Description of Changes

### 3. Purpose of the Document and Scope
Table: Section | Description
Rows: Purpose | In Scope | Out of Scope | Primary Users

### 4. Reference Information
#### 4.1 Related Documents
Table: Document Name | Document Type | Version | Remarks

#### 4.2 Glossary and Abbreviations
Table: Term / Acronym | Meaning | Notes
Include standard DB terms: PK, FK, NN (Not Null), UQ (Unique), IX (Index), etc.

### 5. Data Governance Overview
Table: Area | Details
Areas: Data Owner | Data Steward | Source of Truth | Retention Rule | Confidentiality Level

### 6. Data Entity / Table Inventory
Table: No. | Entity / Table Name | Type | System | Owner | Remarks
Types: Table / View / Report Dataset / API Object / File / Queue

### 7. Standard Field Definition Template
One sub-section per entity (7.1, 7.2, …):

#### 7.x [Entity / Table Name]

**Entity Summary**
Key-value table:
- Entity / Table Name
- Business Description
- Source System
- Primary Key
- Refresh / Update Frequency

**Field Definitions**
Table: No. | Field Name | Alias | Data Type | Length / Size | Nullable | PK / FK | Description | Default Value | Validation Rules | Source / Origin | Remarks

Column widths note: This is a wide table — use landscape page or reduced font (9pt) if needed, or split into two sub-tables (identity + business rules).

### 8. Code Set / Lookup Values
Table: Field Name | Code Value | Label / Description | Status (Active / Deprecated) | Remarks

### 9. Source-to-Target Mapping
Table: Source Field | Source Table | Source System | Target Field | Target Table | Target System | Transformation Rule | Remarks

### 10. Data Quality Rules
Table: DQ ID | Entity / Field | Rule Description | Rule Type | Severity | Action on Failure
Rule Types: Completeness / Uniqueness / Validity / Consistency / Timeliness / Accuracy

### 11. Security Classification
Table: Entity / Field | Classification | Access Level | Masking Rule | Notes
Classifications: Public / Internal / Confidential / Restricted

### 12. Reporting Definitions (if applicable)
Table: Report Name | Dataset / View | Key Metrics / Fields | Refresh Frequency | Owner

### 13. Change Management
Table: Change ID | Date | Entity / Field Affected | Change Description | Approved By | Notes

### 14. Open Issues and Questions
Table: No. | Issue / Question | Owner | Status | Due Date | Notes

### 15. Approval / Sign-Off
Table: Name | Title / Role | Signature | Date (3+ rows)

---

## Table Column Widths

| Table                   | Column Widths (DXA)                                    |
|-------------------------|--------------------------------------------------------|
| Document Control (KV)   | 2800 + 6226 = 9027                                     |
| Entity Inventory        | 500 + 2000 + 1300 + 1500 + 1500 + 2226 = 9027        |
| Field Definitions       | 400+1500+1000+1000+900+700+700+1500+800+1200+700+726 — scale proportionally across 9026 |
| Code Sets               | 2000 + 1500 + 2500 + 1500 + 1526 = 9027              |
| Source-Target Mapping   | 1200+1200+1200+1200+1200+1200+1500+326 = 9027         |
| Approval                | 2500 + 2026 + 2500 + 2000 = 9027                     |

---

## Notes on Wide Tables

The Field Definitions table has 12+ columns. Apply these strategies:
1. Use 9pt Cambria (size: 18 in docx-js) for table body text
2. Abbreviate column headers: "Len" for Length, "Null" for Nullable, "Def" for Default
3. Split into two tables if needed: Table A (identity: name, alias, type, size, nullable, PK/FK) and Table B (business: description, validation, source, remarks)
