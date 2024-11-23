# Use an official Python runtime as a parent image, based on Alpine
FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies required for building certain Python packages
RUN apk add --no-cache \
    tzdata \
    ffmpeg

# Install Python packages from requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Set time zone to UTC+7 Jakarta
ENV TZ=Asia/Jakarta

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Run bot.py when the container launches
CMD ["python", "./app.py"]
