from os import environ
import aiohttp
from pyrogram import Client, filters

API_ID = environ.get('API_ID',"24953797")
API_HASH = environ.get('API_HASH',"f5a80bf6f55664689631266f3eb6d1ce")
BOT_TOKEN = environ.get('BOT_TOKEN',"6872448232:AAFNg-v_C5meULRnIxiZCDuiD1-gZywzDqM")
API_KEY = environ.get('API_KEY',"e26eadf7050fc1af0ce5d082d40d78c6c013984c")

bot = Client('sharedisk bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!**\n\n"
        "I'm GPlink bot. Just send me link and get short link")


@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    try:
        short_link = await get_shortlink(link)
        await message.reply(f'Here is your [short link]({short_link})', quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


async def get_shortlink(link):
    url = 'https://sharedisk.in/api'
    params = {'api': API_KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            return data["shortenedUrl"]


bot.run()