# Document Quality Checklist

> Run this checklist after generation and before delivery. Every item must pass (✅).

---

## Brand & Identity

- [ ] Company name is `INNOTECH SOLUTION CO., LTD` (all caps, correct spelling)
- [ ] Tagline `Make Growth Simple with Innovative Technology` appears on cover page
- [ ] Document type abbreviation is bold, large, teal on cover
- [ ] `Strictly Confidential` appears in every page footer

## Cover Page

- [ ] Cover page exists as the first page
- [ ] Cover metadata table has all 6 rows: project name, prepared by, version, date, status, confidentiality
- [ ] Cover metadata table uses light-blue label cells
- [ ] `[PROJECT TITLE]` placeholder is replaced with actual project title
- [ ] All `[bracketed placeholders]` are replaced or marked `TBD` if unknown

## Header & Footer

- [ ] Header shows company name (left) and project title (right) on line 1
- [ ] Header shows document name (left) and `Strictly Confidential` (right) on line 2
- [ ] Header has a teal bottom border
- [ ] Footer shows document name, page numbers, and `Strictly Confidential`
- [ ] Cover page does NOT have the repeating header/footer

## Document Control (Section 1)

- [ ] Section 1 is titled `Document Control`
- [ ] Key-value table has all required fields (title, ID, version, prepared by, reviewed by, approved by, date, status)
- [ ] Label cells are light-blue filled, bold
- [ ] Table borders are black, 1pt single

## Revision History (Section 2)

- [ ] Section 2 is titled `Revision History`
- [ ] Table has 4 columns: Version, Date, Prepared By, Description of Changes
- [ ] Header row is teal with white bold text
- [ ] At least one row of data (or placeholder rows)

## Section Structure

- [ ] All required sections for the document type are present (per generation standard)
- [ ] Sections are numbered using the correct scheme (1., 1.1, 1.1.1)
- [ ] Heading levels match section depth (H1 for top-level, H2 for sub, H3 for sub-sub)
- [ ] No guidance/how-to text remains in the final document (remove from output)

## Tables

- [ ] All table headers use teal fill (`1F7080`) with white bold text
- [ ] All table borders are black
- [ ] No table uses `WidthType.PERCENTAGE`
- [ ] All cells have defined padding (top/bottom 80, left/right 120 DXA)
- [ ] `columnWidths` array sums equal the table `width.size`

## Approval / Sign-Off

- [ ] Approval section is the last section of the document
- [ ] Table has columns: Name, Title/Role, Signature, Date
- [ ] Minimum 3 approver rows present

## File Output

- [ ] File is a valid `.docx` (opens without error in Word / LibreOffice)
- [ ] File name follows convention: `[CODE]_[ProjectName]_[YYYY-MM-DD].docx`
- [ ] No validation errors from `validate_document.py`
