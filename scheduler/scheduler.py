import schedule
import time
from datetime import datetime, timedelta
from api_services.prayer_times import fetch_prayer_times
from bot.reminders import send_reminder

def refresh_daily_reminders():
    """
    Fetch today's prayer times and schedule reminders.
    """
    now = datetime.now()
    prayer_times = fetch_prayer_times(now.day, now.month, now.year)
    if prayer_times:
        schedule_reminders_for_day(prayer_times)
    else:
        print("Failed to refresh daily reminders. Prayer times could not be fetched.")

def schedule_reminders_for_day(prayer_times):
    """
    Schedule reminders for prayer times based on the fetched schedule.
    Clears previous reminders to prevent duplication.
    """
    # Clear existing prayer reminders to prevent duplicates
    schedule.clear('prayer-reminders')
    schedule.clear('sahur-reminder')
    schedule.clear('breaking-reminder')

    # Schedule sahur reminder (1 hour before Imsak)
    imsak_time = datetime.strptime(prayer_times['imsak'], '%H:%M') - timedelta(hours=1)
    schedule.every().day.at(imsak_time.strftime('%H:%M')).do(
        send_reminder,
        message="Poro sederek, wancinipun sahur! Semoga lancar puasanya hari ini.",
        reminder_type="video",
        video_path="assets/sahur.mp4"
    ).tag('sahur-reminder')

    # Schedule reminders for each prayer time
    for prayer, time in prayer_times.items():
        if prayer in ['imsak', 'subuh', 'dzuhur', 'ashar', 'maghrib', 'isya']:
            schedule.every().day.at(time).do(
                send_reminder,
                message=f"Saatnya {prayer.capitalize()}! Jangan lupa untuk berdoa.",
                reminder_type="text"
            ).tag('prayer-reminders')

    # Schedule breaking fast reminder (1 hour before Maghrib)
    maghrib_time = datetime.strptime(prayer_times['maghrib'], '%H:%M') - timedelta(hours=1)
    schedule.every().day.at(maghrib_time.strftime('%H:%M')).do(
        send_reminder,
        message="Sebentar lagi waktunya berbuka. Siapkan makanan dan doa terbaik!",
        reminder_type="video",
        video_path="assets/buka.mp4"
    ).tag('breaking-reminder')

def initialize_scheduler():
    """
    Initialize the scheduler by setting up daily tasks.
    """
    # Schedule a daily refresh of reminders at midnight
    schedule.every().day.at("00:01").do(refresh_daily_reminders).tag('daily-refresh')

    # Run an initial refresh to set up today's reminders
    refresh_daily_reminders()
