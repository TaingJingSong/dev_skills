---
name: company-engineering-standard
description: >
  Generate professional InnoTech-branded .docx documents from company-approved templates.
  Use when the user asks to create a BRD, PRD, SRS, FRD, TRD, API Specification,
  Data Dictionary, UAT document, or Issue & Risk Log in the company standard format.
  This skill enforces InnoTech style: teal headers, light-blue label cells, black borders,
  cover page, document control, revision history, and approval / sign-off sections.
---

# Company Document Generation Skill

## Purpose

This skill enables an AI agent to produce `.docx` documents that are visually and structurally
identical to InnoTech Solution Co., Ltd.'s standardized templates. Every generated document must
look as though it was created by an InnoTech business analyst using the approved template library.

---

## Supported Document Types

| Code | Document Type | Standard File |
|------|---------------|---------------|
| BRD  | Business Requirement Document      | references/brd-generation-standard.md |
| PRD  | Product Requirement Document       | references/prd-generation-standard.md |
| SRS  | Software Requirement Specification | references/srs-generation-standard.md |
| FRD  | Functional Requirement Document    | references/frd-generation-standard.md |
| TRD  | Technical Requirement Document     | references/trd-generation-standard.md |
| API  | API Specification                  | references/api-spec-generation-standard.md |
| DD   | Data Dictionary                    | references/data-dictionary-generation-standard.md |
| UAT  | User Acceptance Testing Document   | references/uat-generation-standard.md |
| IRL  | Issue & Risk Log                   | references/issue-risk-log-generation-standard.md |

---

## Mandatory Reading Order

Before generating **any** document, the agent MUST read these files in order:

1. `references/document-style-guide.md`          — Colors, fonts, borders, branding rules
2. `references/docx-generation-rules.md`          — docx-js coding constraints and patterns
3. `references/document-routing.md`               — How to identify which doc type to generate
4. `references/document-quality-checklist.md`     — Final quality gate
5. The relevant `references/<type>-generation-standard.md` — Section structure for the target doc
6. The relevant `prompts/generate-<type>.md`       — Prompt instructions for that document type
7. `checklists/pre-generation-checklist.md`        — Confirm all inputs are present

---

## Workflow

```
User request
    │
    ▼
[1] Read document-routing.md → identify doc type
    │
    ▼
[2] Run pre-generation-checklist.md → gather missing inputs
    │
    ▼
[3] Read style guide + docx rules + doc-type standard
    │
    ▼
[4] Execute generate-<type>.md prompt → produce JS script
    │
    ▼
[5] Run scripts/generate_docx.py → build .docx
    │
    ▼
[6] Run scripts/validate_document.py → quality check
    │
    ▼
[7] Run checklists/final-review-checklist.md → confirm output
    │
    ▼
[8] Deliver .docx to user
```

---

## Quick Reference: InnoTech Style Constants

| Element                  | Value / Rule                                      |
|--------------------------|---------------------------------------------------|
| Company name             | INNOTECH SOLUTION CO., LTD                        |
| Tagline                  | Make Growth Simple with Innovative Technology     |
| Teal header fill         | `#1A949D` (hex) / `1A949D` (docx-js)              |
| Light-blue label fill    | `#D9EAF7` (hex) / `D9EAF7` (docx-js)             |
| Header text color        | White `#FFFFFF`                                   |
| Body font                | Cambria, 11pt                                       |
| Heading 1                | Cambria Bold, 14pt                                  |
| Heading 2                | Cambria Bold, 12pt                                  |
| Table border color       | Black `#000000`                                   |
| Footer text              | `Strictly Confidential`                           |
| Page size                | A4 (11907 × 16840 DXA)                            |
| Margins                  | 1 inch all sides (1440 DXA)                       |
| Confidentiality default  | Strictly Confidential                             |

---

## File Map

```
skills/company-document-generation/
├── SKILL.md                              ← YOU ARE HERE
├── references/
│   ├── document-style-guide.md           ← Colors, fonts, branding
│   ├── document-routing.md               ← Doc-type detection logic
│   ├── docx-generation-rules.md          ← docx-js coding rules
│   ├── document-quality-checklist.md     ← Quality gate criteria
│   ├── brd-generation-standard.md        ← BRD section structure
│   ├── prd-generation-standard.md        ← PRD section structure
│   ├── srs-generation-standard.md        ← SRS section structure
│   ├── frd-generation-standard.md        ← FRD section structure
│   ├── trd-generation-standard.md        ← TRD section structure
│   ├── api-spec-generation-standard.md   ← API Spec section structure
│   ├── data-dictionary-generation-standard.md
│   ├── uat-generation-standard.md        ← UAT section structure
│   └── issue-risk-log-generation-standard.md
├── prompts/
│   ├── generate-brd.md
│   ├── generate-prd.md
│   ├── generate-srs.md
│   ├── generate-frd.md
│   ├── generate-trd.md
│   ├── generate-api-spec.md
│   ├── generate-data-dictionary.md
│   ├── generate-uat.md
│   ├── generate-issue-risk-log.md
│   └── generate-document-from-template.md
├── checklists/
│   ├── pre-generation-checklist.md
│   ├── style-compliance-checklist.md
│   ├── content-completeness-checklist.md
│   ├── docx-formatting-checklist.md
│   └── final-review-checklist.md
└── scripts/
    ├── README.md
    ├── generate_docx.py
    ├── template_loader.py
    ├── style_apply.py
    └── validate_document.py
```
