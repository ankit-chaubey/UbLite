import asyncio
import logging
from telethon import TelegramClient, events
from UbLite.config import client

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def download_media(message):
    try:
        if message.media:
            result = await message.download_media()
            await client.send_file("me", result, caption="Successfully #SelfDestructive Media Saved By @UbLite")
        else:
            logger.info("No media found in the message.")
    except Exception as e:
        logger.error(f"Error downloading media: {e}")

@client.on(events.NewMessage(func=lambda e: e.is_private and (e.photo or e.video) and e.media_unread))
async def downloader(event):
    await download_media(event)

@client.on(events.NewMessage(func=lambda e: e.is_private and e.is_reply))
async def reply_downloader(event):
    try:
        original_message = await event.get_reply_message()
        if original_message and (original_message.photo or original_message.video):
            await download_media(original_message)
        else:
            logger.info("The original message does not contain media.")
    except Exception as e:
        logger.error(f"Error handling reply: {e}")
