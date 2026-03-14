from flask_pymongo import PyMongo

mongo = PyMongo()

def init_db(app):
    mongo.init_app(app)
    
    # Force database name from env
    import os
    db_name = os.getenv("DB_NAME", "sentinelvoteai_production")
    mongo.db = mongo.cx[db_name]
    