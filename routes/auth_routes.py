from flask import Blueprint, request, jsonify, render_template, session, redirect
from models.user_model import UserModel
from ml.face_auth import capture_face_encoding, verify_face
from models.candidate_model import CandidateModel
from ml.behavior_model import (
    extract_behavior_features,
    train_model,
    predict_sample
)

auth_bp = Blueprint("auth", __name__)

# ==========================
# Home Route
# ==========================
@auth_bp.route("/")
def home():
    return render_template("login.html")


# ==========================
# Register Route
# ==========================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    if UserModel.find_by_email(email):
        return jsonify({"error": "User already exists"}), 400

    face_encoding = capture_face_encoding()

    if face_encoding is None:
        return jsonify({"error": "Face not detected"}), 400

    face_encoding = face_encoding.tolist()

    UserModel.create_user(name, email, password, face_encoding)

    return jsonify({"message": "User registered successfully with face"}), 201


# ==========================
# Login Route (EMAIL ONLY)
# ==========================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    hold_times = data.get("holdTimes", [])
    key_intervals = data.get("keyIntervals", [])
    mouse_speeds = data.get("mouseSpeeds", [])

    if not email or not password:
        return jsonify({"error": "Missing credentials"}), 400

    user = UserModel.find_by_email(email)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # 🔹 Password Verification
    if not UserModel.verify_password(user["password_hash"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    # 🔹 Face Verification
    new_encoding = capture_face_encoding()

    if new_encoding is None:
        return jsonify({"error": "Face not detected"}), 400

# Only verify if stored encoding exists
    if user.get("face_encoding"):
        match = verify_face(user["face_encoding"], new_encoding)

        if not match:
            return jsonify({"error": "Face mismatch"}), 403
        
    # 🔹 Behavioral Feature Extraction
    new_features = extract_behavior_features(
        hold_times,
        key_intervals,
        mouse_speeds
    )

    behavior_samples = user.get("behavior_profile", [])

    if len(behavior_samples) >= 2:
        model = train_model(behavior_samples)

        if model:
            prediction, score = predict_sample(model, new_features)

            if prediction == -1:
                return jsonify({
                    "error": "Anomalous behavior detected",
                    "risk_score": score
                }), 403

    # 🔹 Store new behavior sample
    UserModel.add_behavior_sample(user["_id"], new_features)

    # 🔹 SET SESSION
    session["user_id"] = str(user["_id"])
    session["user_email"] = user["email"]
    session["role"] = user.get("role", "voter")
    
    
    if session["role"] == "admin":
        redirect_url = "/dashboard"
    else:
        redirect_url = "/vote-page"

    return jsonify({
        "message": "Login successful",
        "redirect": redirect_url
    }), 200

# ==========================
# Behavior Data Route
# ==========================
@auth_bp.route("/behavior-data", methods=["POST"])
def behavior_data():
    data = request.get_json()

    email = data.get("email")
    hold_times = data.get("holdTimes", [])
    key_intervals = data.get("keyIntervals", [])
    mouse_speeds = data.get("mouseSpeeds", [])

    user = UserModel.find_by_email(email)

    if not user:
        return jsonify({"error": "User not found"}), 404

    features = extract_behavior_features(
        hold_times,
        key_intervals,
        mouse_speeds
    )

    UserModel.add_behavior_sample(user["_id"], features)

    return jsonify({"message": "Behavior profile updated"}), 200


# ==========================
# Logout Route
# ==========================
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login-page")
