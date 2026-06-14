# Scripts — Company Document Generation

These Python helper scripts support the InnoTech document generation workflow.

## Prerequisites

```bash
pip install python-docx --break-system-packages
npm install -g docx
```

## Script Overview

| Script                  | Purpose                                                           |
|-------------------------|-------------------------------------------------------------------|
| `generate_docx.py`      | Orchestrator: runs the Node.js generation script and validates output |
| `template_loader.py`    | Loads document standards and populates input variable dictionaries |
| `style_apply.py`        | Post-processing: verifies and patches style constants in generated docx |
| `validate_document.py`  | Validates a .docx file for InnoTech compliance                    |

## Usage

### Generate a document

```bash
python scripts/generate_docx.py \
  --type BRD \
  --project "Customer Portal" \
  --output ./output/
```

### Validate an existing document

```bash
python scripts/validate_document.py path/to/document.docx
```

### Load template standard

```python
from template_loader import TemplateLoader
loader = TemplateLoader("BRD")
inputs = loader.prompt_for_inputs()
loader.export_js_vars(inputs, "vars.js")
```

## Environment

All scripts run in Python 3.8+. No external network access required.
