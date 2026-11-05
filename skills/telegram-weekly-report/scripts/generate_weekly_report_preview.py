#!/usr/bin/env python3
"""Generate manual copy/paste weekly Telegram report. No network or authentication."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def require(data: dict, key: str):
    val = data.get(key)
    if not isinstance(val, str) or not val.strip():
        raise ValueError(f"Required non-empty string: {key}")
    return val.strip()


def bullet_list(items: list[str]) -> str:
    if not isinstance(items, list) or not all(isinstance(x, str) and x.strip() for x in items):
        raise ValueError("Achievements and next_sprint must be lists of non-empty strings")
    return "\n".join(f"• {item.strip()}" for item in items) or "• None reported"


def build_report(data: dict) -> str:
    recipient = require(data, "recipient_display")
    week = require(data, "week_label")
    status = require(data, "project_status")
    sender = require(data, "sender_name")
    achievement_lines = bullet_list(data.get("achievements", []))
    next_lines = bullet_list(data.get("next_sprint", []))
    slide_link = data.get("slide_link", "")
    if not isinstance(slide_link, str):
        raise ValueError("slide_link must be a string")
    images = data.get("images", [])
    if not isinstance(images, list) or not all(isinstance(x, str) for x in images):
        raise ValueError("images must be a list of strings")
    image_text = "\n\nImages for manual upload:\n" + "\n".join(f"- {x}" for x in images) if images else ""
    return (f"Dear {recipient},\n\nPlease find below the weekly update for {week}.\n\n"
            f"1. Project Status\n{status}\n\n2. Achievements This Sprint\n{achievement_lines}\n\n"
            f"3. Plan for Next Sprint\n{next_lines}\n\n4. Progress Slide\n"
            f"{slide_link or 'Not provided'}\n\nBest regards,\n{sender}{image_text}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path, help="User-created JSON containing factual weekly updates")
    p.add_argument("--output", type=Path, default=Path("./output"), help="Output folder; default ./output")
    a = p.parse_args()
    try:
        data = json.loads(a.input.read_text(encoding="utf-8"))
        report = build_report(data)
        a.output.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        for suffix in ("txt", "md"):
            target = a.output / f"weekly_report_{stamp}.{suffix}"
            target.write_text(report + "\n", encoding="utf-8")
            print(f"Saved: {target}")
        print("\nWEEKLY REPORT PREVIEW (NOT SENT)\n" + "=" * 42 + "\n" + report)
        print("\nPreview only. Copy/paste into Telegram manually. Upload images separately.")
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        p.error(str(exc))


if __name__ == "__main__":
    main()
