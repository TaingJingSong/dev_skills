# Prompt: Generate Issue & Risk Log (IRL)

## Pre-Conditions
Read: document-style-guide.md, docx-generation-rules.md, issue-risk-log-generation-standard.md

## Input Variables
```
PROJECT_TITLE, PROJECT_NAME, PRODUCT_NAME, PREPARED_BY, VERSION, DATE, STATUS
DOCUMENT_ID, CUSTOMER, REPORTING_PERIOD, PROJECT_MANAGER, OWNER
ISSUES (list: ID | Date | Summary | Impact | Priority | Owner | Due Date | Status | Action | Closed)
RISKS (list: ID | Statement | Category | Prob | Impact | Score | Mitigation | Contingency | Owner | Status | Target)
ACTIONS (list: No | Ref ID | Action | Owner | Target Date | Progress% | Remarks)
ESCALATION_RECORDS (list: Item | Frequency | Participants | Notes)
```

## Cover Page
- Abbreviation: "issue AND RISK log (IRL)   [product]" (teal, bold, 28pt, mixed case as per template)
- Sub-title: "PROJECT:………………….………"
- Additional header info table (4-column): Project Name | Prepared By | Customer | Reporting Period | Version | Status | PM | Owner
- Cover table includes: DOCUMENT STATUS and Confidentiality rows

## Body Sections
Follow issue-risk-log-generation-standard.md §1–9 in order.
Issue Log and Risk Register are wide tables — use 9pt font.
Summary totals tables (§3, §5) have no header row; show counts directly.

## Output: `IRL_[ProjectName]_[YYYY-MM-DD].docx`
