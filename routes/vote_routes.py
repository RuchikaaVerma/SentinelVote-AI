from flask import Blueprint, request, jsonify, render_template, redirect, session
from models.vote_model import VoteModel
from models.user_model import UserModel
from models.candidate_model import CandidateModel

vote_bp = Blueprint("vote", __name__)


# ==============================
# HELPER — serialize MongoDB docs
# ==============================
def serialize(doc):
    """Convert ObjectId _id to string so Jinja2 tojson works."""
    if doc is None:
        return doc
    d = dict(doc)
    if "_id" in d:
        d["_id"] = str(d["_id"])
    return d


# ==============================
# CAST VOTE (API)
# ==============================
@vote_bp.route("/vote", methods=["POST"])
def cast_vote():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    candidate_id = data.get("candidate_id")

    if not candidate_id:
        return jsonify({"error": "Missing candidate ID"}), 400

    user_id = session["user_id"]
    user = UserModel.find_by_id(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if VoteModel.has_user_voted(user["_id"]):
        return jsonify({
            "error": "User already voted",
            "redirect": "/results-page"
        }), 403

    CandidateModel.increment_vote(candidate_id)

    audit_hash, timestamp = VoteModel.create_vote_with_audit(
        user["_id"], candidate_id
    )

    UserModel.mark_as_voted(user["_id"])

    return jsonify({
        "message": "Vote cast successfully",
        "audit_hash": audit_hash,
        "timestamp": timestamp,
        "redirect": "/confirmation-page"
    }), 200


# ==============================
# Vote Page (UI)
# ==============================
@vote_bp.route("/vote-page")
def vote_page():

    if "user_id" not in session:
        return redirect("/login-page")

    candidates = CandidateModel.get_all()
    for c in candidates:
        c["votes"] = None
        c["_id"] = str(c["_id"])   # serialize ObjectId
    return render_template("vote.html", candidates=candidates)


# ==============================
# Results Page
# ==============================
@vote_bp.route("/results-page")
def results_page():

    if "user_id" not in session:
        return redirect("/login-page")

    # Get candidates and serialize _id → string (CRITICAL for tojson)
    raw_candidates = CandidateModel.get_all()
    candidates = []
    for c in raw_candidates:
        candidates.append({
            "_id":   str(c["_id"]),
            "name":  c.get("name", "Unknown"),
            "party": c.get("party", ""),
            "votes": int(c.get("votes", 0))
        })

    # Sort descending by votes
    candidates = sorted(candidates, key=lambda x: x["votes"], reverse=True)

    # Totals
    total_votes = sum(c["votes"] for c in candidates)
    total_users = UserModel.count_users()

    # Turnout
    turnout = 0
    if total_users > 0:
        turnout = round((total_votes / total_users) * 100, 2)

    # Vote share
    vote_share = []
    for c in candidates:
        share = round((c["votes"] / total_votes) * 100, 2) if total_votes > 0 else 0
        vote_share.append({
            "name":  c["name"],
            "votes": c["votes"],
            "share": share
        })

    # Vote trend — live from MongoDB
    # VoteModel.votes_by_hour() should return: [{"_id": hour_int, "count": n}, ...]
    vote_trend = VoteModel.votes_by_hour()
    # Serialize any ObjectId in trend data too (just in case)
    vote_trend = [
        {"_id": int(d.get("_id", 0)), "count": int(d.get("count", 0))}
        for d in (vote_trend or [])
    ]
    
    
    return render_template(
        "results.html",
        candidates=candidates,
        total_votes=total_votes,
        total_users=total_users,
        turnout=turnout,
        vote_share=vote_share,
        vote_trend=vote_trend,
        election_date="May 1, 2026",
        election_status="Active"
    )


# ==============================
# Confirmation Page
# ==============================
@vote_bp.route("/confirmation-page")
def confirmation_page():

    if "user_id" not in session:
        return redirect("/login-page")

    audit_hash = request.args.get("hash")
    timestamp  = request.args.get("time")

    return render_template(
        "confirmation.html",
        audit_hash=audit_hash,
        timestamp=timestamp
    )