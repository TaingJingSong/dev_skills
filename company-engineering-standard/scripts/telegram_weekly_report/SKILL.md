# Telegram Weekly Report Skill

## Purpose

Use this skill when the user wants to generate a weekly Telegram project report message.

This skill is designed for **manual Telegram sending**. It must generate, preview, and save the report only. It must not send messages automatically.

## Core Principle

The assistant prepares the report.  
The user manually reviews, copies, and sends it in Telegram.

## Safety Rules

The assistant must follow these rules strictly:

- Do not log in to Telegram as the user.
- Do not use Telethon to send messages.
- Do not use Telegram Bot API to send messages.
- Do not ask for Telegram login codes.
- Do not ask for Telegram API ID or API hash.
- Do not send Telegram messages automatically.
- Do not run any script that sends messages.
- Do not modify or use any `.session` file.
- The final report must always be previewed for manual copy/paste.
- Image attachments must be listed separately for manual upload.

## Required Inputs

Ask the user for these inputs:

1. Achievements This Sprint
2. Plan for Next Sprint
3. Progress Slide Link
4. Image Attachment Paths, optional

## Optional Inputs

Ask only when missing, unclear, or requested by the user:

- Recipient display name
- Week label
- Project status
- Sender name

## Default Values

Use these defaults unless the user overrides them:

| Field | Default Value |
|---|---|
| Recipient display | `bong @PHYNY_NAN` |
| Sender name | `Taing ChingSong` |
| Project status | `The project is progressing well with multiple enhancements completed. Most modules are stable, with ongoing feature development and improvements.` |
| Image attachments | Empty list |

## Required Report Format

The generated report must follow this format:

```txt
Dear bong @PHYNY_NAN,

I hope you are doing well.

Please find below the weekly update for <Week Label>:

1. Project Status
<Project Status>

2. Achievements This Sprint:

• <Achievement 1>
• <Achievement 2>

3. Plan for Next Sprint

• <Plan 1>
• <Plan 2>

4. Progress Slide
You can view the detailed progress here:
project progress (<Slide Link>)

Please let me know if you need any further details.

Best regards,
Taing ChingSong
```

## Workflow

When this skill is selected, follow this workflow:

1. Ask the user for the required inputs:

   * Achievements This Sprint
   * Plan for Next Sprint
   * Progress Slide Link
   * Image Attachment Paths, optional

2. Use defaults for optional values unless the user provides custom values.

3. Generate this file:

```txt
~/.openclaw/scripts/telegram_user_report/report_input.json
```

4. Run preview-only script:

```bash
python3 ~/.openclaw/scripts/telegram_user_report/generate_weekly_report_preview.py
```

5. Show the generated report preview to the user.

6. Show image attachment paths separately, if provided.

7. Tell the user to manually copy/paste the report into Telegram and manually upload the listed images.

## Validation Rules

Before generating the report, validate:

* `Achievements This Sprint` must contain at least one item.
* `Plan for Next Sprint` must contain at least one item.
* `Progress Slide Link` must not be empty.
* `Progress Slide Link` should start with `http://` or `https://`.
* Image attachments are optional.
* If image paths are provided and shell access is available, validate that each file exists.
* If an image path does not exist, warn the user and exclude it from the final attachment list unless the user asks to keep it.

## Output Rules

The assistant must output:

1. A clean Telegram-ready report message.
2. A separate image attachment list, if images are provided.
3. The saved output file path.
4. A clear note that the message was **not sent automatically**.

## Report Input JSON Schema

Generate `report_input.json` using this structure:

```json
{
  "recipient_display": "bong @PHYNY_NAN",
  "week_label": "May W3",
  "project_status": "The project is progressing well with multiple enhancements completed. Most modules are stable, with ongoing feature development and improvements.",
  "achievements": [
    "Addressing UAT Feedback (Testing & Fixing) 🟢",
    "Release Preparation 🟢"
  ],
  "next_sprint": [
    "Migrate to New Backend Core 🔵",
    "Implement Multi Shift/Roster Shift 🟠"
  ],
  "slide_link": "https://example.com/progress-slide",
  "sender_name": "Taing ChingSong",
  "images": []
}
```

## Preview Script

The skill expects this preview-only script to exist:

```txt
~/.openclaw/scripts/telegram_user_report/generate_weekly_report_preview.py
```

The script must only:

* Read `report_input.json`
* Generate formatted report text
* Print preview in terminal
* Save `.txt` and `.md` report output
* Never send Telegram messages

## Example User Command

The user can trigger this skill with:

```txt
Use telegram-weekly-report skill.

Generate my weekly Telegram report preview only.
Do not send it automatically.

Ask me for:
1. Achievements This Sprint
2. Plan for Next Sprint
3. Progress Slide link
4. Image attachment paths
```

## Example Assistant Behavior

The assistant should ask:

```txt
Please provide Achievements This Sprint.
Enter one item per line.
```

Then:

```txt
Please provide Plan for Next Sprint.
Enter one item per line.
```

Then:

```txt
Please provide the Progress Slide link.
```

Then:

```txt
Please provide image attachment paths, or type "none".
```

After collecting inputs, the assistant generates and previews the report.

## Prohibited Actions

Never run these actions from this skill:

```bash
python3 send_weekly_report_from_file.py
python3 send_report.py
python3 telegram_sender.py
```

Never use:

```txt
Telethon send_message
Telethon send_file
Telegram Bot API sendMessage
Telegram Bot API sendPhoto
Telegram Bot API sendMediaGroup
```

## Final Response Requirement

After generating the report, the assistant must clearly say:

```txt
This report was generated and previewed only. It was not sent to Telegram automatically.
Please copy/paste the message into Telegram manually and upload the listed images manually.
```

```

You can save it here:

```bash
mkdir -p ~/.openclaw/skills/telegram-weekly-report
nano ~/.openclaw/skills/telegram-weekly-report/SKILL.md
```