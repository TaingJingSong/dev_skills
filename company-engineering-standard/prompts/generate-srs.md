# Prompt: Generate Software Requirements Specification (SRS)

## Pre-Conditions
Read: document-style-guide.md, docx-generation-rules.md, srs-generation-standard.md

## Input Variables
```
PROJECT_TITLE, PROJECT_NAME, PREPARED_BY, VERSION, DATE, STATUS, DOCUMENT_ID
OWNER, CONTRIBUTORS, REVIEWED_BY, APPROVED_BY
SYSTEM_OVERVIEW, STAKEHOLDERS (list: Role | Dept | Responsibility | Notes)
ASSUMPTIONS, CONSTRAINTS, DEPENDENCIES
FUNCTIONAL_REQUIREMENTS (list: ID | Module | Description | Priority | Source | Criteria | Remarks)
NFR (list: ID | Category | Requirement | Metric | Priority | Remarks)
INTERFACE_REQUIREMENTS, DATA_REQUIREMENTS, SECURITY_REQUIREMENTS
BUSINESS_RULES, REPORTING_REQUIREMENTS
```

## Cover Page
- Abbreviation: "SRS – [PROJECT_TITLE]" (teal, bold, 28pt)
- Full title: "SOFTWARE REQUIREMENTS SPECIFICATION"
- Cover table includes: DOCUMENT STATUS, Confidentiality, Owner, Contributors

## Body Sections
Follow srs-generation-standard.md §1–18 in order.
Functional requirements use "The system shall…" language throughout.
Traceability matrix in §16 links every FR to a source document and test case.

## Output: `SRS_[ProjectName]_[YYYY-MM-DD].docx`
