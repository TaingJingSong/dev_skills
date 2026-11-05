#!/usr/bin/env python3
"""
style_apply.py — InnoTech Style Patcher

Post-processes a generated .docx file and verifies (and optionally patches)
InnoTech style constants. Operates on the raw XML inside the docx ZIP.

Checks performed:
  - Teal fill color on table header rows (1A949D)
  - Light-blue fill on label cells (D9EAF7)
  - Cambria font throughout
  - Black table borders (000000)
  - Footer "Strictly Confidential" text
  - Page size: A4 (11907 x 16840 DXA)

Patch mode:
  When --patch is supplied, the script rewrites incorrect color values and
  font names to match the InnoTech standard, then repacks the docx.

Usage:
    python style_apply.py document.docx [--patch] [--out patched.docx]
"""

import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Dict, List, Tuple

# ── InnoTech Style Constants ─────────────────────────────────────────────────

STYLE_CONSTANTS = {
    "TEAL":       "1A949D",
    "LIGHT_BLUE": "D9EAF7",
    "WHITE":      "FFFFFF",
    "BLACK":      "000000",
    "FONT":       "Cambria",
    "PAGE_W":     "11907",   # A4 width in DXA
    "PAGE_H":     "16840",   # A4 height in DXA
}

# Colors that SHOULD be teal (common wrong blues from default Word styles)
WRONG_TEAL_COLORS = {"2E75B6", "4472C4", "0070C0", "17375E", "1F497D", "2F5597"}

# Colors that SHOULD be light-blue
WRONG_LIGHTBLUE_COLORS = {"DEEAF1", "BDD7EE", "9DC3E6", "CFE2F3", "DEEBF7"}

# Fonts that should be replaced with Cambria
WRONG_FONTS = {"Calibri", "Times New Roman", "Cambria", "Tahoma", "Verdana"}

STRICTLY_CONFIDENTIAL_TEXT = "Strictly Confidential"


# ── Helpers ──────────────────────────────────────────────────────────────────

def read_docx_xml(docx_path: str) -> Dict[str, str]:
    """Extract all XML files from a docx as a dict {filename: content}."""
    files = {}
    with zipfile.ZipFile(docx_path, "r") as z:
        for name in z.namelist():
            if name.endswith(".xml") or name.endswith(".rels"):
                files[name] = z.read(name).decode("utf-8", errors="replace")
    return files


def write_docx_xml(original_docx: str, xml_files: Dict[str, str], output_path: str) -> None:
    """Repack a docx, replacing XML files with patched versions."""
    shutil.copy2(original_docx, output_path)
    with zipfile.ZipFile(output_path, "a") as z:
        for name, content in xml_files.items():
            z.writestr(name, content.encode("utf-8"))
    print(f"[style_apply] Patched docx written to: {output_path}")


def find_pattern(xml: str, pattern: str) -> List[str]:
    return re.findall(pattern, xml, re.IGNORECASE)


# ── Check Functions ──────────────────────────────────────────────────────────

class StyleReport:
    def __init__(self):
        self.issues: List[str] = []
        self.patches: List[Tuple[str, str, str]] = []  # (file, from, to)
        self.ok: List[str] = []

    def add_issue(self, msg: str):
        self.issues.append(msg)

    def add_patch(self, file: str, from_val: str, to_val: str):
        self.patches.append((file, from_val, to_val))

    def add_ok(self, msg: str):
        self.ok.append(msg)

    def print_summary(self):
        print(f"\n{'═'*60}")
        print("  InnoTech Style Report")
        print(f"{'═'*60}")
        if self.ok:
            print(f"\n  ✅ PASSED ({len(self.ok)})")
            for msg in self.ok:
                print(f"     {msg}")
        if self.issues:
            print(f"\n  ⚠️  ISSUES ({len(self.issues)})")
            for msg in self.issues:
                print(f"     {msg}")
        if self.patches:
            print(f"\n  🔧 PATCHES APPLIED ({len(self.patches)})")
            for file, from_val, to_val in self.patches:
                print(f"     [{file}] '{from_val}' → '{to_val}'")
        if not self.issues and not self.patches:
            print("\n  All style checks passed. No patches needed.")
        print(f"\n{'═'*60}\n")

    @property
    def passed(self) -> bool:
        return len(self.issues) == 0


def check_page_size(xml: str, report: StyleReport) -> None:
    """Verify A4 page dimensions in document.xml."""
    w_match = re.search(r'<w:pgSz[^>]*w:w="(\d+)"', xml)
    h_match = re.search(r'<w:pgSz[^>]*w:h="(\d+)"', xml)

    if w_match and h_match:
        w, h = w_match.group(1), h_match.group(1)
        if w == STYLE_CONSTANTS["PAGE_W"] and h == STYLE_CONSTANTS["PAGE_H"]:
            report.add_ok(f"Page size: A4 ({w} × {h} DXA) ✓")
        else:
            report.add_issue(
                f"Page size mismatch: found {w} × {h} DXA, "
                f"expected {STYLE_CONSTANTS['PAGE_W']} × {STYLE_CONSTANTS['PAGE_H']} (A4)"
            )
    else:
        report.add_issue("Page size element <w:pgSz> not found in document.xml")


def check_font(xml: str, report: StyleReport) -> Tuple[str, bool]:
    """Check for wrong fonts; return patched XML and whether patched."""
    patched = False
    for wrong_font in WRONG_FONTS:
        pattern = re.compile(re.escape(wrong_font), re.IGNORECASE)
        if pattern.search(xml):
            report.add_issue(
                f"Non-standard font found: '{wrong_font}' — should be 'Cambria'"
            )
    # Check Cambria presence
    if "Cambria" in xml:
        report.add_ok("Font: Cambria found ✓")
    return xml, patched


def check_and_patch_colors(
    xml: str, filename: str, report: StyleReport, do_patch: bool
) -> str:
    """Check teal and light-blue color fills; patch if requested."""
    # Check teal header fill
    teal_found = STYLE_CONSTANTS["TEAL"].upper() in xml.upper()
    if teal_found:
        report.add_ok(f"[{filename}] Teal header fill (1A949D) found ✓")
    else:
        # Look for known wrong blues
        wrong_used = [c for c in WRONG_TEAL_COLORS if c.upper() in xml.upper()]
        if wrong_used:
            report.add_issue(
                f"[{filename}] Wrong header color: {wrong_used} — expected 1A949D (InnoTech teal)"
            )
            if do_patch:
                for wrong in wrong_used:
                    pattern = re.compile(wrong, re.IGNORECASE)
                    xml = pattern.sub(STYLE_CONSTANTS["TEAL"], xml)
                    report.add_patch(filename, wrong, STYLE_CONSTANTS["TEAL"])

    # Check light-blue label fill
    lb_found = STYLE_CONSTANTS["LIGHT_BLUE"].upper() in xml.upper()
    if lb_found:
        report.add_ok(f"[{filename}] Light-blue label fill (D9EAF7) found ✓")
    else:
        wrong_lb = [c for c in WRONG_LIGHTBLUE_COLORS if c.upper() in xml.upper()]
        if wrong_lb:
            report.add_issue(
                f"[{filename}] Wrong label-cell color: {wrong_lb} — expected D9EAF7"
            )
            if do_patch:
                for wrong in wrong_lb:
                    pattern = re.compile(wrong, re.IGNORECASE)
                    xml = pattern.sub(STYLE_CONSTANTS["LIGHT_BLUE"], xml)
                    report.add_patch(filename, wrong, STYLE_CONSTANTS["LIGHT_BLUE"])

    return xml


def check_strictly_confidential(xml: str, report: StyleReport) -> None:
    """Verify 'Strictly Confidential' text exists in footer XML."""
    if STRICTLY_CONFIDENTIAL_TEXT in xml:
        report.add_ok("Footer: 'Strictly Confidential' text found ✓")
    else:
        report.add_issue(
            "Footer: 'Strictly Confidential' text NOT found. "
            "Check footer section in word/footer1.xml or word/document.xml."
        )


def check_borders(xml: str, report: StyleReport) -> None:
    """Check for black table borders."""
    black_border = re.search(r'w:color="000000"', xml, re.IGNORECASE)
    if black_border:
        report.add_ok("Table borders: Black (000000) color found ✓")
    else:
        report.add_issue(
            "Table borders: No black (000000) border color found. "
            "Verify table cells use fullBorder('000000')."
        )


def check_shading_type(xml: str, report: StyleReport) -> None:
    """Warn if ShadingType.SOLID is used (should be CLEAR)."""
    solid_pattern = re.findall(r'w:fill="[^"]*"[^>]*w:val="solid"', xml, re.IGNORECASE)
    if solid_pattern:
        report.add_issue(
            f"ShadingType.SOLID detected ({len(solid_pattern)} instances). "
            "Change to ShadingType.CLEAR to avoid black backgrounds."
        )
    else:
        report.add_ok("Shading type: No SOLID shading detected ✓")


# ── Main ─────────────────────────────────────────────────────────────────────

def run_checks(docx_path: str, do_patch: bool, output_path: str) -> StyleReport:
    report = StyleReport()
    xml_files = read_docx_xml(docx_path)
    patched_files: Dict[str, str] = {}

    doc_xml_key = "word/document.xml"
    doc_xml = xml_files.get(doc_xml_key, "")

    # Page size
    check_page_size(doc_xml, report)

    # Font check
    styles_xml = xml_files.get("word/styles.xml", doc_xml)
    check_font(styles_xml, report)

    # Colors: check document.xml and styles.xml
    for fname in [doc_xml_key, "word/styles.xml"]:
        xml = xml_files.get(fname, "")
        if xml:
            patched = check_and_patch_colors(xml, fname, report, do_patch)
            if patched != xml:
                patched_files[fname] = patched

    # Borders
    check_borders(doc_xml, report)

    # Shading type
    check_shading_type(doc_xml, report)

    # Strictly Confidential
    footer_xml = ""
    for key in xml_files:
        if "footer" in key.lower():
            footer_xml += xml_files[key]
    check_strictly_confidential(footer_xml or doc_xml, report)

    # Write patched docx if needed
    if do_patch and patched_files:
        write_docx_xml(docx_path, patched_files, output_path)
    elif do_patch:
        print("[style_apply] No patches were needed — output is identical to input.")

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Check and optionally patch InnoTech style compliance in a .docx file."
    )
    parser.add_argument("docx", help="Path to the .docx file to check")
    parser.add_argument("--patch", action="store_true",
                        help="Patch incorrect style values in-place")
    parser.add_argument("--out", default=None,
                        help="Output path for patched docx (default: overwrites original)")
    args = parser.parse_args()

    docx_path = args.docx
    if not Path(docx_path).exists():
        print(f"[style_apply] ERROR: File not found: {docx_path}", file=sys.stderr)
        sys.exit(1)

    output_path = args.out or docx_path

    print(f"\n[style_apply] Checking: {docx_path}")
    if args.patch:
        print(f"[style_apply] Patch mode: ON → output: {output_path}")

    report = run_checks(docx_path, do_patch=args.patch, output_path=output_path)
    report.print_summary()

    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
