import os
import telepot
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the bot with the token
BOT_TOKEN = os.getenv('BOT_TOKEN')
REMAINDER_IDS = json.loads(os.getenv("GROUP_IDS", "[]"))
bot = telepot.Bot(BOT_TOKEN)

def send_reminder(message, reminder_type='text', video_path=None):
    """
    Send a reminder to a predefined set of chat IDs.
    
    Args:
        message (str): The reminder message to be sent.
        reminder_type (str): Type of the reminder ('text' or 'video').
        video_path (str, optional): Path to the video file (if reminder_type is 'video').
    """
    # Define the chat IDs to send the reminder to
    chat_ids = REMAINDER_IDS

    for chat_id in chat_ids:
        if reminder_type == 'text':
            # Send a text message
            bot.sendMessage(chat_id, message)
        elif reminder_type == 'video' and video_path:
            # Send a video message with a caption
            with open(video_path, 'rb') as video_file:
                bot.sendVideo(chat_id, video_file, caption=message)

        else:
            print(f"Invalid reminder type: {reminder_type}")
