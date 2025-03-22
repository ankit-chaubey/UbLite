from telethon.sync import TelegramClient, events
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetShortName, InputStickerSetItem, InputDocument
from telethon.tl.functions.stickers import AddStickerToSetRequest, CreateStickerSetRequest
import re
from UbLite.config import client

def extract_shortname(url):
    match = re.search(r"https://t.me/addstickers/(\w+)", url)
    if match:
        return match.group(1)
    return None

async def fetch_stickers(source_shortname):
    sticker_set = await client(GetStickerSetRequest(
        stickerset=InputStickerSetShortName(source_shortname),
        hash=0
    ))
    stickers = []
    for doc in sticker_set.documents:
        if doc.mime_type == "video/webm":
            emoji = next(
                (pack.emoticon for pack in sticker_set.packs if doc.id in pack.documents),
                None
            )
            if emoji:
                stickers.append((doc, emoji, 'animated'))
        elif doc.mime_type == "image/webp":
            emoji = next(
                (pack.emoticon for pack in sticker_set.packs if doc.id in pack.documents),
                None
            )
            if emoji:
                stickers.append((doc, emoji, 'static'))
        else:
            emoji = next(
                (pack.emoticon for pack in sticker_set.packs if doc.id in pack.documents),
                None
            )
            if emoji:
                stickers.append((doc, emoji, 'mask'))
    return stickers

async def create_sticker_pack(user, shortname, title, placeholder_sticker, placeholder_emoji, sticker_type):
    sticker_item = InputStickerSetItem(
        document=InputDocument(
            id=placeholder_sticker.id,
            access_hash=placeholder_sticker.access_hash,
            file_reference=placeholder_sticker.file_reference
        ),
        emoji=placeholder_emoji
    )
    await client(CreateStickerSetRequest(
        user_id=user,
        title=title,
        short_name=shortname,
        stickers=[sticker_item]
    ))

async def add_stickers_to_pack(user, shortname, stickers):
    for sticker_file, emoji, sticker_type in stickers:
        await client(AddStickerToSetRequest(
            stickerset=InputStickerSetShortName(shortname),
            sticker=InputStickerSetItem(
                document=InputDocument(
                    id=sticker_file.id,
                    access_hash=sticker_file.access_hash,
                    file_reference=sticker_file.file_reference
                ),
                emoji=emoji
            )
        ))
        print(f"Added sticker with emoji '{emoji}' to the '{shortname}' pack. Sticker type: {sticker_type}.")

@client.on(events.NewMessage(pattern=r"\*clone (https://t\.me/addstickers/\w+) (\w+) (.+)", outgoing=True))
async def clone_sticker(event):
    user = await client.get_me()
    ALLOWED_USER_ID = user.id

    if event.sender_id != ALLOWED_USER_ID:
        return

    try:
        source_url, shortname, title = event.pattern_match.groups()
        source_shortname = extract_shortname(source_url)
        if not source_shortname:
            await event.edit("Invalid sticker set URL.")
            return

        stickers = await fetch_stickers(source_shortname)
        if not stickers:
            await event.edit(f"No stickers found in the source pack '{source_shortname}'.")
            return

        await event.edit("Pack creation in progress. Please wait...")
        placeholder_sticker, placeholder_emoji, sticker_type = stickers[0]
        await create_sticker_pack(user, shortname, title, placeholder_sticker, placeholder_emoji, sticker_type)
        await add_stickers_to_pack(user, shortname, stickers)

        await event.edit(
            f"Sticker pack cloned successfully! You can now use your pack: {title}. Access it here: https://t.me/addstickers/{shortname}"
        )

    except Exception as e:
        await event.edit(f"An error occurred: {e}")

@client.on(events.NewMessage(pattern=r"\*add (\w+)", outgoing=True))
async def add_sticker_to_pack(event):
    user = await client.get_me()
    ALLOWED_USER_ID = user.id

    if event.sender_id != ALLOWED_USER_ID:
        return

    if not event.reply_to_msg_id:
        await event.edit("Please reply to a sticker or video sticker to add it to the pack.")
        return

    try:
        shortname = event.pattern_match.group(1)
        reply_message = await event.get_reply_message()
        sticker = reply_message.sticker

        if not sticker:
            await event.edit("Please reply to a sticker or video sticker.")
            return

        emoji = sticker.emoji if hasattr(sticker, 'emoji') and sticker.emoji else "👍"
        sticker_type = "static" if sticker.mime_type == "image/webp" else "animated" if "video" not in sticker.mime_type else "video"

        await add_stickers_to_pack(user, shortname, [(sticker, emoji, sticker_type)])
        print(f"Sticker added: Emoji: '{emoji}', Pack: '{shortname}', Sticker type: '{sticker_type}'.")

        await event.edit(f"Added sticker with emoji '{emoji}' to your pack  https://t.me/addstickers/{shortname}")

    except Exception as e:
        await event.edit(f"An error occurred: {e}")
