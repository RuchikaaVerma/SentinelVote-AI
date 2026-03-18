FROM python:3.11-slim

RUN pip install --upgrade pip && \
    pip install --no-cache-dir dlib-bin

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["python", "app.py"]