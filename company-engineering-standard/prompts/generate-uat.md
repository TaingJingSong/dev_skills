# Prompt: Generate UAT Document

## Pre-Conditions
Read: document-style-guide.md, docx-generation-rules.md, uat-generation-standard.md

## Input Variables
```
PROJECT_TITLE, PROJECT_NAME, PREPARED_BY, VERSION, DATE, STATUS, DOCUMENT_ID
UAT_PERIOD_FROM, UAT_PERIOD_TO, OWNER, CONTRIBUTORS
REVIEWED_BY, APPROVED_BY
PROJECT_BACKGROUND, UAT_OBJECTIVE, SCOPE_IN, SCOPE_OUT
STAKEHOLDERS (list: Name | Role | Responsibility | Contact)
SYSTEM_OVERVIEW, UAT_SCHEDULE (list: Phase | Activity | Start | End | Owner)
TEST_ENVIRONMENT (URL, DB, accounts, access method)
TEST_CASES (list: ID | Feature | Scenario | Steps | Expected | Actual | Status | Tester | Date)
DEFECTS (list: ID | Test Case ID | Description | Severity | Priority | Status | ...)
MODULES (for execution summary table)
```

## Cover Page
- Abbreviation: "User Acceptance Testing (uat) [PROJECT_TITLE]" (teal, bold, 28pt, mixed case as per template)
- Sub-title: "UAT PERIOD: FROM:[date] TO: [date]"
- Cover table includes: DOCUMENT STATUS and Confidentiality rows

## Body Sections
Follow uat-generation-standard.md §1–18 in order.
Test Case Register and Defect Log use 9pt font.
Go/No-Go recommendation clearly stated in §17.

## Output: `UAT_[ProjectName]_[YYYY-MM-DD].docx`
