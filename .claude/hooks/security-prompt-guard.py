#!/usr/bin/env python3
"""
InnoTech Security Prompt Guard
================================
Fires on every UserPromptSubmit (and SessionStart for Claude Code / Codex).
Scans the incoming prompt for sensitive patterns and either:
  - MASKS  : redacts the value in-place and lets the (sanitised) prompt through
  - BLOCKS : exits with code 2, rejecting the prompt entirely

Configure behaviour per category in the RULES list below.
"""

import json
import re
import sys
from dataclasses import dataclass, field
from typing import Literal

# ─── Configuration ────────────────────────────────────────────────────────────

ACTION = Literal["mask", "block"]

@dataclass
class Rule:
    name: str
    pattern: re.Pattern
    action: ACTION          # "mask" → redact in prompt | "block" → reject whole prompt
    mask_label: str = ""    # shown in place of the matched value when action="mask"

RULES: list[Rule] = [
    # ── Hard blocks (these should NEVER reach the AI) ──────────────────────
    Rule(
        name="Private Key / PEM",
        pattern=re.compile(
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----[\s\S]+?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
            re.IGNORECASE,
        ),
        action="block",
    ),
    Rule(
        name="SSH Private Key Header",
        pattern=re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----", re.IGNORECASE),
        action="block",
    ),
    Rule(
        name="Database Connection String with Credentials",
        # matches: postgresql://user:pass@host, mysql://user:pass@host, etc.
        pattern=re.compile(
            r"(?:postgresql|mysql|mariadb|mongodb|redis|mssql|oracle):\/\/[^:@\s]+:[^@\s]+@[\w.\-]+",
            re.IGNORECASE,
        ),
        action="block",
    ),

    # ── Mask (redact value, allow sanitised prompt through) ────────────────
    Rule(
        name="AWS Access Key",
        pattern=re.compile(r"\b(AKIA[0-9A-Z]{16})\b"),
        action="mask",
        mask_label="[REDACTED:AWS_ACCESS_KEY]",
    ),
    Rule(
        name="AWS Secret Key",
        # 40-char base64 after common label
        pattern=re.compile(
            r"(?i)(?:aws[_\-]?secret[_\-]?(?:access[_\-]?)?key\s*[:=]\s*)([A-Za-z0-9/+=]{40})"
        ),
        action="mask",
        mask_label="[REDACTED:AWS_SECRET]",
    ),
    Rule(
        name="Generic API Key / Token assignment",
        # e.g.  API_KEY=abc123...  or  token: "eyJ..."
        pattern=re.compile(
            r"(?i)(?:api[_\-]?key|api[_\-]?secret|auth[_\-]?token|access[_\-]?token|bearer[_\-]?token)"
            r"\s*[:=]\s*['\"]?([A-Za-z0-9\-_./+=]{16,})['\"]?"
        ),
        action="mask",
        mask_label="[REDACTED:API_KEY]",
    ),
    Rule(
        name="JWT Token",
        pattern=re.compile(r"\b(eyJ[A-Za-z0-9\-_]+\.eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_.+/=]+)\b"),
        action="mask",
        mask_label="[REDACTED:JWT]",
    ),
    Rule(
        name="GitHub / GitLab Token",
        pattern=re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{36}|glpat-[A-Za-z0-9\-_]{20})\b"),
        action="mask",
        mask_label="[REDACTED:GIT_TOKEN]",
    ),
    Rule(
        name="Slack Token",
        pattern=re.compile(r"\b(xox[baprs]-[0-9A-Za-z\-]+)\b"),
        action="mask",
        mask_label="[REDACTED:SLACK_TOKEN]",
    ),
    Rule(
        name="Generic Password Assignment",
        # password = "something" or PASSWORD: mysecret123
        pattern=re.compile(
            r"(?i)(?:password|passwd|pwd)\s*[:=]\s*['\"]?(\S{8,})['\"]?"
        ),
        action="mask",
        mask_label="[REDACTED:PASSWORD]",
    ),
    Rule(
        name="Thai National ID / 13-digit ID",
        # 13-digit number that looks like an ID card
        pattern=re.compile(r"\b(\d{13})\b"),
        action="mask",
        mask_label="[REDACTED:NATIONAL_ID]",
    ),
    Rule(
        name="Credit Card Number",
        # Visa, MC, Amex, etc. with optional separators
        pattern=re.compile(r"\b(\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4})\b"),
        action="mask",
        mask_label="[REDACTED:CREDIT_CARD]",
    ),
    Rule(
        name="Email Address",
        # Only mask if it looks like an internal/staff email (you can relax this rule)
        pattern=re.compile(
            r"(?i)\b([a-z0-9._%+\-]+@(?:innotech|talentedge|internal)\.[a-z]{2,})\b"
        ),
        action="mask",
        mask_label="[REDACTED:INTERNAL_EMAIL]",
    ),
    Rule(
        name=".env File Content",
        # Whole-line VAR=value patterns pasted in bulk
        pattern=re.compile(
            r"(?m)^([A-Z][A-Z0-9_]{2,}=(?!false|true|0|1|\d+$)\S+)$"
        ),
        action="mask",
        mask_label="[REDACTED:ENV_VAR]",
    ),
]

# ─── Helpers ──────────────────────────────────────────────────────────────────

def read_stdin() -> dict:
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def extract_prompt(data: dict) -> str:
    """
    Claude Code: data["prompt"]
    OpenAI Codex: same field, but fall back to data["message"] or empty string.
    """
    return data.get("prompt") or data.get("message") or ""


def build_block_output(violated_rules: list[str]) -> None:
    """Exit 2 → rejects the prompt; stderr message shown to the user."""
    rule_list = "\n".join(f"  • {r}" for r in violated_rules)
    message = (
        "🚫 SECURITY BLOCK: Your prompt contains sensitive information that "
        "must not be sent to the AI.\n\n"
        f"Detected:\n{rule_list}\n\n"
        "Please remove the sensitive data and try again.\n"
        "Tip: Use environment variables or secret managers instead of pasting credentials."
    )
    print(message, file=sys.stderr)
    sys.exit(2)


def build_mask_output(sanitised_prompt: str, masked_rules: list[str]) -> None:
    """Exit 0 with JSON stdout → replaces the prompt with the sanitised version."""
    rule_list = ", ".join(masked_rules)
    # additionalContext is shown to Claude so it knows redaction happened
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": (
                f"⚠️ Security guard automatically redacted sensitive values in the user's prompt "
                f"({rule_list}). The redacted tokens appear as [REDACTED:TYPE]. "
                "Do not ask the user to reveal the original values."
            ),
            # Replace the prompt text Claude will see
            "updatedPrompt": sanitised_prompt,
        }
    }
    print(json.dumps(output))
    sys.exit(0)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    data = read_stdin()
    prompt = extract_prompt(data)

    if not prompt:
        sys.exit(0)  # nothing to check

    blocked_rules: list[str] = []
    masked_rules: list[str] = []
    sanitised = prompt

    for rule in RULES:
        if rule.action == "block":
            if rule.pattern.search(sanitised):
                blocked_rules.append(rule.name)
        elif rule.action == "mask":
            # Only mask the captured group (group 1) when present, otherwise full match
            def replacer(m: re.Match, lbl: str = rule.mask_label) -> str:
                if m.lastindex:
                    # Replace only the captured group, preserve surrounding text
                    start, end = m.span(1)
                    relative_start = start - m.start()
                    relative_end = end - m.start()
                    full = m.group(0)
                    return full[:relative_start] + lbl + full[relative_end:]
                return lbl

            new_text = rule.pattern.sub(replacer, sanitised)
            if new_text != sanitised:
                masked_rules.append(rule.name)
                sanitised = new_text

    # Blocks take priority — if any block rule fired, reject the whole prompt
    if blocked_rules:
        build_block_output(blocked_rules)

    # If only masking happened, pass through the sanitised prompt
    if masked_rules:
        build_mask_output(sanitised, masked_rules)

    # All clear
    sys.exit(0)


if __name__ == "__main__":
    main()