---
name: company-engineering-standard
description: Create or review InnoTech BRD, PRD, SRS, FRD, TRD, API specs, data dictionaries, UAT and issue/risk logs using company standards. DOCX requires a generator.
---

## Cross-Agent Safety Contract

These instructions are subordinate to the user's explicit scope, repository policy, and higher-priority agent instructions. Before any file write, inspect the actual repository conventions and applicable `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`. Existing architecture, core logic, public contracts, schemas, security boundaries, dependencies, and directory structure are protected by default. Do not move, rename, replace, or refactor them as a side effect. If the requested task requires a protected change, **stop at that boundary**, explain the blocker and safer alternatives, and request separate explicit approval plus updated scope/policy before continuing. Never silently widen scope. Preserve unrelated work, do not run destructive commands or commits without authorization, and report tests not run. See `../../POLICY.md` when using this bundled distribution; in copied installations, follow the local repository instructions instead.

# Company Document Generation Skill

## Purpose

This skill enables an AI agent to produce `.docx` documents that are consistent with the documented InnoTech Solution Co., Ltd. house style; exact visual identity requires actual approved templates, which are not bundled. Every generated document must
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
[4] Write a Node.js generator from the requested content and relevant standards; confirm the template if exact fidelity is required
    │
    ▼
[5] Run scripts/generate_docx.py --script /path/to/generated.js → build .docx (the Python wrapper does not author JS)
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
skills/company-engineering-standard/
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

## Generation Preconditions and Limitations

- The included Markdown references are standards, **not approved DOCX template binaries**; request the exact template when pixel-level matching is mandatory.
- `scripts/generate_docx.py` is an executor for a supplied JS generator (`--script`) and a validator, **not** an automatic prompt-to-document generator.
- Install `docx` locally in the generated JS project (`npm install docx`) if that JS imports it; do not assume globally installed npm packages are resolvable.
- Run the validation script and disclose warnings/failures. Never claim a document is compliant without actually validating it.
- Google Docs retrieval is an optional authenticated operation; never use or package stored OAuth secrets.
