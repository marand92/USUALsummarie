import datetime
from fetch import run_fetcher
from summarizer import run_summarizer
from emailer import run_emailer

def main():
    print(f"\n🕒 Starting USUAL Summary Bot at {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")

    try:
        print("\n--- Step 1: Fetching messages from Discord ---")
        run_fetcher()

        print("\n--- Step 2: Summarizing today's discussion ---")
        run_summarizer()

        print("\n--- Step 3: Sending summary email ---")
        run_emailer()

        print("\n✅ All tasks completed successfully!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
