# Use official Playwright base image
FROM mcr.microsoft.com/playwright:v1.53.0-noble

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN apt-get update
RUN apt install -y python3 python3-pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Flask port
EXPOSE 8080

# Command to run the app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]