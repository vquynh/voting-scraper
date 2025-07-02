# Use a stable Ubuntu base image
FROM ubuntu:22.04

# Set environment to avoid interactive prompts during package install
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install Python + pip
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3 python3-pip

# Install required dependencies for Chrome and Selenium
RUN apt-get install -y wget gnupg libglib2.0-0 libsm6 libxrender1 libxext6 ffmpeg xvfb

# Download and install Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb  && \
    dpkg -i google-chrome-stable_current_amd64.deb || apt-get -f install -y

# Install Chromedriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver

# Set working directory
WORKDIR /app

# Copy requirements.txt first to leverage layer caching
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Flask port
EXPOSE 8080

# Command to run the app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]