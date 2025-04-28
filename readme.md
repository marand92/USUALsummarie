# USUAL Chat Summarizer Bot

This project automatically fetches daily messages from a Discord community channel about the **USUAL** token project, summarizes the important discussions, and emails the summary in a clean, readable format.

## Features

- 📥 Fetches daily Discord channel discussions
- 🧹 Filters out irrelevant messages (e.g., bot messages)
- ✍️ Summarizes discussions, highlighting:
  - New developments
  - User concerns and suggestions
  - Critiques and improvement proposals
- 📝 Captures **key arguments** raised by users
- 🧠 Adds GPT's own expert analysis after each point
- 📧 Sends daily HTML-formatted email updates
- 🕒 Saves daily transcripts and summaries locally

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/marand92/USUALsummarie.git

2. Set up a Python virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate   # (Linux/Mac)
    venv\Scripts\activate      # (Windows)
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project root with your API keys and SMTP details:

    ```env
    DISCORD_TOKEN=your-discord-token
    CHANNEL_ID=your-discord-channel-id
    OPENAI_API_KEY=your-openai-api-key
    SMTP_USERNAME=your-smtp-username
    SMTP_PASSWORD=your-smtp-password
    SMTP_SERVER=your-smtp-server
    SMTP_PORT=your-smtp-port
    EMAIL_FROM=your-sender-email
    TO_EMAIL=your-destination-email
    ```

5. Run the scripts manually, or later automate them via scheduled tasks (like `cron` or Windows Task Scheduler).

## Project Structure

| Folder / File | Purpose |
|:---|:---|
| `fetcher.py` | Fetches daily Discord messages |
| `summarizer.py` | Summarizes the day's discussion using GPT |
| `emailer.py` | Sends the daily summary by email |
| `transcripts/` | Stores raw daily message logs |
| `summaries/` | Stores generated daily summaries (HTML format) |

## Notes

- Make sure `.env` and `venv/` are excluded via `.gitignore`.
- No sensitive keys are committed to GitHub.
- Summaries are already in HTML format for clean email rendering.

---
