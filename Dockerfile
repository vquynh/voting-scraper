# Use official Playwright base image
FROM mcr.microsoft.com/playwright:v1.45.0-noble

# Set working directory
WORKDIR /app

# Install Python and Pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv

COPY requirements.txt .
RUN python3 -m venv .venv
RUN . .venv/bin/activate
RUN .venv/bin/pip install -r requirements.txt

# Copy app code
COPY . .

# Expose Flask port
EXPOSE 8080

# Command to run the app
CMD [".venv/bin/gunicorn", "-b", "0.0.0.0:8080", "app:app"]