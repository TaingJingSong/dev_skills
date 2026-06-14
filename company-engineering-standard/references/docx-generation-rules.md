# docx-js Generation Rules for InnoTech Documents

> These rules supplement the public docx SKILL.md with InnoTech-specific constraints.
> **All rules here take precedence over defaults when generating InnoTech documents.**

---

## 1. Setup and Installation

```bash
npm install -g docx
node generate_document.js
```

---

## 2. Standard Imports

```javascript
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, VerticalAlign, PageNumber, PageBreak, LevelFormat,
  TabStopType, TabStopPosition
} = require('docx');
const fs = require('fs');
```

---

## 3. Page Setup (A4 — InnoTech Standard)

```javascript
properties: {
  page: {
    size: { width: 11906, height: 16838 },  // A4
    margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
  }
}
// Content width = 11906 - 2*1440 = 9026 DXA
```

---

## 4. InnoTech Color Constants

```javascript
const TEAL        = "1F7080";   // Teal — table headers
const LIGHT_BLUE  = "D5E8F0";   // Light blue — label cells
const WHITE       = "FFFFFF";   // White — header text
const BLACK       = "000000";   // Black — borders, body text
const GRAY_FOOTER = "595959";   // Footer text color
```

---

## 5. Standard Styles Block

Always include this styles block in every Document constructor:

```javascript
styles: {
  default: {
    document: { run: { font: "Cambria", size: 22 } }  // 11pt
  },
  paragraphStyles: [
    {
      id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal",
      run: { size: 28, bold: true, font: "Cambria", color: BLACK },
      paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 }
    },
    {
      id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal",
      run: { size: 24, bold: true, font: "Cambria", color: BLACK },
      paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 }
    },
    {
      id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal",
      run: { size: 22, bold: true, font: "Cambria", color: BLACK },
      paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 2 }
    }
  ]
}
```

---

## 6. Teal Header Row Helper

```javascript
function tealHeaderRow(labels, colWidths) {
  return new TableRow({
    tableHeader: true,
    children: labels.map((label, i) =>
      new TableCell({
        width: { size: colWidths[i], type: WidthType.DXA },
        shading: { fill: TEAL, type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        borders: fullBorder(BLACK),
        verticalAlign: VerticalAlign.CENTER,
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: label, bold: true, color: WHITE, font: "Cambria", size: 20 })]
        })]
      })
    )
  });
}
```

---

## 7. Light-Blue Label Cell Helper

```javascript
function labelCell(text, width) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: { fill: LIGHT_BLUE, type: ShadingType.CLEAR },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    borders: fullBorder(BLACK),
    children: [new Paragraph({
      children: [new TextRun({ text, bold: true, font: "Cambria", size: 20 })]
    })]
  });
}
```

---

## 8. Full Border Helper

```javascript
function fullBorder(color = BLACK, size = 4) {
  const b = { style: BorderStyle.SINGLE, size, color };
  return { top: b, bottom: b, left: b, right: b };
}
```

---

## 9. Standard Key-Value Table (Document Control)

Two-column table: label (light-blue) | value (white)

```javascript
function kvTable(rows) {
  // rows = [{ label: "Document Title", value: "BRD – Project X" }, ...]
  return new Table({
    width: { size: 9026, type: WidthType.DXA },
    columnWidths: [2800, 6226],
    rows: rows.map(({ label, value }) =>
      new TableRow({ children: [
        labelCell(label, 2800),
        new TableCell({
          width: { size: 6226, type: WidthType.DXA },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          borders: fullBorder(BLACK),
          children: [new Paragraph({
            children: [new TextRun({ text: value, font: "Cambria", size: 20 })]
          })]
        })
      ]})
    )
  });
}
```

---

## 10. Standard Header

```javascript
function makeHeader(projectTitle, docName) {
  return new Header({
    children: [
      new Paragraph({
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: TEAL, space: 1 } },
        tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
        children: [
          new TextRun({ text: "INNOTECH SOLUTION CO., LTD", bold: true, font: "Cambria", size: 18 }),
          new TextRun({ text: "\t" + projectTitle, font: "Cambria", size: 18 }),
        ]
      }),
      new Paragraph({
        tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
        children: [
          new TextRun({ text: docName, font: "Cambria", size: 18, color: GRAY_FOOTER }),
          new TextRun({ text: "\tStrictly Confidential", font: "Cambria", size: 18, color: GRAY_FOOTER })
        ]
      })
    ]
  });
}
```

---

## 11. Standard Footer

```javascript
function makeFooter(docName) {
  return new Footer({
    children: [
      new Paragraph({
        tabStops: [
          { type: TabStopType.CENTER, position: 4513 },
          { type: TabStopType.RIGHT, position: TabStopPosition.MAX }
        ],
        children: [
          new TextRun({ text: docName, font: "Cambria", size: 18, color: GRAY_FOOTER }),
          new TextRun({ text: "\t", font: "Cambria", size: 18 }),
          new TextRun({ children: ["Page ", PageNumber.CURRENT, " of ", PageNumber.TOTAL_PAGES],
            font: "Cambria", size: 18, color: GRAY_FOOTER }),
          new TextRun({ text: "\tStrictly Confidential", font: "Cambria", size: 18, color: GRAY_FOOTER })
        ]
      })
    ]
  });
}
```

---

## 12. Cover Page Structure

The cover page must be in its **own section** with no header/footer (first page different).

```javascript
// Section 1: Cover page (no header/footer)
{
  properties: {
    page: {
      size: { width: 11906, height: 16838 },
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
    }
  },
  children: [
    // Company name + project title line
    // Tagline
    // Document type abbreviation (large teal bold)
    // Full document name
    // Cover metadata table
    // Standard Form badge
  ]
}

// Section 2+: Document body (with header/footer)
{
  properties: { ... },
  headers: { default: makeHeader(projectTitle, docName) },
  footers: { default: makeFooter(docName) },
  children: [ /* all body content */ ]
}
```

---

## 13. Critical Rules Summary

| Rule                                 | Correct                          | Wrong                        |
|--------------------------------------|----------------------------------|------------------------------|
| Page size                            | A4: 11906 × 16838 DXA            | Default (also A4 but confirm)|
| Table width type                     | `WidthType.DXA`                  | `WidthType.PERCENTAGE`       |
| Shading type                         | `ShadingType.CLEAR`              | `ShadingType.SOLID`          |
| Bullet points                        | `LevelFormat.BULLET` + numbering | Unicode `•` character        |
| Line breaks                          | Separate `new Paragraph()`       | `\n` inside TextRun          |
| PageBreak                            | Inside a `new Paragraph()`       | Standalone element           |
| Header/footer two-column layout      | Tab stops                        | Tables inside header/footer  |
| Table borders                        | `fullBorder(BLACK)` on each cell | Omitting border definition   |
| Cell dual widths                     | `columnWidths` + cell `width`    | Only one of them             |
