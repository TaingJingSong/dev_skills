# DOCX Formatting Checklist

> Technical checks for the docx-js output file.

## File Validity
- [ ] File opens in Microsoft Word without errors
- [ ] File opens in LibreOffice without errors
- [ ] `validate_document.py` returns 0 errors

## Section Structure
- [ ] Cover page is Section 1 (no header/footer)
- [ ] Document body is Section 2 (with header/footer)
- [ ] Wide-table pages use landscape section if applicable
- [ ] Page breaks between major sections are clean

## Heading Hierarchy
- [ ] All Heading 1 paragraphs use `HeadingLevel.HEADING_1`
- [ ] All Heading 2 paragraphs use `HeadingLevel.HEADING_2`
- [ ] No manual bold+size used in place of heading levels
- [ ] `outlineLevel` is set on all heading styles in the styles block

## Lists
- [ ] No unicode bullet characters used directly in TextRun
- [ ] All bullets use `LevelFormat.BULLET` numbering config
- [ ] All numbered lists use `LevelFormat.DECIMAL`

## Tables
- [ ] No table inside header or footer (use tab stops instead)
- [ ] No empty tables (all tables have at least 1 data row or placeholder row)
- [ ] `columnWidths` array sums equal table `width.size` for every table

## Special Content
- [ ] Page breaks use `new Paragraph({ children: [new PageBreak()] })`
- [ ] No `\n` characters inside TextRun
- [ ] All hyperlinks use `ExternalHyperlink` or `InternalHyperlink`

## Header and Footer
- [ ] Header uses tab stop for right-aligned project title (not a table)
- [ ] Footer uses tab stops for three-column layout
- [ ] `PageNumber.CURRENT` and `PageNumber.TOTAL_PAGES` used
