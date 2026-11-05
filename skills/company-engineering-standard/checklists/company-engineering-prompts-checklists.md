# Document Routing Guide

> Use this file to identify which document type the user is requesting and which generation
> standard to load next.

---

## Step 1 — Keyword Detection

Scan the user request for these trigger phrases (case-insensitive):

| User Says                                                              | Document Type | Code | Standard File                          |
|------------------------------------------------------------------------|---------------|------|----------------------------------------|
| "BRD", "business requirement", "business requirements document"        | BRD           | BRD  | references/brd-generation-standard.md  |
| "PRD", "product requirement", "product requirements document"          | PRD           | PRD  | references/prd-generation-standard.md  |
| "SRS", "software requirement spec", "software requirements specification" | SRS        | SRS  | references/srs-generation-standard.md  |
| "FRD", "functional requirement", "functional requirements document"    | FRD           | FRD  | references/frd-generation-standard.md  |
| "TRD", "technical requirement", "technical requirements document"      | TRD           | TRD  | references/trd-generation-standard.md  |
| "API spec", "API specification", "interface specification"             | API Spec      | API  | references/api-spec-generation-standard.md |
| "data dictionary", "DTD", "field definitions", "data catalog"          | Data Dictionary | DD | references/data-dictionary-generation-standard.md |
| "UAT", "user acceptance test", "acceptance testing document"           | UAT           | UAT  | references/uat-generation-standard.md  |
| "issue log", "risk log", "IRL", "issue and risk log", "risk register"  | Issue & Risk Log | IRL | references/issue-risk-log-generation-standard.md |

---

## Step 2 — Ambiguity Resolution

If the user request is ambiguous (e.g., "make a requirements document"), ask:

> "Which document type would you like? Options: BRD (business), PRD (product), SRS (full software spec), FRD (functional), or TRD (technical)?"

If the user provides raw content and says "format this as a document", apply:

1. Scan content for section headings to infer type.
2. If unable to infer, default to BRD and ask for confirmation.

---

## Step 3 — Load Corresponding Files

Once document type is confirmed, load in this order:

```
1. references/document-style-guide.md
2. references/docx-generation-rules.md
3. references/<type>-generation-standard.md
4. prompts/generate-<type>.md
5. checklists/pre-generation-checklist.md
```

---

## Step 4 — Input Gathering

Run `checklists/pre-generation-checklist.md` to confirm required inputs are present before generating.

---

## Step 5 — Output Naming Convention

Generated files should follow this naming pattern:

```
[CODE]_[ProjectName]_[YYYY-MM-DD].docx
```

Examples:
- `BRD_CustomerPortal_2025-01-15.docx`
- `SRS_PaymentGateway_2025-03-01.docx`
- `UAT_MobileApp_2025-04-20.docx`
