import json
import re
import time
from telethon import events
from UbLite.config import client, owner_id, prefixes, dl_time, error_dl
import asyncio

async def send_json_response(event, message_data):
    try:
        message_json = json.dumps(message_data.to_dict(), default=str, indent=4)
        await event.edit(f"**Replied Message JSON**:\n```\n{message_json}\n```")
    except Exception as e:
        await event.edit(f"Error occurred: {e}")
        print(f"Error in sending JSON: {e}")
        await asyncio.sleep(error_dl)
        await event.delete()

@client.on(events.NewMessage(pattern=r'(' + '|'.join(map(re.escape, prefixes)) + r')json'))
async def handle_json_command(event):
    try:
        if event.sender_id != owner_id:
            return
        
        if event.is_reply:
            replied_message = await event.get_reply_message()
            await send_json_response(event, replied_message)
        else:
            await event.edit("Please reply to a message to get its JSON.")
            await event.delete()
            await asyncio.sleep(dl_time)
            await event.delete()
    except Exception as e:
        await event.edit(f"Error occurred: {e}")
        print(f"Error in .json command: {e}")
        await asyncio.sleep(error_dl)
        await event.delete()
