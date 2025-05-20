# Use an official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements (if you have one)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set environment variables (optional defaults)
ENV TELEGRAM_TOKEN=""
ENV NOTION_TASKER_DB_ID=""
ENV NOTION_IDEAS_DB_ID=""
ENV NOTION_DATABASE_ID=""

# Run the application
CMD ["python", "python_telegram_notion_bot/main.py"]
