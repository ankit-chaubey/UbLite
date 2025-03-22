import asyncio
from telethon import events
from UbLite.config import client

HELP_TEXT = """
**📌 UbLite Userbot – Quick Commands**
🚀 Light, Fast, and Smart Automation Bot

🔹 **Basic Commands**
- `.purge <n>` – Delete multiple messages
- `.purgeme <n>` – Delete your own messages
- `.purgeall` – Delete all messages from a user

🔹 **GIF & Sticker Tools**
- `.gif sendall <user>` – Send all saved GIFs
- `.gif deleteall` – Remove all GIFs
- `/clone <sticker_url> <shortname> <packname>` – Clone sticker packs

🔹 **Utilities**
- `.json` – Get message JSON data
- `.t-en नमस्ते` – Translate Hindi to English

📖 **Full Command Guide:** [UbLite Commands](https://github.com/ankit-chaubey/ublite/blob/main/UbLite/readme.md)
"""

@client.on(events.NewMessage(pattern=r"^\.help$", outgoing=True))
async def help(event):
    await event.edit(HELP_TEXT)
