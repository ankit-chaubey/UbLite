import asyncio
import re
from datetime import datetime
from telethon import events
from UbLite.config import client, owner_id, prefixes

async def spam_message(event, n, message, delay=1):
    try:
        for _ in range(n):
            await event.respond(message)
            print(f"Sent: {message} at {datetime.now()}")
            await asyncio.sleep(delay)
    except Exception as e:
        print(f"An error occurred: {e}")

@client.on(events.NewMessage(pattern=r'(' + '|'.join(map(re.escape, prefixes)) + r')spam (\d+) (.+)'))
async def handle_spam_command(event):
    try:
        if event.sender_id != owner_id:
            return
        
        n = int(event.pattern_match.group(2))
        message = event.pattern_match.group(3)
        print(f"Received spam command: {event.text}")
        
        await spam_message(event, n, message)
    except Exception as e:
        print(f"Error: {e}")
        await event.edit("An error occurred while processing your command.")

@client.on(events.NewMessage(pattern=r'(' + '|'.join(map(re.escape, prefixes)) + r')delayspam (\d+) (.+) (\d+)'))
async def handle_delayspam_command(event):
    try:
        if event.sender_id != owner_id and event.sender_id not in auth_users:
            return
        
        n = int(event.pattern_match.group(2))
        message = event.pattern_match.group(3)
        delay = int(event.pattern_match.group(4))
        print(f"Received delayspam command: /delayspam {n} {message} {delay}s")
        
        await spam_message(event, n, message, delay)
    except Exception as e:
        print(f"Error: {e}")
        await event.edit("An error occurred while processing your command.")

@client.on(events.NewMessage(pattern=r'(' + '|'.join(map(re.escape, prefixes)) + r')help spam'))
async def help_spam_command(event):
    try:
        if event.sender_id != owner_id and event.sender_id not in auth_users:
            return  

        help_text = (
            "**.spam** - `spam <number> <message>` (Sends a message multiple times)\n"
            "**.delayspam** - `delayspam <number> <message> <delay>` (Sends a message with a delay)\n"
        )
        await event.edit(help_text)
    except Exception as e:
        print(f"Error: {e}")
        await event.edit("An error occurred while processing your command.")
