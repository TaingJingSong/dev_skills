# Prompt: Generate Technical Requirement Document (TRD)

## Pre-Conditions
Read: document-style-guide.md, docx-generation-rules.md, trd-generation-standard.md

## Input Variables
```
PROJECT_TITLE, PROJECT_NAME, PREPARED_BY, VERSION, DATE, STATUS, DOCUMENT_ID
REVIEWED_BY, APPROVED_BY
ARCHITECTURE_LAYERS (list: Layer | Description | Technologies)
ENVIRONMENTS (list: Env | Purpose | URL | Owner)
COMPONENTS (list: ID | Module | Description | Dependencies)
DATA_MODEL (list: Entity | Description | PK | Key Attributes)
API_INTEGRATIONS (list: ID | Name | Direction | Protocol | Consumer | Description)
AUTH_MECHANISMS, SECURITY_REQUIREMENTS
NFR (list: ID | Category | Requirement | Target | Priority)
INFRASTRUCTURE, DEPLOYMENT_STRATEGY
MONITORING, TECHNICAL_RISKS
```

## Cover Page
- Abbreviation: "TRD – [PROJECT_TITLE]" (teal, bold, 28pt)
- Full title: "TECHNICAL REQUIREMENT DOCUMENT"

## Body Sections
Follow trd-generation-standard.md §1–18 in order.
Performance thresholds always include numeric values and conditions.

## Output: `TRD_[ProjectName]_[YYYY-MM-DD].docx`
