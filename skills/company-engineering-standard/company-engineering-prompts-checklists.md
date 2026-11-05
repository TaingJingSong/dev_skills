# InnoTech Document Style Guide

> **Source of truth for all visual and typographic decisions.**  
> Every generated document must match this guide exactly.

---

## 1. Brand Identity

| Element        | Value                                         |
|----------------|-----------------------------------------------|
| Company Name   | INNOTECH SOLUTION CO., LTD                    |
| Tagline        | Make Growth Simple with Innovative Technology |
| Confidential   | Strictly Confidential (footer, every page)    |

---

## 2. Color Palette

| Role                     | Hex Code  | docx-js fill value | Usage                                     |
|--------------------------|-----------|--------------------|-------------------------------------------|
| Teal – table header bg   | `#1F7080` | `1F7080`           | All table header rows                     |
| White – header text      | `#FFFFFF` | `FFFFFF`           | Text inside teal header cells             |
| Light blue – label cells | `#D5E8F0` | `D5E8F0`           | Left-column label cells in key-value tables |
| Black – borders          | `#000000` | `000000`           | All table borders                         |
| Dark text                | `#000000` | `000000`           | Body text                                 |
| Cover page accent        | `#1F7080` | `1F7080`           | Cover page horizontal rule / accents      |

---

## 3. Typography

| Style          | Font  | Size | Weight | Color     | Notes                               |
|----------------|-------|------|--------|-----------|-------------------------------------|
| Body           | Cambria | 11pt | Normal | `#000000` | Default for all paragraph text      |
| Heading 1      | Cambria | 14pt | Bold   | `#000000` | Numbered section headings (1. 2. …) |
| Heading 2      | Cambria | 12pt | Bold   | `#000000` | Sub-sections (1.1, 2.1 …)           |
| Heading 3      | Cambria | 11pt | Bold   | `#000000` | Sub-sub-sections                    |
| Table header   | Cambria | 10pt | Bold   | `#FFFFFF` | Inside teal header cells            |
| Table body     | Cambria | 10pt | Normal | `#000000` | Inside regular table cells          |
| Cover title    | Cambria | 20pt | Bold   | `#1F7080` | Document type name on cover         |
| Cover subtitle | Cambria | 14pt | Normal | `#000000` | Full document name on cover         |
| Cover meta     | Cambria | 11pt | Normal | `#000000` | Prepared by / version / date rows   |
| Footer         | Cambria | 9pt  | Normal | `#595959` | Page number + "Strictly Confidential"|

---

## 4. Page Layout

| Setting          | Value                                  |
|------------------|----------------------------------------|
| Page size        | A4 (11906 × 16838 DXA)                 |
| Top margin       | 1440 DXA (1 inch)                      |
| Bottom margin    | 1440 DXA (1 inch)                      |
| Left margin      | 1440 DXA (1 inch)                      |
| Right margin     | 1440 DXA (1 inch)                      |
| Content width    | 9026 DXA (page 11906 − 2 × 1440)      |
| Header distance  | 720 DXA (0.5 inch from top)            |
| Footer distance  | 720 DXA (0.5 inch from bottom)         |

---

## 5. Cover Page Structure

Every document begins with a cover page section containing the following elements in order:

```
[Company Name]                   [PROJECT TITLE]   ← right-aligned tab
[blank line]
[Tagline in teal italic]
[blank line]
[Document Type abbreviation – large, bold, teal]
[Full Document Name – subtitle]
[blank line]
[Cover metadata table]
[blank line]
[Standard Form badge line]
[Confidentiality notice / tagline]
```

### Cover Metadata Table (3-column, no outer border)

| Column      | Width (DXA) | Style                   |
|-------------|-------------|-------------------------|
| Label       | 2200        | Light-blue fill, bold   |
| Colon (`:`) | 300         | No fill, centered       |
| Value       | 6526        | No fill                 |

Rows: `project name`, `Prepared By`, `Version`, `Date`, `DOCUMENT STATUS`, `Confidentiality`

---

## 6. Header (Repeating, Every Page Except Cover)

Two-line header using tab stops:
- Line 1: `[Company Name]` (left) `[PROJECT TITLE]` (right-aligned)
- Line 2: `[Document Name abbreviation + full name]` (left) `Strictly Confidential` (right-aligned)
- Separated from body by a 1pt teal bottom border on the paragraph.

---

## 7. Footer (Repeating, Every Page Except Cover)

Single line using tab stop:
- Left: `[Document Name]`
- Center tab: `Page X of Y`
- Right-aligned: `Strictly Confidential`
- Font: Cambria 9pt, color `#595959`

---

## 8. Tables

### Standard Data Table

```
Header row  → teal fill (#1F7080), white bold text, 10pt Cambria
Body rows   → white fill, black text, 10pt Cambria
All borders → Black (#000000), 1pt single
Cell padding → top 80 DXA, bottom 80 DXA, left 120 DXA, right 120 DXA
```

### Key-Value (Document Control) Table

```
Left column  → light-blue fill (#D5E8F0), bold label, 10pt Cambria
Right column → white fill, value text, 10pt Cambria
Borders      → Black, 1pt single
```

### Critical docx-js Rules for Tables

- Always use `WidthType.DXA` — never `WidthType.PERCENTAGE`
- Always set both `columnWidths` on the Table AND `width` on each TableCell
- Always use `ShadingType.CLEAR` — never `ShadingType.SOLID`
- `columnWidths` must sum exactly to the table's `width.size`
- For full-width tables: `width.size = 9026` (A4 content width)

---

## 9. Section Numbering

- Top-level sections: `1.`, `2.`, `3.` … — use Heading 1
- Sub-sections: `1.1`, `1.2`, `2.1` … — use Heading 2
- Sub-sub-sections: `1.1.1` … — use Heading 3 (plain bold paragraph if needed)
- Guidance text blocks: shown in italics, remove from final deliverable

---

## 10. Document Control Section (All Document Types)

Every document must contain a Section 1 titled **Document Control** with a key-value table:

| Field          | Description                                       |
|----------------|---------------------------------------------------|
| Document Title | Full name with document type – Project Name       |
| Document ID    | Reference code, e.g. BRD-001, PRD-XXX            |
| Version        | e.g. 1.0                                          |
| Prepared By    | Name / Position / Department / Company            |
| Reviewed By    | Name / Position / Department / Company            |
| Approved By    | Name / Position / Department / Company            |
| Date           | DD-MMM-YYYY                                       |
| Status         | Draft / Review / Approved / Final                 |
| Related Documents | Comma-separated list of referenced docs        |

---

## 11. Revision History Section (All Document Types)

Section 2 titled **Revision History** with a 4-column table:

| Column              | Header Text           |
|---------------------|-----------------------|
| Version             | Version               |
| Date                | Date                  |
| Prepared By         | Prepared By           |
| Description         | Description of Changes|

Header row: teal fill, white bold text.

---

## 12. Approval / Sign-Off Section (All Document Types)

Final section of every document:

| Field     | Columns                                    |
|-----------|--------------------------------------------|
| Name      | Full name                                  |
| Title/Role| Title and organizational role              |
| Signature | Blank field for wet or digital signature   |
| Date      | Date of signature                          |

Minimum 3 rows for approvers.
