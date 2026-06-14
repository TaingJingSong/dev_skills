import os
import asyncio
from pathlib import Path
from datetime import datetime
from telethon import TelegramClient


BASE_DIR = Path(__file__).resolve().parent
SESSION_NAME = str(BASE_DIR / "telegram_user_report")

API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]


DEFAULT_TARGET = "@PHYNY_NAN"
DEFAULT_SENDER_NAME = "Taing ChingSong"


def ask_text(prompt: str, default: str | None = None) -> str:
    if default:
        value = input(f"{prompt} [{default}]: ").strip()
        return value or default

    return input(f"{prompt}: ").strip()


def ask_multiline(title: str) -> list[str]:
    print(f"\n{title}")
    print("Enter one item per line. Press Enter on empty line to finish.")

    items: list[str] = []

    while True:
        line = input("> ").strip()
        if not line:
            break
        items.append(line)

    return items


def ask_image_paths() -> list[Path]:
    print("\nImage attachments")
    print("Enter image paths one by one. Press Enter on empty line to finish.")
    print("Example: /Users/macbookpro/Desktop/progress.png")

    paths: list[Path] = []

    while True:
        raw_path = input("> ").strip()
        if not raw_path:
            break

        path = Path(raw_path).expanduser()

        if not path.exists():
            print(f"⚠️ File not found: {path}")
            continue

        if path.suffix.lower() not in [".png", ".jpg", ".jpeg", ".webp"]:
            print(f"⚠️ Unsupported image type: {path.suffix}")
            continue

        paths.append(path)

    return paths


def format_bullet_items(items: list[str], default_items: list[str] | None = None) -> str:
    final_items = items or default_items or ["-"]
    return "\n".join(f"• {item}" for item in final_items)


def build_report_message(
    recipient: str,
    week_label: str,
    project_status: str,
    achievements: list[str],
    next_sprint: list[str],
    slide_link: str,
    sender_name: str,
) -> str:
    achievements_text = format_bullet_items(
        achievements,
        default_items=[
            "Addressing UAT Feedback (Testing & Fixing) 🟢",
            "Release Preparation 🟢",
        ],
    )

    next_sprint_text = format_bullet_items(
        next_sprint,
        default_items=[
            "Migrate to New Backend Core 🔵",
            "Implement Multi Shift/Roster Shift 🟠",
        ],
    )

    return f"""
Dear bong {recipient},

I hope you are doing well.

Please find below the weekly update for {week_label}:

**1. Project Status**
{project_status}

**2. Achievements This Sprint:**

{achievements_text}

**3. Plan for Next Sprint**

{next_sprint_text}

**4. Progress Slide**
You can view the detailed progress here:
[project progress]({slide_link})

Please let me know if you need any further details.

Best regards,
{sender_name}
""".strip()


async def send_report() -> None:
    print("Weekly Telegram Report Sender")
    print("--------------------------------")

    target = ask_text(
        "Send to Telegram target username/group/chat",
        DEFAULT_TARGET,
    )

    recipient_display = ask_text(
        "Recipient display in message",
        "bong @PHYNY_NAN",
    )

    current_month = datetime.now().strftime("%B")
    week_label = ask_text(
        "Week label",
        f"{current_month} W3",
    )

    project_status = ask_text(
        "Project Status",
        "The project is progressing well with multiple enhancements completed. Most modules are stable, with ongoing feature development and improvements.",
    )

    achievements = ask_multiline("Achievements This Sprint")
    next_sprint = ask_multiline("Plan for Next Sprint")

    slide_link = ask_text("Progress slide link")

    sender_name = ask_text("Sender name", DEFAULT_SENDER_NAME)

    image_paths = ask_image_paths()

    message = build_report_message(
        recipient=recipient_display,
        week_label=week_label,
        project_status=project_status,
        achievements=achievements,
        next_sprint=next_sprint,
        slide_link=slide_link,
        sender_name=sender_name,
    )

    print("\nPreview Message")
    print("--------------------------------")
    print(message)
    print("--------------------------------")

    if image_paths:
        print("\nImages:")
        for path in image_paths:
            print(f"- {path}")
    else:
        print("\nImages: none")

    confirm = ask_text("\nSend this report? Type yes to send", "no").lower()

    if confirm != "yes":
        print("Cancelled.")
        return

    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    async with client:
        await client.send_message(
            target,
            message,
            parse_mode="md",
            link_preview=True,
        )

        for image_path in image_paths:
            await client.send_file(target, image_path)

    print("✅ Report sent successfully.")


if __name__ == "__main__":
    asyncio.run(send_report())