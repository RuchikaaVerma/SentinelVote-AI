from dotenv import load_dotenv
load_dotenv()

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
import bcrypt

# Connect to MongoDB
uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
db_name = os.getenv("DB_NAME", "sentinelvoteai_production")

if "mongodb+srv" in uri:
    client = MongoClient(uri, tlsAllowInvalidCertificates=True)
else:
    client = MongoClient(uri)

db = client[db_name]

# ── Add Candidates ──────────────────────────
db.candidates.delete_many({})  # clear existing
db.candidates.insert_many([
    {"name": "Alice Johnson", "party": "Progressive Party", "votes": 0, "image": ""},
    {"name": "Bob Smith",     "party": "Unity Alliance",    "votes": 0, "image": ""},
    {"name": "Carol Davis",   "party": "Green Initiative",  "votes": 0, "image": ""},
])
print("✅ Candidates added!")

# ── Add Admin User ──────────────────────────
existing = db.users.find_one({"email": "admin@sentinelvote.ai"})
if not existing:
    hashed = bcrypt.hashpw("Admin@2024".encode(), bcrypt.gensalt())
    db.users.insert_one({
        "name": "Admin",
        "email": "admin@sentinelvote.ai",
        "password_hash": hashed,
        "face_encoding": [],
        "behavior_profile": [],
        "has_voted": False,
        "role": "admin"
    })
    print("✅ Admin user created!")
else:
    db.users.update_one(
        {"email": "admin@sentinelvote.ai"},
        {"$set": {"role": "admin"}}
    )
    print("✅ Admin role updated!")

print("\n��� Done! Login with:")
print("   Email:    admin@sentinelvote.ai")
print("   Password: Admin@2024")
