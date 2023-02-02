# bot.py
import discord
import os
import re
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents = intents)
guild = discord.Guild
messages =  []

def is_blockable(message):
    if len(message) < 25:
        return False
    regex = re.compile('[^a-zA-Z]')
    if len(regex.sub('', message)) == 25:
        return True
    return False

print("Bot started")
@client.event
async def on_message(message):
    if is_blockable(message.content):
        emoji = "🟧"
        await message.add_reaction(emoji)
    
client.run(TOKEN)