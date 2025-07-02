# Start from the official Selenium Chrome image
FROM selenium/standalone-chrome:latest

# Set working directory
WORKDIR /app

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3-pip

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port used by Flask
EXPOSE 8080

# Command to run the app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]