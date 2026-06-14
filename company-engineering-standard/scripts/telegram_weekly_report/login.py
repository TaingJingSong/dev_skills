import os
from telethon import TelegramClient

API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]

SESSION_NAME = "telegram_user_report"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def main():
    me = await client.get_me()
    print(f"Logged in as: {me.first_name} / @{me.username}")

with client:
    client.loop.run_until_complete(main())