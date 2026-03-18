FROM python:3.11-slim

# Only runtime libs needed — no build tools
RUN apt-get update && apt-get install -y \
    libopenblas0 \
    liblapack3 \
    libx11-6 \
    libglib2.0-0 \
    libgl1 \
    ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dlib-bin FIRST (precompiled, no cmake, no RAM spike)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir dlib-bin

# Install rest of dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["python", "app.py"]