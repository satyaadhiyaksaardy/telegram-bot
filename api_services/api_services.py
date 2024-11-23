import requests
import base64
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_INGFO = os.getenv("API_INGFO")
CCTV_TOKEN = os.getenv('CCTV_TOKEN')

def api_request(url_path):
    """Make an API request and decode image."""
    response = requests.get(f"{API_INGFO}/{url_path}",headers= {"Authorization": f"{CCTV_TOKEN}"})
    if response.status_code == 200:
        img_data = response.json()["image"]
        person_count = response.json()["count"]
        output_file = save_image(img_data)
        return output_file, person_count
    return None, 0

def save_image(img_data):
    """Save image from base64 data."""
    img = base64.b64decode(img_data)
    output_file = f"images/{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "wb") as file:
        file.write(img)
    return output_file
