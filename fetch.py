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

class FetchClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

        channel = self.get_channel(CHANNEL_ID)
        if not channel:
            print("Channel not found.")
            await self.close()
            return

        print(f"Fetching messages from {channel.name} since {START_AFTER_DATE}")

        all_messages = []
        last_message = None

        while True:
            kwargs = {"after": START_AFTER_DATE}
            if last_message:
                kwargs["after"] = last_message.created_at

            batch = []
            async for message in channel.history(limit=100, **kwargs):
                batch.append(message)

            if not batch:
                break

            all_messages.extend(batch)
            last_message = batch[-1]

            delay = max(13, min(104, random.normalvariate(30, 10)))
            print(f"Waiting {delay:.1f} seconds before fetching more messages...")
            await asyncio.sleep(delay)

        print(f"Fetched {len(all_messages)} messages.")

        # Save messages
        SAVE_DIR = "transcripts"
        os.makedirs(SAVE_DIR, exist_ok=True)
        today_str = datetime.date.today().isoformat()
        filename = os.path.join(SAVE_DIR, f"{today_str}.json")

        if os.path.exists(filename):
            print(f"Overwriting existing transcript: {filename}")
        else:
            print(f"Saving new transcript: {filename}")

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

        await self.close()

def run_fetcher():
    client = FetchClient()   # <<< No intents needed for your discord.py version
    client.run(TOKEN)

if __name__ == "__main__":
    run_fetcher()
