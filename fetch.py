import discord
import asyncio
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Start after a today, midnight
START_AFTER_DATE = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
kwargs = {}
kwargs["after"] = START_AFTER_DATE

client = discord.Client(bot=False)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    channel = client.get_channel(CHANNEL_ID)
    if channel:
        messages = []
        async for message in channel.history(limit=100, **kwargs):
            messages.append((message.created_at, message.author.name, message.content))

        for created_at, author, content in messages:
            print(f"[{created_at}] {author}: {content}")
    else:
        print("Channel not found.")

    await client.close()

client.run(TOKEN)  # <<< VERY IMPORTANT: bot=False here
