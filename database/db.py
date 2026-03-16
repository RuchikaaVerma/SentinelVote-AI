from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

class MongoDB:
    db = None

mongo = MongoDB()

def init_db(app):
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/sentinelvoteai_production")
    db_name = os.getenv("DB_NAME", "sentinelvoteai_production")

    if "mongodb+srv" in uri:
        client = MongoClient(
            uri,
            server_api=ServerApi('1'),
            tlsAllowInvalidCertificates=True,
            tlsAllowInvalidHostnames=True,
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000
        )
    else:
        client = MongoClient(uri)

    mongo.db = client[db_name]