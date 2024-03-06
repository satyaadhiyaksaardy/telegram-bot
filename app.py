import telepot
from telepot.loop import MessageLoop
from dotenv import load_dotenv
import os
import time
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Define constants
INTERVAL = 600
GROUP_IDS = os.getenv('GROUP_IDS')
SPECIAL_ID = os.getenv('SPECIAL_ID')  # This ID has no wait interval
LAST_RUN_TIMES = {group_id: time.time() - INTERVAL for group_id in GROUP_IDS}
RTSP_URL = os.getenv('RTSP_URL')

# Initialize the bot
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telepot.Bot(BOT_TOKEN)

def is_time_to_run(chat_id):
    """Check if the command can be executed based on the interval."""
    return time.time() - LAST_RUN_TIMES.get(chat_id, 0) > INTERVAL or chat_id == SPECIAL_ID

def update_last_run_time(chat_id):
    """Update the last run time for a chat_id."""
    if chat_id != SPECIAL_ID:  # Special ID does not need to wait
        LAST_RUN_TIMES[chat_id] = time.time()

def execute_ffmpeg_command(output_file, idc, ids):
    """Execute the FFmpeg command to capture an image or video."""
    cmd = f"ffmpeg -rtsp_transport tcp -y -i '{RTSP_URL}/mode=real&idc={idc}&ids={ids}' -vframes:v 1 {output_file}"
    os.system(cmd)
    return output_file

def handle(msg):
    chat_id = str(msg['chat']['id'])  # Ensure chat_id is a string
    message_id = msg['message_id']
    command = msg['text'].lower()  # Handle commands case-insensitively

    if chat_id in GROUP_IDS:
        if not command.startswith('/'):
            return
        if is_time_to_run(chat_id):
            if command == '/ingfo-atas':
                bot.sendMessage(chat_id, "Ingfo atas diproses!")
                output_file = execute_ffmpeg_command("do.jpg", 1, 1)
                bot.sendPhoto(chat_id, open(output_file, 'rb'), "Terpantau BC atas", reply_to_message_id=message_id)
                os.remove(output_file)
            elif command == '/ingfo-bawah':
                bot.sendMessage(chat_id, "Ingfo bawah diproses!")
                output_file = execute_ffmpeg_command("do2.jpg", 2, 1)
                bot.sendPhoto(chat_id, open(output_file, 'rb'), "Terpantau BC bawah", reply_to_message_id=message_id)
                os.remove(output_file)
            elif command == '/ingfov':
                bot.sendMessage(chat_id, "Ingfo video diproses!")
                output_file = "ingfov.mp4"
                os.system(f"ffmpeg -rtsp_transport tcp -y -i '{RTSP_URL}/mode=real&idc=1&ids=1' -c copy -t 10 {output_file}")
                bot.sendVideo(chat_id, open(output_file, 'rb'), caption="Terpantau kondisi BC atas gan", reply_to_message_id=message_id)
                os.remove(output_file)
            else:
                return  # Ignore other commands
            update_last_run_time(chat_id)
        else:
            bot.sendMessage(chat_id, "INGFA-INGFO.. BRISIK!!!", reply_to_message_id=message_id)
    else:
        bot.sendMessage(chat_id, "Dih, siapa lu?", reply_to_message_id=message_id)

MessageLoop(bot, handle).run_as_thread()
print('Bot is listening...')

while True:
    time.sleep(10)
