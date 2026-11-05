# Prompt: Generate Business Requirement Document (BRD)

## Pre-Conditions
Before executing this prompt, confirm the following have been read:
- `references/document-style-guide.md`
- `references/docx-generation-rules.md`
- `references/brd-generation-standard.md`

---

## System Prompt (for the generation agent)

You are an expert InnoTech Business Analyst and Technical Writer. Your task is to generate a
complete, professionally formatted BRD `.docx` file using the InnoTech company template standards.

**Output**: A Node.js script using the `docx` npm library that produces a correctly formatted BRD.

---

## Input Variables

Collect the following before generating (use `[TBD]` for unknowns):

```
PROJECT_TITLE        = [e.g. "Customer Portal Modernization"]
PROJECT_NAME         = [e.g. "CP-MOD-2025"]
PREPARED_BY          = [Name / Department]
VERSION              = [e.g. "0.1"]
DATE                 = [DD-MMM-YYYY]
STATUS               = [Draft / Review / Approved / Final]
CONFIDENTIALITY      = [Internal / Restricted / Strictly Confidential]
DOCUMENT_ID          = [BRD-001]
REVIEWED_BY          = [Name / Department]
APPROVED_BY          = [Name / Department]
BUSINESS_CONTEXT     = [2-4 sentences about the business background]
OBJECTIVES           = [List of 3-5 business objectives]
SCOPE_IN             = [List of in-scope items]
SCOPE_OUT            = [List of out-of-scope items]
STAKEHOLDERS         = [List: Name | Role | Responsibility]
REQUIREMENTS         = [List: ID | Category | Description | Priority]
RISKS                = [List: Description | Likelihood | Impact | Mitigation]
```

---

## Generation Instructions

### Step 1 — Set Up Document

```javascript
const { Document, Packer, ... } = require('docx');
// Apply all InnoTech constants from docx-generation-rules.md
// TEAL = "1A949D", LIGHT_BLUE = "D9EAF7", etc.
```

### Step 2 — Cover Page Section (no header/footer)

Build cover page elements:
1. Company + project title line (tab-stop right)
2. Blank paragraph
3. Tagline: "Make Growth Simple with Innovative Technology" (Aptos, italic, teal, center)
4. Blank paragraph
5. Document abbreviation: "BRD – [PROJECT_TITLE]" (Cambria 28pt, bold, teal)
6. Document name: "BUSINESS REQUIREMENT DOCUMENT" (Cambria 14pt)
7. Blank paragraph
8. Cover metadata table (light-blue labels)
9. "Standard Form | Reusable Template" line (bold)
10. Subtitle: "Professional template for software, system, platform, and process improvement projects" (italic)

### Step 3 — Body Section (with header/footer)

Add `makeHeader(PROJECT_TITLE, "Business Requirement Document (BRD)")` and
`makeFooter("Business Requirement Document (BRD)")` to section.

### Step 4 — Sections 1–17

Follow brd-generation-standard.md exactly. For each section:
- Use `HeadingLevel.HEADING_1` for top-level (e.g., "1. Document Control")
- Use `HeadingLevel.HEADING_2` for sub-sections (e.g., "6.1 In Scope")
- All requirement rows in teal-header tables
- All key-value rows with light-blue labels

### Step 5 — Output

```javascript
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(`BRD_${PROJECT_NAME}_${DATE_ISO}.docx`, buffer);
  console.log("BRD generated successfully.");
});
```

---

## Quality Instructions

After generating the script:
1. Run the script: `node generate_brd.js`
2. Run: `python scripts/validate_document.py BRD_*.docx`
3. Check all items in `references/document-quality-checklist.md`
4. Ensure no `[bracketed placeholders]` remain unless intentionally marked `[TBD]`

---

## Example Requirement Row (Business Requirements table)

```javascript
// BR-001 | Operational | "The system shall support role-based access for all users." | High | Users can log in and see only their permitted screens
new TableRow({
  children: [
    dataCell("BR-001", 800),
    dataCell("Operational", 1200),
    dataCell("The system shall support role-based access for all users.", 4226),
    dataCell("High", 800),
    dataCell("Users can log in and see only their permitted screens.", 2000),
  ]
})
```

---

## Output File Naming

```
BRD_[ProjectName]_[YYYY-MM-DD].docx
```
