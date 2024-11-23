import os
import time
import telepot
from dotenv import load_dotenv
from telepot.loop import MessageLoop
from datetime import datetime
from bot.bot_handler import handle
from scheduler.scheduler import initialize_scheduler

# Load environment variables
load_dotenv()

# Initialize constants
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telepot.Bot(BOT_TOKEN)

def start_bot():
    """Start the Telegram bot and the scheduler."""
    initialize_scheduler()
    MessageLoop(bot, handle).run_as_thread()
    print("Bot is listening...")

    while True:
        time.sleep(10)

if __name__ == "__main__":
    start_bot()
