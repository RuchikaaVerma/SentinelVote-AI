FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir dlib-bin
RUN pip install --no-cache-dir face-recognition-models
RUN pip install --no-cache-dir face_recognition --no-deps

COPY requirements.txt .
RUN pip install --no-cache-dir \
    flask \
    flask-pymongo \
    bcrypt \
    python-dotenv \
    numpy \
    scikit-learn \
    cryptography \
    opencv-python \
    certifi

COPY . .
EXPOSE 5000
CMD ["python", "app.py"]