# Prompt: Generate API Specification

## Pre-Conditions
Read: document-style-guide.md, docx-generation-rules.md, api-spec-generation-standard.md

## Input Variables
```
PROJECT_TITLE, API_NAME, PREPARED_BY, VERSION, DATE, STATUS, DOCUMENT_ID
OWNING_SYSTEM, BUSINESS_PURPOSE, INTERFACE_TYPE, DIRECTION, CONSUMERS, ENVIRONMENTS
STANDARDS_AND_CONVENTIONS (base URL, content type, naming convention, versioning)
AUTH_METHOD, AUTH_MODEL, TOKEN_EXPIRY, SECRETS_MANAGEMENT
ENDPOINTS (list: ID | Method | URI | Operation | Description | Priority)
For each ENDPOINT:
  - REQUEST_HEADERS, PATH_PARAMS, QUERY_PARAMS, REQUEST_BODY, SAMPLE_REQUEST
  - RESPONSE_CODES, RESPONSE_BODY, SAMPLE_RESPONSE, ERROR_STRUCTURE
DATA_MAPPING, VALIDATION_RULES, NFR, LOGGING, MONITORING, DEPLOYMENT
```

## Cover Page
- Abbreviation: "api specification" (teal, bold, 28pt, sentence case as per template)
- Full title: "Application Programming Interface Specification"
- Cover table: Prepared By | Version | Date only (3 rows)

## Body Sections
Follow api-spec-generation-standard.md §1–18 in order.
Section 10 repeats once per endpoint.
JSON samples use Courier New 9pt in shaded cell.

## Output: `API_[ProjectName]_[YYYY-MM-DD].docx`
