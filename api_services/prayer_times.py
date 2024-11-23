import os
import requests

API_PRAYER_TIME = os.getenv("API_PRAYER_TIME")

def fetch_prayer_times(date, month, year):
    """
    Fetch today's prayer times for a given city and date.
    """
    url = f"{API_PRAYER_TIME}/{year}-{month}-{date}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        return response.json()['data']['jadwal']
    except requests.RequestException as e:
        print(f"Failed to fetch prayer times: {e}")
        return None
