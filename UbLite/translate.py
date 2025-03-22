from telethon import TelegramClient, events
from googletrans import Translator
import requests
from UbLite.config import client

API_KEY = 'GOOGLE_API_KEY'
CSE_ID = 'SEARCH_ENGINE_ID'
translator = Translator()

@client.on(events.NewMessage(pattern=r'\.t-([a-z]{2,5}) (.+)', outgoing=True))
async def autodetect_and_translate(event):
    target_lang = event.pattern_match.group(1)
    text = event.pattern_match.group(2)
    translated = await translator.translate(text, src='auto', dest=target_lang)
    await event.edit(f"{translated.text}")

@client.on(events.NewMessage(pattern=r'\.t-([a-z]{2,5}):([a-z]{2,5}) (.+)', outgoing=True))
async def translate_with_source(event):
    source_lang = event.pattern_match.group(1)
    target_lang = event.pattern_match.group(2)
    text = event.pattern_match.group(3)

    full_text = '\n'.join(event.raw_text.splitlines()[1:])
    translated = await translator.translate(full_text, src=source_lang, dest=target_lang)
    await event.edit(f"{translated.text}")

def google_search(query, num_results):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CSE_ID}"
    response = requests.get(url)
    results = response.json().get("items", [])
    if results:
        return "\n".join([f"{item['title']}: {item['link']}" for item in results[:num_results]])
    return "No results found."

@client.on(events.NewMessage(pattern=r'\.g (\d+) (.+)', outgoing=True))
async def google_search_command(event):
    try:
        message = event.text.split('\n')
        first_line = message[0]
        num_results, query_start = first_line.split(' ', 2)[1:]
        query = " ".join([query_start] + message[1:])
        num_results = int(num_results)
        search_results = google_search(query, num_results)
        await event.edit(f"Google Search Results for '{query}':\n{search_results}")
    except Exception as e:
        await event.edit(f"Error: {e}")
