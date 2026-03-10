from database.db import mongo
from bson.objectid import ObjectId


class CandidateModel:

    @staticmethod
    def create_candidate(name, party):
        candidate = {
            "name": name,
            "party": party,
            "votes": 0
        }
        return mongo.db.candidates.insert_one(candidate)

    @staticmethod
    def get_all():
        candidates = list(mongo.db.candidates.find())

        for candidate in candidates:
            candidate["_id"] = str(candidate["_id"])  # Convert ObjectId to string

        return candidates

    @staticmethod
    def get_by_id(candidate_id):
        return mongo.db.candidates.find_one({
            "_id": ObjectId(candidate_id)
        })

    @staticmethod
    def increment_vote(candidate_id):
        return mongo.db.candidates.update_one(
            {"_id": ObjectId(candidate_id)},
            {"$inc": {"votes": 1}}
        )
