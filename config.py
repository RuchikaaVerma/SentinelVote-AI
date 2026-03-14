import os

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/sentivoteai")
    SECRET_KEY = os.getenv("SECRET_KEY", "a32a219889454456c86cf413e2a41f06c39652135c7c66c81a4f8ca89778bae4")
    DB_NAME = os.getenv("DB_NAME", "sentinelvoteai_production")
    FACE_TOLERANCE = float(os.getenv("FACE_TOLERANCE", "0.6"))
    BEHAVIOR_THRESHOLD = float(os.getenv("BEHAVIOR_THRESHOLD", "0.3"))