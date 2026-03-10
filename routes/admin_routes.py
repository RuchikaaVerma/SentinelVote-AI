from flask import Blueprint, jsonify
from database.db import mongo
from models.candidate_model import CandidateModel

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/data")
def admin_data():

    total_users = mongo.db.users.count_documents({})
    total_votes = mongo.db.votes.count_documents({})
    candidates = CandidateModel.get_all()

    return jsonify({
        "total_users": total_users,
        "total_votes": total_votes,
        "total_candidates": len(candidates),
        "candidates": candidates
    })
