from flask_pymongo import PyMongo
from pymongo import MongoClient
import os

mongo = PyMongo()

def init_db(app):
    uri = os.getenv("MONGO_URI")
    
    # Direct MongoClient with SSL fix
    client = MongoClient(
        uri,
        tls=True,
        tlsAllowInvalidCertificates=True
    )
    
    db_name = os.getenv("DB_NAME", "sentinelvoteai_production")
    app.db = client[db_name]
    
    # Also init PyMongo for compatibility
    mongo.init_app(app)
    mongo.db = client[db_name]