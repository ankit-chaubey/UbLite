import logging
import re
from telethon import TelegramClient, events, functions, types
from telethon.errors import UsernameNotOccupiedError, PeerIdInvalidError
from UbLite.config import client, owner_id, prefixes, dl_time, error_dl  # Import dl_time and error_dl
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_success(event, message, delete_after=True):
    success_msg = await event.respond(message)
    if delete_after:
        await asyncio.sleep(dl_time)
        await success_msg.delete()

async def send_error(event, message, delete_after=True):
    error_msg = await event.respond(message)
    if delete_after:
        await asyncio.sleep(error_dl)
        await error_msg.delete()

async def send_all_gifs(event, recipient_id):
    try:
        recipient_entity = await client.get_entity(
            int(recipient_id) if recipient_id.isdigit() else recipient_id
        )
    except (UsernameNotOccupiedError, PeerIdInvalidError):
        await send_error(event, "The provided recipient does not exist.")
        logger.error("Invalid recipient for sending GIFs.")
        return

    result = await client(functions.messages.GetSavedGifsRequest(hash=0))
    if isinstance(result, types.messages.SavedGifs) and result.gifs:
        await send_success(event, f"Sending {len(result.gifs)} saved GIF(s) to {recipient_id}...")
        for i, gif in enumerate(result.gifs, start=1):
            await client.send_file(recipient_entity, gif)
            logger.info(f"Sent GIF {i} of {len(result.gifs)} to {recipient_id}")
        await send_success(event, "All saved GIFs have been sent.")
    else:
        await send_error(event, "No saved GIFs found.")
        logger.warning("No saved GIFs to send.")

async def delete_all_gifs(event):
    result = await client(functions.messages.GetSavedGifsRequest(hash=0))
    if isinstance(result, types.messages.SavedGifs) and result.gifs:
        await send_success(event, f"Deleting {len(result.gifs)} saved GIF(s) from saved GIFs...")
        for i, gif in enumerate(result.gifs, start=1):
            await client(functions.messages.SaveGifRequest(id=gif, unsave=True))
            logger.info(f"Deleted GIF {i} of {len(result.gifs)} from saved GIFs.")
        await send_success(event, "All saved GIFs have been deleted.")
    else:
        await send_error(event, "No saved GIFs found to delete.")
        logger.warning("No saved GIFs to delete.")

async def add_all_gifs(event, target_chat_id):
    try:
        target_entity = await client.get_entity(
            int(target_chat_id) if target_chat_id.isdigit() else target_chat_id
        )
    except (UsernameNotOccupiedError, PeerIdInvalidError):
        await send_error(event, "The target chat does not exist.")
        logger.error("Invalid target chat for adding GIFs.")
        return

    gif_count = 0
    async for message in client.iter_messages(target_entity, filter=types.InputMessagesFilterGif):
        if message.media:
            await client(functions.messages.SaveGifRequest(id=message.media.document, unsave=False))
            gif_count += 1
            logger.info(f"Saved a GIF from {target_chat_id} to saved GIFs.")

    if gif_count > 0:
        await send_success(event, f"Saved {gif_count} GIF(s) from {target_chat_id} to saved GIFs.")
    else:
        await send_error(event, "No GIFs found in the target chat.")
        logger.warning("No GIFs found in the target chat to add.")

async def show_help(event):
    help_text = (
        "**GIF Bot Commands**\n\n"
        "1. **.gif sendall <@username or chat_id>**\n"
        "   Sends all saved GIFs to the specified username or chat ID.\n\n"
        "2. **.gif deleteall**\n"
        "   Deletes all GIFs currently saved in your saved GIFs.\n\n"
        "3. **.gif addall <@username or chat_id>**\n"
        "   Adds all GIFs from the specified chat to your saved GIFs.\n\n"
        "4. **.gif help**\n"
        "   Shows this help message with all available commands."
    )
    await send_success(event, help_text, delete_after=False)
    logger.info("Displayed help message.")

async def is_authorized(event):
    return event.sender_id == owner_id

@client.on(events.NewMessage(pattern=r'(' + '|'.join(map(re.escape, prefixes)) + r')gif sendall (.+)'))
async def handle_sendall(event):
    if not await is_authorized(event):
        return
    recipient = event.pattern_match.group(2).strip()
    # Delete the command message
    await event.delete()
    await send_all_gifs(event, recipient)

@client.on(events.NewMessage(pattern=r'(' + '|'.join(map(re.escape, prefixes)) + r')gif deleteall'))
async def handle_deleteall(event):
    if not await is_authorized(event):
        return
    await event.delete()
    await delete_all_gifs(event)

@client.on(events.NewMessage(pattern=r'(' + '|'.join(map(re.escape, prefixes)) + r')gif addall (.+)'))
async def handle_addall(event):
    if not await is_authorized(event):
        return
    target_chat = event.pattern_match.group(2).strip()
    await event.delete()
    await add_all_gifs(event, target_chat)

@client.on(events.NewMessage(pattern=r'(' + '|'.join(map(re.escape, prefixes)) + r')help gif'))
async def handle_help(event):
    if not await is_authorized(event):
        return
    await event.delete()
    await show_help(event)
