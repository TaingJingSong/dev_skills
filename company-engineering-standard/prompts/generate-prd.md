# Prompt: Generate Product Requirement Document (PRD)

## Pre-Conditions
Read: document-style-guide.md, docx-generation-rules.md, prd-generation-standard.md

## Input Variables
```
PROJECT_TITLE, PROJECT_NAME, PREPARED_BY, VERSION, DATE, STATUS, DOCUMENT_ID
OWNER, CONTRIBUTORS, REVIEWED_BY, APPROVED_BY
PRODUCT_VISION, BUSINESS_GOALS (list: Goal | Target), PROBLEM_STATEMENT
PERSONAS (list: Persona | Description | Need | Frequency)
USER_STORIES (list: ID | As a | I want | So that | Priority | Criteria)
SCOPE_IN, SCOPE_OUT
FEATURES (list: ID | Feature | Description | Priority)
NFR (list: Category | Requirement | Target)
RISKS (list: Risk | Likelihood | Impact | Mitigation)
RELEASE_PLAN (list: Release | Scope | Target Date | Status)
```

## Cover Page
- Abbreviation: "PRD – [PROJECT_TITLE]" (teal, bold, 28pt)
- Full title: "PRODUCT REQUIREMENTS DOCUMENT"
- Cover table includes: DOCUMENT STATUS and Confidentiality rows

## Body Sections
Follow prd-generation-standard.md §1–21 in order.
Apply teal header rows to all data tables.
Apply light-blue labels to all key-value tables.

## Output: `PRD_[ProjectName]_[YYYY-MM-DD].docx`
