# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (required for dlib/face_recognition)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install prebuilt dlib (IMPORTANT)
RUN pip install --no-cache-dir dlib-bin

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn (production server)
RUN pip install gunicorn

# Copy all project files
COPY . .

# Run app using Gunicorn (Railway auto uses $PORT)
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]