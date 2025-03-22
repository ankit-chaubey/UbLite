import asyncio
import logging
from telethon import TelegramClient, events
from UbLite.config import client, prefixes, prefix_pattern
from telethon.errors import FloodWaitError
import asyncio

#@client.on(events.NewMessage(pattern=r'(' + prefix_pattern + r')fwd (\d+) (\d+) (\d+)/sec (-?\d+) (-?\d+)'))

@client.on(events.NewMessage(pattern=r'\*fwd (\d+) (\d+) (\d+)/sec (-?\d+) (-?\d+)'))
async def forward_command_handler(event):
    user = await client.get_me()
    ALLOWED_USER_ID = user.id

    if event.sender_id != ALLOWED_USER_ID:
        return

    try:
        starting_message_id = int(event.pattern_match.group(1))
        last_message_id = int(event.pattern_match.group(2))
        messages_per_sec = int(event.pattern_match.group(3))
        source_channel_id = int(event.pattern_match.group(4))
        destination_channel_id = int(event.pattern_match.group(5))

        delay = 1 / messages_per_sec

        await event.edit(
            f"Starting to forward messages from {source_channel_id} "
            f"(IDs {starting_message_id} to {last_message_id}) to {destination_channel_id} "
            f"at {messages_per_sec} messages per second."
        )

        for message_id in range(starting_message_id, last_message_id + 1):
            try:
                message = await client.get_messages(source_channel_id, ids=message_id)
                if message:
                    await client.send_message(destination_channel_id, message)
                    await asyncio.sleep(delay)
            except FloodWaitError as e:
                print(f"Flood wait triggered. Waiting for {e.seconds} seconds.")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                await event.reply(f"Error with message ID {message_id}: {e}")

        await event.edit("Message forwarding completed.")

    except Exception as e:
        await event.edit(f"An error occurred: {e}")

@client.on(events.NewMessage(pattern=r'(' + prefix_pattern + r')help fwd'))
async def help_fwd_command(event):
    help_text = (
        "Usage: `.fwd <starting_message_id> <last_message_id> <messages_per_sec> <source_channel_id> <destination_channel_id>`\n\n"
        "Example: `*fwd 100 200 5 123456789 987654321`\n"
    )
    await event.edit(help_text)
