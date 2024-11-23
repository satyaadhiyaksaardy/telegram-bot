# **Telegram Prayer Reminder Bot**

A modular and extensible Telegram bot designed to provide users with reminders for prayer times, weather updates, and custom alerts. The bot also integrates with an external API for advanced functionality and supports automated scheduled tasks.

---

## **Features**

- **Daily Prayer Time Notifications**:
  - Automatically fetches prayer times and sends reminders.
  - Includes custom notifications for Sahur and Iftar during Ramadan.

- **Command-Based Responses**:
  - `/jadwal_sholat`: Fetch and display today’s prayer schedule.
  - `/ingfo_atas` and `/ingfo_bawah`: Fetch data from an RTSP stream or API.
  - `/ingfov`: Generate and send a video stream capture.
  - `/ingfo_cuaca`: Fetch weather updates with images.

- **Scheduled Tasks**:
  - Midnight updates for daily reminders.
  - Real-time prayer time notifications using `schedule`.

- **Customizable for Multiple Groups**:
  - The bot supports predefined group chat IDs and special privileges for certain users.

---

## **Technologies Used**

- **Programming Language**: Python 3.9
- **Telegram Library**: [Telepot](https://github.com/nickoala/telepot)
- **Task Scheduling**: [Schedule](https://schedule.readthedocs.io/en/stable/)
- **Environment Management**: [python-dotenv](https://pypi.org/project/python-dotenv/)
- **API Requests**: [Requests](https://pypi.org/project/requests/)
- **RTSP Streaming**: [FFmpeg](https://ffmpeg.org/)
- **Dockerized Deployment**:
  - The project uses Docker for containerization and easy deployment.

---

## **Getting Started**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-repo/telegram-prayer-bot.git
cd telegram-prayer-bot
```

### **2. Set Up Environment Variables**
Create a .env file in the root directory with the following variables:
```bash
BOT_TOKEN=your-telegram-bot-token
GROUP_IDS=["your-predefined-id"]
REMAINDER_IDS=["your-predefined-id-to-remainded"]
SPECIAL_ID=your-super-privileges-id
RTSP_URL=your-rtsp-url
API_INGFO=your-api-ingfo-url
CCTV_TOKEN=your-api-ingfo-token
API_WEATHER=your-api-weather-url
API_PRAYER_TIME=your-api-prayer-url
```

### **3. Install Dependencies**
```bash
pip3 install -r requirements.txt
```

### **4. Run Locally**
Start the bot by running:
```bash
python3 main.py
```

---
## **Using Docker**

### **1. Build the Docker Image**
```bash
docker build -t telegram-prayer-bot .
```

### **2. Run the Docker Container**
```bash
docker-compose up
```

---

## **Commands**

| Command | Description |
| -------- | ------- |
| /jadwal_sholat | Fetch and display today’s prayer schedule. |
| /ingfo_atas | Retrieve data from the RTSP stream (top view). |
| /ingfo_bawah | Retrieve data from the RTSP stream (bottom view). |
| /ingfov | Send a video stream capture. |
| /ingfo_cuaca | Fetch and display weather updates. |
| /jadwal_berjalan | View the currently scheduled tasks. |
| /jam_server | Display the server's current time. |

---

## **Project Structure**

```bash
telegram-prayer-bot/
│
│── api_services/
│   ├
│   ├
│   ├
│
├── bot/
│   ├── __init__.py
│   ├── bot_handler.py       # Handles incoming bot messages
│   ├── reminders.py         # Logic for sending reminders
│
├── scheduler/
│   ├── __init__.py
│   ├── scheduler.py         # Manages scheduled tasks
│
├── utils/
│   ├── __init__.py
│   ├── ffmpeg_utils.py      # Helper functions for time-based operations
│   ├── utils.py             # Helper functions for time-based operations
│   ├── weather_utils.py     # Helper functions for time-based operations
│
├── .env                     # Environment variables
├── app.py                   # Entry point of the bot
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Docker configuration
└── README.md                # Project documentation
├── requirements.txt         # Python dependencies
```

---

## **Extending the Project**

### **1. Add New Commands:**
- Modify `bot/bot_handler.py` and add a handler for your new command.
- Example: Create a new command `/my_command` to send a custom message.

### **2. Integrate Additional APIs:**
- Use the `requests` library in `utils` or `bot` modules for API integrations.

### **3. Schedule More Tasks:**
- Add new jobs to `scheduler/task_scheduler.py`.
