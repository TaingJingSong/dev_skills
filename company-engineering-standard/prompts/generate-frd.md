# Prompt: Generate Functional Requirement Document (FRD)

## Pre-Conditions
Read: document-style-guide.md, docx-generation-rules.md, frd-generation-standard.md

## Input Variables
```
PROJECT_TITLE, PROJECT_NAME, PREPARED_BY, VERSION, DATE, STATUS, DOCUMENT_ID
REVIEWED_BY, APPROVED_BY
MODULES (list of module names with descriptions)
For each MODULE:
  - USER_ROLES (list: Role | Access Level | Permissions)
  - REQUIREMENTS (list: ID | Description | Priority | Trigger | Behavior | Remarks)
  - BUSINESS_RULES (list: ID | Rule | Applicable To)
  - VALIDATION_RULES (list: Field | Rule | Error Message)
  - WORKFLOW (numbered steps)
  - NOTIFICATIONS (list: Trigger | Type | Recipient | Content)
INTEGRATION_REQUIREMENTS, REPORTING_REQUIREMENTS
```

## Cover Page
- Abbreviation: "FRD – [PROJECT_TITLE]" (teal, bold, 28pt)
- Full title: "FUNCTIONAL REQUIREMENT DOCUMENT"
- Cover table includes: DOCUMENT STATUS and Confidentiality rows

## Body Sections
Follow frd-generation-standard.md §1–15 in order.
Each module gets its own numbered section (8.1, 8.2, …) with all sub-sections.

## Output: `FRD_[ProjectName]_[YYYY-MM-DD].docx`
