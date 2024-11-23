import os
import requests
from datetime import datetime

API_WEATHER = os.getenv("API_WEATHER")

def get_weather(output_dir="images/"):
    """
    Fetch weather image and save it to a file.
    """
    url = f"{API_WEATHER}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for HTTP codes 4xx/5xx
        output_file = os.path.join(output_dir, f"weather_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, "wb") as file:
            file.write(response.content)  # Save binary content
        return output_file
    except requests.RequestException as e:
        print(f"Failed to fetch weather data: {e}")
        return None
