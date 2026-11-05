#!/usr/bin/env python3
"""
template_loader.py — InnoTech Document Template Input Loader

Reads the generation standard for a document type and provides:
  - A structured input variable schema
  - Interactive CLI prompting for missing inputs
  - JSON export of collected inputs
  - JavaScript variable export for use in docx-js scripts
"""

import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

SKILL_ROOT = Path(__file__).parent.parent
REFERENCES_DIR = SKILL_ROOT / "references"

# ── Input schemas per document type ──────────────────────────────────────────

COMMON_INPUTS = {
    "PROJECT_TITLE":    {"label": "Project Title",          "required": True,  "default": None},
    "PROJECT_NAME":     {"label": "Project / System Name",  "required": True,  "default": None},
    "DOCUMENT_ID":      {"label": "Document ID",            "required": False, "default": "[TBD]"},
    "PREPARED_BY":      {"label": "Prepared By",            "required": True,  "default": None},
    "REVIEWED_BY":      {"label": "Reviewed By",            "required": False, "default": "[TBD]"},
    "APPROVED_BY":      {"label": "Approved By",            "required": False, "default": "[TBD]"},
    "VERSION":          {"label": "Version",                "required": False, "default": "0.1"},
    "DATE":             {"label": "Date (DD-MMM-YYYY)",     "required": False, "default": date.today().strftime("%d-%b-%Y").upper()},
    "STATUS":           {"label": "Document Status",        "required": False, "default": "Draft",
                         "choices": ["Draft", "Review", "Approved", "Final"]},
    "CONFIDENTIALITY":  {"label": "Confidentiality",        "required": False, "default": "Strictly Confidential",
                         "choices": ["Internal", "Restricted", "Strictly Confidential", "Public"]},
}

TYPE_EXTRA_INPUTS: Dict[str, Dict] = {
    "BRD": {
        "BUSINESS_CONTEXT":  {"label": "Business Context (2-4 sentences)", "required": True,  "default": None, "multiline": True},
        "OBJECTIVES":        {"label": "Business Objectives (one per line)", "required": True, "default": None, "multiline": True},
        "SCOPE_IN":          {"label": "In-Scope items (one per line)",      "required": True, "default": None, "multiline": True},
        "SCOPE_OUT":         {"label": "Out-of-Scope items (one per line)",  "required": False,"default": "[TBD]", "multiline": True},
    },
    "PRD": {
        "PRODUCT_VISION":    {"label": "Product Vision Statement",           "required": True,  "default": None},
        "PROBLEM_STATEMENT": {"label": "Problem Statement",                  "required": True,  "default": None, "multiline": True},
        "SCOPE_IN":          {"label": "In-Scope features (one per line)",   "required": True,  "default": None, "multiline": True},
    },
    "SRS": {
        "SYSTEM_OVERVIEW":   {"label": "System Overview (brief description)","required": True,  "default": None, "multiline": True},
        "SCOPE_IN":          {"label": "In-Scope items (one per line)",      "required": True,  "default": None, "multiline": True},
    },
    "FRD": {
        "MODULES":           {"label": "Module names (one per line)",        "required": True,  "default": None, "multiline": True},
        "SCOPE_IN":          {"label": "In-Scope functional areas",          "required": True,  "default": None, "multiline": True},
    },
    "TRD": {
        "SYSTEM_OVERVIEW":   {"label": "Technical System Overview",          "required": True,  "default": None, "multiline": True},
        "TECH_STACK":        {"label": "Technology Stack (languages, frameworks, DB)", "required": False, "default": "[TBD]"},
    },
    "API": {
        "API_NAME":          {"label": "API / Service Name",                 "required": True,  "default": None},
        "OWNING_SYSTEM":     {"label": "Owning System / Platform",           "required": True,  "default": None},
        "INTERFACE_TYPE":    {"label": "Interface Type",                     "required": False, "default": "REST",
                              "choices": ["REST", "SOAP", "GraphQL", "Webhook", "File-Based", "Other"]},
        "AUTH_METHOD":       {"label": "Authentication Method",              "required": False, "default": "OAuth 2.0"},
    },
    "DD": {
        "DATA_OWNER":        {"label": "Data Owner (name / department)",     "required": False, "default": "[TBD]"},
        "ENTITIES":          {"label": "Entity / Table names (one per line)","required": True,  "default": None, "multiline": True},
    },
    "UAT": {
        "UAT_FROM":          {"label": "UAT Period From (DD-MMM-YYYY)",      "required": False, "default": "[TBD]"},
        "UAT_TO":            {"label": "UAT Period To (DD-MMM-YYYY)",        "required": False, "default": "[TBD]"},
        "UAT_OBJECTIVE":     {"label": "UAT Objective",                      "required": True,  "default": None, "multiline": True},
        "SCOPE_IN":          {"label": "In-Scope modules / features",        "required": True,  "default": None, "multiline": True},
    },
    "IRL": {
        "CUSTOMER":          {"label": "Customer / Client Name",             "required": False, "default": "[TBD]"},
        "REPORTING_PERIOD":  {"label": "Reporting Period (Week / Month)",    "required": False, "default": "[TBD]"},
        "PROJECT_MANAGER":   {"label": "Project Manager",                    "required": False, "default": "[TBD]"},
        "OWNER":             {"label": "Log Owner",                          "required": False, "default": "[TBD]"},
    },
}


class TemplateLoader:
    """Load and manage inputs for a specific InnoTech document type."""

    def __init__(self, doc_type: str):
        doc_type = doc_type.upper()
        if doc_type not in TYPE_EXTRA_INPUTS and doc_type not in ["BRD","PRD","SRS","FRD","TRD","API","DD","UAT","IRL"]:
            raise ValueError(f"Unknown document type: {doc_type}")
        self.doc_type = doc_type
        self.schema = {**COMMON_INPUTS, **TYPE_EXTRA_INPUTS.get(doc_type, {})}
        self.values: Dict[str, Any] = {}

    def load_standard(self) -> str:
        """Read the generation standard markdown for the doc type."""
        filename_map = {
            "BRD": "brd-generation-standard.md",
            "PRD": "prd-generation-standard.md",
            "SRS": "srs-generation-standard.md",
            "FRD": "frd-generation-standard.md",
            "TRD": "trd-generation-standard.md",
            "API": "api-spec-generation-standard.md",
            "DD":  "data-dictionary-generation-standard.md",
            "UAT": "uat-generation-standard.md",
            "IRL": "issue-risk-log-generation-standard.md",
        }
        path = REFERENCES_DIR / filename_map[self.doc_type]
        if path.exists():
            return path.read_text()
        return f"[Standard not found at {path}]"

    def load_from_json(self, json_path: str) -> "TemplateLoader":
        """Load inputs from a JSON file."""
        with open(json_path) as f:
            data = json.load(f)
        self.values.update(data)
        return self

    def prompt_for_inputs(self, skip_optional: bool = False) -> Dict[str, Any]:
        """Interactively prompt the user for each input variable."""
        print(f"\n{'─'*50}")
        print(f"  Input Collection: {self.doc_type}")
        print(f"  (Press Enter to accept default; type value to override)")
        print(f"{'─'*50}\n")

        for key, meta in self.schema.items():
            if key in self.values:
                continue  # Already loaded from JSON
            if skip_optional and not meta.get("required"):
                self.values[key] = meta.get("default", "[TBD]")
                continue

            label = meta["label"]
            default = meta.get("default")
            choices = meta.get("choices")
            multiline = meta.get("multiline", False)
            required = meta.get("required", False)

            prompt_str = f"  {label}"
            if default:
                prompt_str += f" [{default}]"
            if choices:
                prompt_str += f"\n  Options: {' / '.join(choices)}"
            if multiline:
                prompt_str += "\n  (Enter multiple lines; blank line to finish)"
            prompt_str += ": "

            if multiline:
                print(prompt_str)
                lines = []
                while True:
                    line = input("    > ").strip()
                    if not line:
                        break
                    lines.append(line)
                value = "\n".join(lines) if lines else (default or "")
            else:
                value = input(prompt_str).strip()
                if not value:
                    value = default or ""

            if choices and value and value not in choices:
                print(f"  Warning: '{value}' is not in the standard choices. Using as-is.")

            if required and not value:
                print(f"  [Required] No value provided — marking as [TBD]")
                value = "[TBD]"

            self.values[key] = value

        print("\n  [TemplateLoader] Input collection complete.\n")
        return self.values

    def get_values(self) -> Dict[str, Any]:
        return self.values

    def export_json(self, output_path: str) -> None:
        """Export collected inputs to a JSON file."""
        with open(output_path, "w") as f:
            json.dump(self.values, f, indent=2)
        print(f"[TemplateLoader] Inputs exported to {output_path}")

    def export_js_vars(self, output_path: str) -> None:
        """Export collected inputs as JavaScript const declarations."""
        lines = ["// Auto-generated input variables for InnoTech document generation", ""]
        for key, value in self.values.items():
            safe_value = str(value).replace("`", "'").replace("\\", "\\\\")
            lines.append(f"const {key} = `{safe_value}`;")
        lines.append("")
        lines.append("module.exports = {")
        for key in self.values:
            lines.append(f"  {key},")
        lines.append("};")

        with open(output_path, "w") as f:
            f.write("\n".join(lines))
        print(f"[TemplateLoader] JS variables exported to {output_path}")

    def summary(self) -> str:
        """Return a human-readable summary of loaded inputs."""
        lines = [f"\n  Input Summary — {self.doc_type}", "  " + "─" * 40]
        for key, value in self.values.items():
            label = self.schema.get(key, {}).get("label", key)
            display_val = str(value)[:60] + ("…" if len(str(value)) > 60 else "")
            lines.append(f"  {label:<35} {display_val}")
        return "\n".join(lines)


# ── CLI entry point ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Collect inputs for InnoTech document generation.")
    parser.add_argument("--type", required=True, help="Document type (BRD, PRD, SRS, etc.)")
    parser.add_argument("--inputs", default=None, help="Optional JSON file of pre-filled inputs")
    parser.add_argument("--out-json", default=None, help="Export inputs to JSON")
    parser.add_argument("--out-js",   default=None, help="Export inputs as JS variables")
    parser.add_argument("--skip-optional", action="store_true", help="Auto-fill optional fields with defaults")
    args = parser.parse_args()

    loader = TemplateLoader(args.type)
    if args.inputs:
        loader.load_from_json(args.inputs)
    loader.prompt_for_inputs(skip_optional=args.skip_optional)
    print(loader.summary())

    if args.out_json:
        loader.export_json(args.out_json)
    if args.out_js:
        loader.export_js_vars(args.out_js)
