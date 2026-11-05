# Prompt: Generate Data Dictionary

## Pre-Conditions
Read: document-style-guide.md, docx-generation-rules.md, data-dictionary-generation-standard.md

## Input Variables
```
PROJECT_TITLE, PROJECT_NAME, PREPARED_BY, VERSION, DATE, STATUS, DOCUMENT_ID
REVIEWED_BY, APPROVED_BY
DATA_GOVERNANCE (Data Owner | Data Steward | Source of Truth | Retention | Confidentiality)
ENTITIES (list: No | Name | Type | System | Owner | Remarks)
For each ENTITY:
  - FIELDS (list: No | Field Name | Alias | Data Type | Length | Nullable | PK/FK |
             Description | Default | Validation | Source | Remarks)
CODE_SETS (list: Field | Code | Label | Status)
SOURCE_TARGET_MAPPING (list: Source Field | Source Table | Source System | Target Field | ...)
DATA_QUALITY_RULES, SECURITY_CLASSIFICATION, REPORTING_DEFINITIONS
```

## Cover Page
- Abbreviation: "DATA DICTIONARY" (teal, bold, 28pt, all caps)
- Sub-title: "STANDARD FORM"
- Cover table includes: DOCUMENT STATUS and Confidentiality rows

## Body Sections
Follow data-dictionary-generation-standard.md §1–15 in order.
Section 7 repeats for each entity.
Wide tables (12+ columns) use 9pt font and split if needed.

## Output: `DD_[ProjectName]_[YYYY-MM-DD].docx`
