#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "report_input.json"
OUTPUT_DIR = BASE_DIR / "output"


DEFAULT_PROJECT_STATUS = (
    "The project is progressing well with multiple enhancements completed. "
    "Most modules are stable, with ongoing feature development and improvements."
)


def bullet_list(items: list[str]) -> str:
    if not items:
        return "• -"
    return "\n".join(f"• {item}" for item in items)


def build_report(data: dict) -> str:
    recipient = data.get("recipient_display", "bong @PHYNY_NAN")
    week_label = data.get("week_label", "May W3")
    project_status = data.get("project_status", DEFAULT_PROJECT_STATUS)
    achievements = data.get("achievements", [])
    next_sprint = data.get("next_sprint", [])
    slide_link = data.get("slide_link", "")
    sender_name = data.get("sender_name", "Taing ChingSong")
    images = data.get("images", [])

    image_text = ""
    if images:
        image_text = "\n\nImage attachments:\n" + "\n".join(f"- {path}" for path in images)

    return f"""
Dear {recipient},

I hope you are doing well.

Please find below the weekly update for {week_label}:

1. Project Status
{project_status}

2. Achievements This Sprint:

{bullet_list(achievements)}

3. Plan for Next Sprint

{bullet_list(next_sprint)}

4. Progress Slide
You can view the detailed progress here:
project progress ({slide_link})

Please let me know if you need any further details.

Best regards,
{sender_name}
{image_text}
""".strip()


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Missing input file: {INPUT_FILE}")

    with INPUT_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    report = build_report(data)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_txt = OUTPUT_DIR / f"weekly_report_{timestamp}.txt"
    output_md = OUTPUT_DIR / f"weekly_report_{timestamp}.md"

    output_txt.write_text(report, encoding="utf-8")
    output_md.write_text(report, encoding="utf-8")

    print("\n" + "=" * 70)
    print("WEEKLY REPORT PREVIEW")
    print("=" * 70)
    print(report)
    print("=" * 70)

    print("\nSaved files:")
    print(f"- {output_txt}")
    print(f"- {output_md}")
    print("\nCopy the preview above and send it manually in Telegram.")


if __name__ == "__main__":
    main()