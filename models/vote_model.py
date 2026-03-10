from database.db import mongo
from bson.objectid import ObjectId
from datetime import datetime
import hashlib


class VoteModel:

    # ====================================
    # CHECK IF USER ALREADY VOTED
    # ====================================
    @staticmethod
    def has_user_voted(user_id):
        return mongo.db.votes.find_one({
            "user_id": ObjectId(user_id)
        }) is not None


    # ====================================
    # CREATE BASIC VOTE (Optional)
    # ====================================
    @staticmethod
    def create_vote(user_id, candidate_id):
        vote = {
            "user_id": ObjectId(user_id),
            "candidate_id": ObjectId(candidate_id),
            "timestamp": datetime.utcnow()
        }

        return mongo.db.votes.insert_one(vote)


    # ====================================
    # CREATE VOTE WITH AUDIT HASH
    # ====================================
    @staticmethod
    def create_vote_with_audit(user_id, candidate_id):

        now = datetime.utcnow()

        raw_string = f"{user_id}-{candidate_id}-{now.isoformat()}"
        audit_hash = hashlib.sha256(raw_string.encode()).hexdigest()

        vote_record = {
            "user_id": ObjectId(user_id),
            "candidate_id": ObjectId(candidate_id),
            "timestamp": now,   # MUST be datetime
            "audit_hash": audit_hash
        }

        mongo.db.votes.insert_one(vote_record)

        return audit_hash, now.isoformat()


    # ====================================
    # COUNT TOTAL VOTES
    # ====================================
    @staticmethod
    def count_votes():
        return mongo.db.votes.count_documents({})


    # ====================================
    # VOTE TREND BY HOUR (SAFE VERSION)
    # ====================================
    @staticmethod
    def votes_by_hour():

        # If no votes exist → return empty safely
        if mongo.db.votes.count_documents({}) == 0:
            return []

        pipeline = [
            {
                "$match": {
                    "timestamp": { "$type": "date" }
                }
            },
            {
                "$group": {
                    "_id": { "$hour": "$timestamp" },
                    "count": { "$sum": 1 }
                }
            },
            {
                "$sort": { "_id": 1 }
            }
        ]

        result = list(mongo.db.votes.aggregate(pipeline))

        formatted = [
            {
                "hour": item["_id"],
                "count": item["count"]
            }
            for item in result
        ]

        return formatted