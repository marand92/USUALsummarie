import discord
import asyncio
import datetime
from dotenv import load_dotenv
import os
import random
import json

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Start after today's midnight
START_AFTER_DATE = datetime.datetime.combine(datetime.date.today(), datetime.time.min)

client = discord.Client(bot=False)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        print("Channel not found.")
        await client.close()
        return

    print(f"Fetching messages from {channel.name} since {START_AFTER_DATE}")

    all_messages = []
    last_message = None

    while True:
        kwargs = {"after": START_AFTER_DATE}
        if last_message:
            kwargs["after"] = last_message.created_at  # Start after the last fetched message

        batch = []
        async for message in channel.history(limit=100, **kwargs):
            batch.append(message)

        if not batch:
            break  # No more messages to fetch

        all_messages.extend(batch)
        last_message = batch[-1]  # Update the last message to fetch next batch after it

        # Realistic human-like scrolling pause
        delay = max(13, min(104, random.normalvariate(30, 10)))  # Clamp between 13 and 104 seconds
        print(f"Waiting {delay:.1f} seconds before fetching more messages...")
        await asyncio.sleep(delay)


    print(f"Fetched {len(all_messages)} messages.")

    # Print messages
    for message in all_messages:
        print(f"[{message.created_at}] {message.author.name}: {message.content}")

    # Directory where daily transcripts will be saved
    SAVE_DIR = "transcripts"

    # Ensure the directory exists
    os.makedirs(SAVE_DIR, exist_ok=True)

    # Generate filename based on today's date
    today_str = datetime.date.today().isoformat()  # e.g., '2025-04-27'
    filename = os.path.join(SAVE_DIR, f"{today_str}.json")

    # Check if the file already exists
    if os.path.exists(filename):
        print(f"Overwriting existing transcript: {filename}")
    else:
        print(f"Saving new transcript: {filename}")

    # Save messages into the file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            [
                {
                    "created_at": message.created_at.isoformat(),
                    "author": message.author.name,
                    "content": message.content
                }
                for message in all_messages
            ],
            f,
            ensure_ascii=False,
            indent=4
        )

    print(f"Messages saved to {filename}.")

    await client.close()

client.run(TOKEN)
