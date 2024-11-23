import time

INTERVAL = 600
LAST_RUN_TIMES = {}

def is_time_to_run(chat_id):
    """Check if the command can be executed."""
    return time.time() - LAST_RUN_TIMES.get(chat_id, 0) > INTERVAL

def update_last_run_time(chat_id):
    """Update the last run time."""
    LAST_RUN_TIMES[chat_id] = time.time()
