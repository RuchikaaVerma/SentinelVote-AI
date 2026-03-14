from pymongo import MongoClient
import os

class MongoDB:
    db = None

mongo = MongoDB()

def init_db(app):
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/sentinelvoteai_production")
    db_name = os.getenv("DB_NAME", "sentinelvoteai_production")
    
    # Use TLS only for Atlas (cloud), not for localhost
    if "mongodb+srv" in uri:
        client = MongoClient(uri, tlsAllowInvalidCertificates=True)
    else:
        client = MongoClient(uri)
    
    mongo.db = client[db_name]