---
name: telegram-weekly-report
description: Generate and preview factual weekly project reports for manual copying into Telegram. Never log in, send messages, or use Telegram API sessions.
---

# Telegram Weekly Report Preview

## Safety

This is a **manual-preview-only** workflow. Never request Telegram login codes, use sessions, run `Telethon`, use Telegram Bot API, or send messages. Do not read private credentials. Follow the repository's project policy and explicit user scope. Do not invent achievements, slide links, progress, or dates.

## Workflow

1. Collect project status, week label, achievements, next sprint plan, progress link, recipient display and sender display from the user or authorized source. Leave genuinely missing information clearly unknown; don't invent it.
2. Prepare a JSON input using `assets_report_input_example.json` as the schema example, replacing every placeholder with verified facts. Keep real personal names or links out of the shared example file.
3. From this skill's directory run `python scripts/generate_weekly_report_preview.py --input /path/to/report.json --output /path/to/output` (local files only).
4. Review the generated preview and the saved `.txt`/`.md` file. List images for **manual** upload only.
5. Deliver the preview for manual copying and explicitly state that **nothing was sent**.

## Input shape

- Required strings: `recipient_display`, `week_label`, `project_status`, `sender_name`.
- Optional string: `slide_link`.
- Optional arrays of strings: `achievements`, `next_sprint`, `images`.

The report uses four sections: Project Status, Achievements This Sprint, Plan for Next Sprint, and Progress Slide. It should not claim a task is done without confirmation.

## Constraints

`generate_weekly_report_preview.py` has no network dependencies. No `login.py`, `send_weekly_report.py`, or Telegram session files are distributed or required. Do not add automatic sending as an incidental change.
