from database.db import mongo
from datetime import datetime
from bson.objectid import ObjectId
import bcrypt


class UserModel:

    # ==========================
    # CREATE USER
    # ==========================
    @staticmethod
    def create_user(name, email, password, face_encoding=None):
        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        if face_encoding is None:
            face_encoding = []

        user = {
            "name": name,
            "email": email,
            "password_hash": hashed_pw,
            "face_encoding": face_encoding,
            "behavior_profile": [],
            "has_voted": False,
            "role": "voter",   # default role
            "created_at": datetime.utcnow()
        }

        return mongo.db.users.insert_one(user)

    # ==========================
    # FIND USER
    # ==========================
    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def find_by_id(user_id):
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})

    # ==========================
    # UPDATE USER
    # ==========================
    @staticmethod
    def mark_as_voted(user_id):
        return mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"has_voted": True}}
        )

    @staticmethod
    def add_behavior_sample(user_id, features):
        return mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$push": {"behavior_profile": features}}
        )

    # ==========================
    # COUNT USERS (FOR TURNOUT)
    # ==========================
    @staticmethod
    def count_users():
        return mongo.db.users.count_documents({})

    # ==========================
    # PASSWORD VERIFY
    # ==========================
    @staticmethod
    def verify_password(stored_hash, password):
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash)