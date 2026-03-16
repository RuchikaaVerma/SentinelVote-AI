from pymongo import MongoClient
import os
import certifi

class MongoDB:
    db = None

mongo = MongoDB()

def init_db(app):
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/sentinelvoteai_production")
    db_name = os.getenv("DB_NAME", "sentinelvoteai_production")

    if "mongodb+srv" in uri:
        client = MongoClient(
            uri,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=30000
        )
    else:
        client = MongoClient(uri)

    mongo.db = client[db_name]