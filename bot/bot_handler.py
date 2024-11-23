import os
import schedule
import telepot
import json
from dotenv import load_dotenv
from datetime import datetime
from api_services.api_services import api_request
from api_services.prayer_times import fetch_prayer_times
from utils.utils import is_time_to_run, update_last_run_time
from utils.weather_utils import get_weather
from utils.ffmpeg_utils import capture_video

# Load environment variables from .env file
load_dotenv()

# Initialize bot and environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telepot.Bot(BOT_TOKEN)
GROUP_IDS = json.loads(os.getenv("GROUP_IDS", "[]"))
SPECIAL_ID = os.getenv("SPECIAL_ID")

def handle(msg):
    """Handle incoming messages and commands."""
    chat_id = str(msg["chat"]["id"])
    message_id = msg["message_id"]
    command = msg["text"].lower()

    if chat_id != SPECIAL_ID and chat_id not in GROUP_IDS:
        bot.sendMessage(chat_id, "Dih, siapa lu?", reply_to_message_id=message_id)
        return

    if not command.startswith("/"):
        return

    if not is_time_to_run(chat_id):
        bot.sendMessage(chat_id, "INGFA-INGFO.. BRISIK!!!", reply_to_message_id=message_id)
        return

    # Command Handling
    if command.startswith("/ingfo_atas"):
        handle_ingfo("atas", chat_id, message_id)
    elif command.startswith("/ingfo_bawah"):
        handle_ingfo("bawah", chat_id, message_id)
    elif command.startswith('/ingfov'):
        handle_ingfov(chat_id, message_id)
    elif command.startswith("/jadwal_sholat"):
        handle_prayer_schedule(chat_id, message_id)
    elif command.startswith("/ingfo_cuaca"):
        handle_weather(chat_id, message_id)
    elif command.startswith("/jadwal_berjalan"):
        handle_schedule_list(chat_id, message_id)
    elif command.startswith("/jam_server"):
        handle_server_time(chat_id, message_id)
    else:
        bot.sendMessage(chat_id, "Command tidak dikenali.", reply_to_message_id=message_id)

    if chat_id != SPECIAL_ID:
        update_last_run_time(chat_id)

def handle_ingfo(position, chat_id, message_id):
    """Process '/ingfo_atas' and '/ingfo_bawah' commands."""
    bot.sendMessage(chat_id, f"Ingfo {position} diproses!")
    output_file, person_count = api_request(f"ingfo/{position}")
    bot.sendPhoto(
        chat_id,
        open(output_file, "rb"),
        f"Terpantau BC {position} {person_count} orang gan",
        reply_to_message_id=message_id,
    )
    os.remove(output_file)

def handle_ingfov(chat_id, message_id):
    bot.sendMessage(chat_id, "Ingfo video diproses!")
    output_file = f"videos/ingfov_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
    capture_video(output_file, duration=10, idc=1, ids=1)
    bot.sendVideo(chat_id, open(output_file, 'rb'), caption="Terpantau kondisi BC atas gan", reply_to_message_id=message_id)
    os.remove(output_file)

def handle_prayer_schedule(chat_id, message_id):
    """Fetch and send today's prayer schedule."""
    now = datetime.now()
    prayer_times = fetch_prayer_times(now.day, now.month, now.year)

    if prayer_times:
        message = f"Jadwal sholat waktu Sleman hari ini ({prayer_times['tanggal']}):\n"
        prayer_times.pop("tanggal")
        message += "```\n" + "\n".join(
            [f"{prayer.capitalize()}: {time}" for prayer, time in prayer_times.items()]
        ) + "\n```"
        bot.sendMessage(chat_id, message, reply_to_message_id=message_id, parse_mode="Markdown")
    else:
        bot.sendMessage(chat_id, "Gagal mengambil jadwal sholat.", reply_to_message_id=message_id)

def handle_weather(chat_id, message_id):
    """Fetch and send the current weather."""
    output_file = get_weather()
    if output_file:
        bot.sendPhoto(chat_id, open(output_file, "rb"), "Cek gan", reply_to_message_id=message_id)
    else:
        bot.sendMessage(chat_id, "Gagal mengambil data cuaca.", reply_to_message_id=message_id)

def handle_schedule_list(chat_id, message_id):
    message = "Jadwal berjalan saat ini:\n"
    for job in schedule.jobs:
        message += (
            f"Job: {job.job_func.__name__}\n"
            f"Next run: {job.next_run}\n"
            "-----------\n"
        )
    bot.sendMessage(chat_id, message, reply_to_message_id=message_id)

def handle_server_time(chat_id, message_id):
    server_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot.sendMessage(chat_id, f"Jam server saat ini: {server_time}", reply_to_message_id=message_id)