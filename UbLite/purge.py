import asyncio
from telethon import TelegramClient, events
from UbLite.config import client

async def eor(event, message, time=5):
    sent = await event.edit(message)
    await asyncio.sleep(time)
    await sent.delete()

@client.on(events.NewMessage(pattern=r"^\*purge( (.*)|$)", outgoing=True))
async def purge(event):
    match = event.pattern_match.group(2)
    if not event.reply_to_msg_id and not match:
        return await eor(event, "__Reply to a message or use `*purge <number>`!__")

    try:
        count = int(match) if match else None
    except ValueError:
        return await eor(event, "__Invalid number!__")

    deleted = 0
    async for msg in client.iter_messages(
        event.chat_id,
        limit=count,
        min_id=event.reply_to_msg_id if event.reply_to_msg_id else None,
    ):
        await msg.delete()
        deleted += 1

    await eor(event, f"__Purged {deleted} messages.__")

@client.on(events.NewMessage(pattern=r"^\*purgeme( (.*)|$)", outgoing=True))
async def purgeme(event):
    count = event.pattern_match.group(2)
    if not count and not event.reply_to_msg_id:
        return await eor(event, "__Reply to a message or use `*purgeme <number>`!__")

    deleted = 0
    if count:
        try:
            count = int(count)
        except ValueError:
            return await eor(event, "__Invalid number!__")
        async for msg in client.iter_messages(
            event.chat_id, limit=count, from_user="me"
        ):
            await msg.delete()
            deleted += 1
    else:
        async for msg in client.iter_messages(
            event.chat_id, from_user="me", min_id=event.reply_to_msg_id
        ):
            await msg.delete()
            deleted += 1

    await eor(event, f"__Purged {deleted} messages.__")

@client.on(events.NewMessage(pattern=r"^\*purgeall$", outgoing=True))
async def purgeall(event):
    if not event.reply_to_msg_id:
        return await eor(event, "__Reply to a user's message to purge all their messages!__")

    reply = await event.get_reply_message()
    try:
        deleted = 0
        async for msg in client.iter_messages(event.chat_id, from_user=reply.sender_id):
            await msg.delete()
            deleted += 1
        await eor(event, f"__Purged all messages from `{reply.sender.first_name}`.__")
    except Exception as err:
        await eor(event, f"__Error: {err}__")