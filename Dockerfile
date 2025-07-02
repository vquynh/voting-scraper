# Use Ubuntu base image
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common wget curl gnupg libgl1 libglib2.0-0 ffmpeg xvfb fonts-liberation libasound2 libappindicator3-1 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdbus-1-3 libpangocairo-1.0-0 libgtk-3-0

# Install Python
RUN apt-get install -y python3 python3-pip

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install-deps chromium
RUN playwright install chromium

# Copy app code
COPY . .

# Expose Flask port
EXPOSE 8080

# Command to run the app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]