#!/usr/bin/env python3
"""
generate_docx.py — InnoTech Document Generation Orchestrator

Orchestrates the full generation pipeline:
  1. Loads document type standard and collects inputs
  2. Generates a Node.js docx-js script from the prompt template
  3. Executes the Node.js script to produce the .docx
  4. Runs validate_document.py to check compliance
  5. Reports the output file location
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

SKILL_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = Path(__file__).parent
OUTPUT_DIR = Path("./output")

DOC_TYPES = {
    "BRD":  {"label": "Business Requirement Document",        "code": "BRD"},
    "PRD":  {"label": "Product Requirement Document",         "code": "PRD"},
    "SRS":  {"label": "Software Requirements Specification",  "code": "SRS"},
    "FRD":  {"label": "Functional Requirement Document",      "code": "FRD"},
    "TRD":  {"label": "Technical Requirement Document",       "code": "TRD"},
    "API":  {"label": "API Specification",                    "code": "API"},
    "DD":   {"label": "Data Dictionary",                      "code": "DD"},
    "UAT":  {"label": "User Acceptance Testing Document",     "code": "UAT"},
    "IRL":  {"label": "Issue and Risk Log",                   "code": "IRL"},
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate an InnoTech-branded .docx document."
    )
    parser.add_argument(
        "--type", required=True, choices=list(DOC_TYPES.keys()),
        help="Document type code (BRD, PRD, SRS, FRD, TRD, API, DD, UAT, IRL)"
    )
    parser.add_argument(
        "--project", required=True,
        help="Project name (used in file naming and document title)"
    )
    parser.add_argument(
        "--inputs", default=None,
        help="Path to a JSON file containing input variables (optional)"
    )
    parser.add_argument(
        "--script", default=None,
        help="Path to an already-generated Node.js script to run directly (skip AI generation)"
    )
    parser.add_argument(
        "--output", default=str(OUTPUT_DIR),
        help="Output directory for the generated .docx file"
    )
    parser.add_argument(
        "--skip-validate", action="store_true",
        help="Skip validation step"
    )
    return parser.parse_args()


def sanitize_project_name(name: str) -> str:
    """Convert project name to safe filename component."""
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in name)


def build_output_filename(doc_type: str, project: str) -> str:
    today = date.today().strftime("%Y-%m-%d")
    safe_project = sanitize_project_name(project)
    return f"{doc_type}_{safe_project}_{today}.docx"


def run_nodejs_script(script_path: str, output_path: str) -> bool:
    """Execute the generated Node.js docx-js script."""
    print(f"[generate_docx] Running Node.js script: {script_path}")
    result = subprocess.run(
        ["node", script_path, "--output", output_path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[generate_docx] ERROR: Node.js script failed.\n{result.stderr}", file=sys.stderr)
        return False
    print(f"[generate_docx] Node.js script completed successfully.")
    if result.stdout:
        print(result.stdout)
    return True


def validate_output(docx_path: str) -> bool:
    """Run validate_document.py on the output file."""
    validate_script = SCRIPTS_DIR / "validate_document.py"
    print(f"[generate_docx] Validating: {docx_path}")
    result = subprocess.run(
        [sys.executable, str(validate_script), docx_path],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"[generate_docx] VALIDATION WARNINGS:\n{result.stderr}", file=sys.stderr)
        return False
    return True


def main():
    args = parse_args()
    doc_info = DOC_TYPES[args.type]
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_filename = build_output_filename(args.type, args.project)
    output_path = output_dir / output_filename

    print(f"\n{'='*60}")
    print(f"  InnoTech Document Generator")
    print(f"  Type    : {args.type} — {doc_info['label']}")
    print(f"  Project : {args.project}")
    print(f"  Output  : {output_path}")
    print(f"{'='*60}\n")

    # Load inputs if provided
    inputs = {}
    if args.inputs:
        with open(args.inputs) as f:
            inputs = json.load(f)
        print(f"[generate_docx] Loaded {len(inputs)} input variables from {args.inputs}")

    # Run Node.js generation script
    if args.script:
        script_path = args.script
    else:
        # Expect the Node.js script to be generated externally (by AI agent) and passed in
        print(
            "[generate_docx] No --script provided. Please generate the Node.js docx-js script\n"
            "  using the prompt in prompts/generate-{type}.md, then pass it via --script.\n"
            "  Example: python generate_docx.py --type BRD --project MyProject "
            "--script generated_brd.js"
        )
        sys.exit(1)

    success = run_nodejs_script(script_path, str(output_path))
    if not success:
        print("[generate_docx] Generation failed. Review the Node.js script for errors.")
        sys.exit(2)

    if not args.skip_validate:
        valid = validate_output(str(output_path))
        if not valid:
            print("[generate_docx] Document generated but validation reported issues.")
            print("                Review the warnings and update the document before delivery.")
    else:
        print("[generate_docx] Validation skipped (--skip-validate flag set).")

    print(f"\n[generate_docx] SUCCESS: {output_path}\n")


if __name__ == "__main__":
    main()
