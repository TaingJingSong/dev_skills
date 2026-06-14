#!/usr/bin/env python3
"""
validate_document.py — InnoTech Document Compliance Validator

Performs a comprehensive compliance check on a generated .docx file.
Validates structure, branding, style constants, required sections,
and file integrity. Outputs a detailed pass/fail report.

Exit codes:
    0 — All checks passed (or only warnings)
    1 — One or more CRITICAL checks failed
    2 — File not found or not a valid docx

Usage:
    python validate_document.py document.docx [--strict] [--json]
"""

import argparse
import json
import re
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

try:
    from docx import Document as DocxDocument
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False


# ── Constants ─────────────────────────────────────────────────────────────────

TEAL_COLOR         = "1A949D"
LIGHT_BLUE_COLOR   = "D9EAF7"
WHITE_COLOR        = "FFFFFF"
BLACK_COLOR        = "000000"
A4_WIDTH_DXA       = "11907"
A4_HEIGHT_DXA      = "16840"
COMPANY_NAME       = "INNOTECH SOLUTION CO., LTD"
TAGLINE            = "Make Growth Simple with Innovative Technology"
STRICTLY_CONF      = "Strictly Confidential"
REQUIRED_FONT      = "Cambria"

# Required section keywords mapped by document type (detected from filename prefix)
SECTION_KEYWORDS: Dict[str, List[str]] = {
    "BRD": ["Document Control", "Revision History", "Purpose", "Scope",
            "Stakeholder", "Business Requirement", "Approval"],
    "PRD": ["Document Control", "Revision History", "Purpose", "Product Vision",
            "Scope", "User Stor", "Approval"],
    "SRS": ["Document Control", "Revision History", "Purpose", "Scope",
            "Stakeholder", "Functional Requirement", "Non-Functional", "Approval"],
    "FRD": ["Document Control", "Revision History", "Purpose", "Scope",
            "Functional Requirement", "Sign-Off"],
    "TRD": ["Document Control", "Revision History", "Purpose", "Architecture",
            "Environment", "Performance", "Approval"],
    "API": ["Document Control", "Revision History", "Purpose",
            "Endpoint", "Authentication", "Approval"],
    "DD":  ["Document Control", "Revision History", "Purpose", "Entity",
            "Data Quality", "Approval"],
    "UAT": ["Document Control", "Purpose", "Entry Criteria",
            "Exit Criteria", "Test Case", "Sign-Off"],   # UAT uses "UAT Sign-Off"
    "IRL": ["Instructions", "Priority", "Issue Log", "Risk",
            "Action", "Escalation", "Approval", "Sign-Off"],
}


# ── Data Classes ─────────────────────────────────────────────────────────────

@dataclass
class CheckResult:
    name: str
    passed: bool
    severity: str   # CRITICAL / WARNING / INFO
    message: str
    detail: Optional[str] = None


@dataclass
class ValidationReport:
    docx_path: str
    doc_type: str
    results: List[CheckResult] = field(default_factory=list)

    def add(self, name: str, passed: bool, severity: str, message: str, detail: str = None):
        self.results.append(CheckResult(name, passed, severity, message, detail))

    @property
    def critical_failures(self) -> List[CheckResult]:
        return [r for r in self.results if not r.passed and r.severity == "CRITICAL"]

    @property
    def warnings(self) -> List[CheckResult]:
        return [r for r in self.results if not r.passed and r.severity == "WARNING"]

    @property
    def passed_checks(self) -> List[CheckResult]:
        return [r for r in self.results if r.passed]

    def overall_passed(self) -> bool:
        return len(self.critical_failures) == 0

    def print_report(self, verbose: bool = True):
        total = len(self.results)
        passed = len(self.passed_checks)
        crit = len(self.critical_failures)
        warn = len(self.warnings)

        print(f"\n{'═'*65}")
        print(f"  InnoTech Document Validation Report")
        print(f"  File    : {self.docx_path}")
        print(f"  Type    : {self.doc_type}")
        print(f"  Result  : {'✅ PASSED' if self.overall_passed() else '❌ FAILED'}")
        print(f"  Checks  : {passed}/{total} passed | {crit} critical | {warn} warnings")
        print(f"{'═'*65}")

        if self.critical_failures:
            print(f"\n  ❌ CRITICAL FAILURES ({crit})")
            for r in self.critical_failures:
                print(f"    [{r.name}] {r.message}")
                if r.detail:
                    print(f"      → {r.detail}")

        if self.warnings:
            print(f"\n  ⚠️  WARNINGS ({warn})")
            for r in self.warnings:
                print(f"    [{r.name}] {r.message}")
                if r.detail:
                    print(f"      → {r.detail}")

        if verbose and self.passed_checks:
            print(f"\n  ✅ PASSED CHECKS ({passed})")
            for r in self.passed_checks:
                print(f"    [{r.name}] {r.message}")

        print(f"\n{'═'*65}\n")

    def to_dict(self) -> dict:
        return {
            "docx_path": self.docx_path,
            "doc_type": self.doc_type,
            "overall_passed": self.overall_passed(),
            "summary": {
                "total": len(self.results),
                "passed": len(self.passed_checks),
                "critical_failures": len(self.critical_failures),
                "warnings": len(self.warnings),
            },
            "checks": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "severity": r.severity,
                    "message": r.message,
                    "detail": r.detail,
                }
                for r in self.results
            ],
        }


# ── XML Readers ───────────────────────────────────────────────────────────────

def read_xml_from_docx(docx_path: str) -> Dict[str, str]:
    """Extract XML files from the docx ZIP archive."""
    files: Dict[str, str] = {}
    try:
        with zipfile.ZipFile(docx_path, "r") as z:
            for name in z.namelist():
                if name.endswith(".xml") or name.endswith(".rels"):
                    files[name] = z.read(name).decode("utf-8", errors="replace")
    except zipfile.BadZipFile:
        return {}
    return files


def extract_text_from_docx(docx_path: str) -> str:
    """Extract all text from a docx using python-docx if available, else raw XML."""
    if DOCX_AVAILABLE:
        try:
            doc = DocxDocument(docx_path)
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception:
            pass
    # Fallback: strip XML tags
    xml_files = read_xml_from_docx(docx_path)
    doc_xml = xml_files.get("word/document.xml", "")
    return re.sub(r"<[^>]+>", " ", doc_xml)


def detect_doc_type(docx_path: str) -> str:
    """Infer document type from filename prefix."""
    name = Path(docx_path).stem.upper()
    for code in ["BRD", "PRD", "SRS", "FRD", "TRD", "API", "DD", "UAT", "IRL"]:
        if name.startswith(code):
            return code
    return "UNKNOWN"


# ── Individual Checks ─────────────────────────────────────────────────────────

def check_file_valid(docx_path: str, report: ValidationReport) -> bool:
    """Check the file is a valid docx (ZIP with word/document.xml)."""
    try:
        with zipfile.ZipFile(docx_path, "r") as z:
            names = z.namelist()
        if "word/document.xml" in names:
            report.add("file_valid", True, "CRITICAL", "File is a valid .docx archive")
            return True
        else:
            report.add("file_valid", False, "CRITICAL",
                       "word/document.xml missing — file may be corrupted")
            return False
    except zipfile.BadZipFile:
        report.add("file_valid", False, "CRITICAL",
                   "File is not a valid ZIP/docx — may be corrupted or incomplete")
        return False


def check_company_name(full_text: str, xml_files: Dict[str, str], report: ValidationReport):
    # Search body text AND all header/footer XML (company name lives in headers)
    combined = full_text
    for key, val in xml_files.items():
        if "header" in key.lower() or "footer" in key.lower():
            combined += re.sub(r"<[^>]+>", " ", val)
    if COMPANY_NAME in combined:
        report.add("company_name", True, "CRITICAL",
                   f"Company name '{COMPANY_NAME}' found ✓")
    else:
        report.add("company_name", False, "CRITICAL",
                   f"Company name '{COMPANY_NAME}' NOT found",
                   "Check cover page and header — exact spelling and casing required")


def check_tagline(full_text: str, xml_files: Dict[str, str], report: ValidationReport):
    combined = full_text
    for key, val in xml_files.items():
        if "header" in key.lower():
            combined += re.sub(r"<[^>]+>", " ", val)
    if TAGLINE in combined:
        report.add("tagline", True, "WARNING", f"Tagline found ✓")
    else:
        report.add("tagline", False, "WARNING",
                   f"Tagline '{TAGLINE}' not found",
                   "Should appear on the cover page in italic teal text")


def check_strictly_confidential(xml_files: Dict[str, str], report: ValidationReport):
    footer_text = ""
    for key, val in xml_files.items():
        if "footer" in key.lower() or "document" in key.lower():
            footer_text += val

    if STRICTLY_CONF in footer_text:
        report.add("strictly_confidential", True, "CRITICAL",
                   "'Strictly Confidential' text found ✓")
    else:
        report.add("strictly_confidential", False, "CRITICAL",
                   "'Strictly Confidential' missing from footer/document",
                   "Required in every page footer — check makeFooter() in the generation script")


def check_teal_color(xml_files: Dict[str, str], report: ValidationReport):
    combined = " ".join(xml_files.values()).upper()
    if TEAL_COLOR in combined:
        report.add("teal_color", True, "CRITICAL",
                   f"InnoTech teal fill ({TEAL_COLOR}) found ✓")
    else:
        report.add("teal_color", False, "CRITICAL",
                   f"InnoTech teal fill ({TEAL_COLOR}) NOT found",
                   "Table headers must use fill color 1A949D. Check tealHeaderRow() helper.")


def check_light_blue_color(xml_files: Dict[str, str], report: ValidationReport):
    combined = " ".join(xml_files.values()).upper()
    if LIGHT_BLUE_COLOR in combined:
        report.add("light_blue_color", True, "WARNING",
                   f"Light-blue label fill ({LIGHT_BLUE_COLOR}) found ✓")
    else:
        report.add("light_blue_color", False, "WARNING",
                   f"Light-blue label fill ({LIGHT_BLUE_COLOR}) not found",
                   "Key-value label cells should use D9EAF7. Check labelCell() helper.")


def check_black_borders(xml_files: Dict[str, str], report: ValidationReport):
    doc_xml = xml_files.get("word/document.xml", "")
    has_border = re.search(r'w:color="000000"', doc_xml, re.IGNORECASE)
    if has_border:
        report.add("black_borders", True, "WARNING",
                   "Black table borders (000000) found ✓")
    else:
        report.add("black_borders", False, "WARNING",
                   "No black (000000) table border color found",
                   "All table cells should use fullBorder('000000')")


def check_cambria_font(xml_files: Dict[str, str], report: ValidationReport):
    combined = " ".join(xml_files.values())
    if "Cambria" in combined:
        report.add("cambria_font", True, "CRITICAL", "Cambria font found ✓")
    else:
        # Downgrade to WARNING — some templates embed fonts differently
        report.add("cambria_font", False, "WARNING",
                   "Cambria font not explicitly found in XML",
                   "Ensure Cambria is set in styles block in the Document constructor.")

    # Check for problematic non-standard fonts
    for bad_font in ["Calibri", "Times New Roman", "Cambria"]:
        if bad_font in combined:
            report.add(f"font_{bad_font.lower().replace(' ', '_')}", False, "WARNING",
                       f"Non-standard font '{bad_font}' detected",
                       f"Replace with Cambria throughout the document")


def check_page_size(xml_files: Dict[str, str], report: ValidationReport):
    doc_xml = xml_files.get("word/document.xml", "")
    w_match = re.search(r'<w:pgSz[^/]*w:w="(\d+)"', doc_xml)
    h_match = re.search(r'<w:pgSz[^/]*w:h="(\d+)"', doc_xml)

    A4_W_RANGE = {str(v) for v in range(11905, 11910)}
    A4_H_RANGE = {str(v) for v in range(16838, 16843)}
    if w_match and h_match:
        w, h = w_match.group(1), h_match.group(1)
        if w in A4_W_RANGE and h in A4_H_RANGE:
            report.add("page_size", True, "WARNING",
                       f"Page size: A4 ({w} × {h} DXA) ✓")
        else:
            report.add("page_size", False, "WARNING",
                       f"Page size: {w} × {h} DXA (expected A4 ~11907 × 16840)",
                       "Set page.size.width=11907, height=16840 in the section properties")
    else:
        report.add("page_size", False, "WARNING",
                   "Page size element <w:pgSz> not found",
                   "Explicit page size definition is required")


def check_no_solid_shading(xml_files: Dict[str, str], report: ValidationReport):
    doc_xml = xml_files.get("word/document.xml", "")
    solid = re.findall(r'w:val="solid"', doc_xml, re.IGNORECASE)
    if solid:
        report.add("shading_type", False, "WARNING",
                   f"ShadingType.SOLID detected ({len(solid)} instances)",
                   "Use ShadingType.CLEAR to prevent black backgrounds in table cells")
    else:
        report.add("shading_type", True, "WARNING",
                   "No SOLID shading detected — ShadingType.CLEAR in use ✓")


def check_required_sections(full_text: str, doc_type: str, report: ValidationReport):
    keywords = SECTION_KEYWORDS.get(doc_type, [])
    if not keywords:
        report.add("required_sections", True, "INFO",
                   f"No section keyword list defined for type '{doc_type}' — skipping")
        return

    missing = []
    for kw in keywords:
        if kw.lower() not in full_text.lower():
            missing.append(kw)

    if not missing:
        report.add("required_sections", True, "CRITICAL",
                   f"All required sections found ({len(keywords)}) ✓")
    else:
        report.add("required_sections", False, "CRITICAL",
                   f"Missing sections: {', '.join(missing)}",
                   f"Ensure all sections from {doc_type.lower()}-generation-standard.md are present")


def check_no_placeholders(full_text: str, report: ValidationReport):
    """Warn if bracketed placeholders still exist (excluding [TBD])."""
    placeholders = re.findall(r'\[(?!TBD)[^\]]{3,60}\]', full_text)
    placeholders = [p for p in placeholders if not p.startswith("[TBD")]
    if placeholders:
        sample = placeholders[:5]
        report.add("placeholders", False, "WARNING",
                   f"Unfilled placeholders found: {sample} {'…' if len(placeholders) > 5 else ''}",
                   "Replace all [bracketed placeholders] with actual content before delivery")
    else:
        report.add("placeholders", True, "WARNING",
                   "No unfilled placeholders detected ✓")


def check_approval_section(full_text: str, xml_files: Dict[str, str], report: ValidationReport):
    doc_xml_text = re.sub(r"<[^>]+>", " ", xml_files.get("word/document.xml", ""))
    combined = (full_text + " " + doc_xml_text).lower()
    approval_keywords = ["approval", "sign-off", "sign off", "uat sign", "signoff"]
    found = any(kw in combined for kw in approval_keywords)
    if found:
        report.add("approval_section", True, "CRITICAL",
                   "Approval / Sign-Off section found ✓")
    else:
        report.add("approval_section", False, "CRITICAL",
                   "Approval / Sign-Off section NOT found",
                   "Every InnoTech document must end with an Approval / Sign-Off section")


def check_document_control(full_text: str, xml_files: Dict[str, str], report: ValidationReport):
    # Use raw XML text for more reliable keyword matching (fields live in table cells)
    doc_xml_text = re.sub(r"<[^>]+>", " ", xml_files.get("word/document.xml", ""))
    combined = (full_text + " " + doc_xml_text).lower()
    # Primary fields — at least 2 required for pass
    primary_kws = ["prepared by", "reviewed by", "approved by"]
    found_primary = sum(1 for kw in primary_kws if kw in combined)
    # Any doc control indicator
    has_dc = "document control" in combined or "prepared by" in combined
    if found_primary >= 2 or (has_dc and found_primary >= 1):
        report.add("document_control", True, "CRITICAL",
                   f"Document Control section found ({found_primary}/3 primary fields) ✓")
    elif found_primary == 1:
        report.add("document_control", False, "WARNING",
                   f"Document Control partially found — only {found_primary}/3 primary fields detected",
                   "Ensure Prepared By, Reviewed By, Approved By are all present in Section 1")
    else:
        report.add("document_control", False, "CRITICAL",
                   "Document Control section not found",
                   "Section 1 must include Prepared By, Reviewed By, Approved By")


def check_revision_history(full_text: str, xml_files: Dict[str, str], report: ValidationReport):
    # Also search raw XML text — revision history may be in table cells not paragraphs
    doc_xml_text = re.sub(r"<[^>]+>", " ", xml_files.get("word/document.xml", ""))
    combined = (full_text + " " + doc_xml_text).lower()
    has_revision = "revision history" in combined or ("revision" in combined and "version" in combined)
    has_cols = "version" in combined and "description" in combined
    if has_revision and has_cols:
        report.add("revision_history", True, "CRITICAL", "Revision History section found ✓")
    elif has_revision:
        report.add("revision_history", False, "WARNING",
                   "Revision History heading found but table columns may be incomplete",
                   "Table must have: Version | Date | Prepared By | Description of Changes")
    else:
        report.add("revision_history", False, "WARNING",
                   "Revision History section not clearly detected — verify Section 2",
                   "Section 2 must be a Revision History table")


# ── Main Validator ────────────────────────────────────────────────────────────

def validate(docx_path: str, strict: bool = False) -> ValidationReport:
    doc_type = detect_doc_type(docx_path)
    report = ValidationReport(docx_path=docx_path, doc_type=doc_type)

    # 1. File integrity
    if not check_file_valid(docx_path, report):
        return report  # Cannot continue if file is broken

    # 2. Read XML
    xml_files = read_xml_from_docx(docx_path)
    full_text = extract_text_from_docx(docx_path)

    # 3. Branding checks
    check_company_name(full_text, xml_files, report)
    check_tagline(full_text, xml_files, report)
    check_strictly_confidential(xml_files, report)

    # 4. Style checks
    check_teal_color(xml_files, report)
    check_light_blue_color(xml_files, report)
    check_black_borders(xml_files, report)
    check_cambria_font(xml_files, report)
    check_page_size(xml_files, report)
    check_no_solid_shading(xml_files, report)

    # 5. Content / structure checks
    check_document_control(full_text, xml_files, report)
    check_revision_history(full_text, xml_files, report)
    check_required_sections(full_text, doc_type, report)
    check_approval_section(full_text, xml_files, report)

    # 6. Placeholder check
    check_no_placeholders(full_text, report)

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Validate an InnoTech-branded .docx file for compliance."
    )
    parser.add_argument("docx", help="Path to the .docx file")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as failures (stricter exit code)")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON instead of human-readable")
    parser.add_argument("--quiet", action="store_true",
                        help="Only show failures (suppress passed checks)")
    args = parser.parse_args()

    docx_path = args.docx
    if not Path(docx_path).exists():
        print(f"[validate] ERROR: File not found: {docx_path}", file=sys.stderr)
        sys.exit(2)

    report = validate(docx_path, strict=args.strict)

    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        report.print_report(verbose=not args.quiet)

    # Exit code
    if not report.overall_passed():
        sys.exit(1)
    if args.strict and report.warnings:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
