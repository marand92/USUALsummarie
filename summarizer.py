import os
import json
import datetime
import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TRANSCRIPTS_DIR = "transcripts"
SUMMARIES_DIR = "summaries"

client = OpenAI(api_key=OPENAI_API_KEY)

openai.api_key = OPENAI_API_KEY

def load_transcript(date=None):
    if date is None:
        date = datetime.date.today()

    filename = os.path.join(TRANSCRIPTS_DIR, f"{date.isoformat()}.json")

    if not os.path.exists(filename):
        print(f"No transcript found for {date.isoformat()}")
        return None

    with open(filename, "r", encoding="utf-8") as f:
        messages = json.load(f)

    return messages

def prepare_prompt(messages):
    filtered_messages = [msg for msg in messages if msg['author'] != "Mava"]

    formatted_messages = []
    for msg in filtered_messages:
        formatted_messages.append(f"[{msg['created_at']}] [{msg['author']}]: {msg['content']}")

    prompt = f"""
You are an expert crypto analyst.

You are analyzing today's community discussion around the USUAL token project, a stablecoin-focused token infrastructure.
Focus particularly on your perspective as an **investor and USUALx staking token holder**.

**Your task:**

- Summarize **new relevant developments** and **official announcements**.
- Extract **useful discussions** where:
  - Users suggest improvements
  - Users highlight risks
  - Users critique the project or the team
  - Users propose expectations toward the team
- **Ignore irrelevant trolling, chatter, or messages from the AI agent "Mava".**

For each important point you identify:

1. Provide a **brief summary** of the discussion.
2. Include the **list of usernames** who participated in the discussion.
3. Indicate an approximate **timeframe** when the discussion took place (e.g., "10:00–13:00 UTC").
4. **Evaluate whether the discussion is valuable** for a USUALx token holder to know.
5. **Give your expert opinion** on the topic or the users' perspectives.

Additionally:

- At the end, provide a **General Danger Indicator**:
  - Assess the overall mood of today's chat.
  - Are there major risks, warnings, scandals, rumors, or negative developments worth noting for investors?
  - If so, summarize them clearly.
  - If not, explicitly state that no significant dangers were observed.

**Final Response Format:**

- **Summary Point 1**: [summarized discussion]
  - **Participants**: [usernames]
  - **Approximate Timeframe**: [time period, e.g., 10:00–13:00 UTC]
  - **Usefulness for USUALx Holder**: [yes/no, with a short reason]
  - **Your Opinion**: [short expert commentary]

- **Summary Point 2**: [summarized discussion]
  - **Participants**: [usernames]
  - **Approximate Timeframe**: [time period]
  - **Usefulness for USUALx Holder**: [yes/no]
  - **Your Opinion**: [commentary]

[...]

- **General Danger Indicator**: [summary of overall risks or safety today]

---

Here are today's cleaned and chronologically ordered chat messages:

"""

    prompt += "\n\n" + "\n".join(formatted_messages)

    return prompt

def generate_summary(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional crypto community analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=2000
    )

    return response.choices[0].message.content

def save_summary(summary_text, date=None):
    if date is None:
        date = datetime.date.today()

    os.makedirs(SUMMARIES_DIR, exist_ok=True)

    filename = os.path.join(SUMMARIES_DIR, f"dailyUpdate_{date.isoformat()}.md")

    if os.path.exists(filename):
        print(f"Overwriting existing summary: {filename}")
    else:
        print(f"Saving new summary: {filename}")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(summary_text)

    print(f"Summary saved to {filename}.")

def main():
    messages = load_transcript()
    if not messages:
        return

    prompt = prepare_prompt(messages)
    summary = generate_summary(prompt)

    print("\n===== SUMMARY =====\n")
    print(summary)

    save_summary(summary)

if __name__ == "__main__":
    main()
