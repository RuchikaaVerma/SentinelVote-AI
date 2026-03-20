# 🛡️ SentinelVote AI
### AI-Secured Smart Voting System with Multi-Layer Security

<div align="center">

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.0-green.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0-green.svg)](https://www.mongodb.com/)
[![dlib](https://img.shields.io/badge/dlib-19.24-orange.svg)](http://dlib.net/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.0-red.svg)](https://scikit-learn.org/)

**[▶️ Watch Demo](https://drive.google.com/file/d/1_CgyXHfT_jjlcqKMHMJHmdpZV6EAGoWX/view?usp=sharingg) · [📂 GitHub Repo](https://github.com/RuchikaaVerma/SentinelVote-AI) ·

---

> *"What if digital elections could be more secure than physical ones?"*

SentinelVote AI is a next-generation electronic voting platform that combines **facial recognition**, **behavioral AI**, and **blockchain audit trails** to create a tamper-proof, transparent, and trustworthy voting system.

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🎯 Problem Statement](#-problem-statement)
- [🔐 Security Layers](#-security-layers)
- [🏗️ System Architecture](#️-system-architecture)
- [📸 User Journey](#-user-journey)
- [🛠️ Tech Stack](#️-tech-stack)
- [📁 Project Structure](#-project-structure)
- [⚙️ Installation](#️-installation)
- [🚀 Running the App](#-running-the-app)
- [🧪 Testing](#-testing)
- [👥 Team](#-team)
- [🗺️ Roadmap](#️-roadmap)

---

## ✨ Features

### Core
| Feature | Description |
|---|---|
| 🔐 **Multi-Factor Auth** | Password + face verification + behavioral biometrics |
| 🤖 **AI Fraud Detection** | Isolation Forest ML — real-time risk scoring (0–1) |
| ⛓️ **Blockchain Audit** | SHA-256 hashed, immutable, tamper-proof vote records |
| 📊 **Live Dashboard** | Real-time vote counts, turnout analytics, security events |
| 🛡️ **Security Analytics** | Face mismatch logs, login attempts, anomaly alerts |

### Advanced
- ✅ **Double vote prevention** — one vote per registered user, enforced at DB level
- ✅ **Secure session management** — Flask sessions with 1-hour timeout
- ✅ **Responsive design** — mobile-first, works on all devices
- ✅ **Role-based access** — Voter vs Admin permissions
- ✅ **Full audit logging** — complete trail of all system events

---

## 🎯 Problem Statement

Traditional e-voting systems face five critical challenges:

| Problem | Impact |
|---|---|
| 🚨 **Identity Fraud** | Fake voters, stolen credentials |
| 🔁 **Multiple Voting** | Same user votes more than once |
| ⚠️ **Insider Tampering** | Database manipulation by admins |
| 📋 **No Transparency** | Black-box systems, no public audit |
| 🕵️ **Behavioral Attacks** | Bots, automated voting scripts |

> Only **37% of users trust** digital voting systems globally *(Pew Research, 2023)*

---

## 🔐 Security Layers

SentinelVote AI uses **5 stacked security layers** — fraud is detected *before* it happens:

```
┌─────────────────────────────────────────────────────┐
│  Layer 5  ⛓️  Blockchain Audit     Tamper-proof      │
│  Layer 4  🔒  Vote Lock            No double voting  │
│  Layer 3  🤖  Behavioral AI        Anomaly detection │
│  Layer 2  👤  Face Recognition     Biometric check   │
│  Layer 1  🔑  Password             bcrypt hash       │
└─────────────────────────────────────────────────────┘
```

### Layer 1 — Password Authentication
- **Technology:** bcrypt (cost factor 12)
- **Validation:** Min 8 chars · uppercase · lowercase · digit · special char
- **Protection against:** Rainbow tables, brute-force attacks

### Layer 2 — Face Recognition
- **Technology:** dlib + face_recognition library
- **Process:** Capture at registration → extract 128-D encoding → compare at login (tolerance 0.6)
- **Protection against:** Impersonation, stolen credentials

```python
# Registration — extract face encoding
face_encoding = face_recognition.face_encodings(image)[0]  # 128-D vector

# Login — compare faces
distance = face_recognition.face_distance([stored_encoding], live_encoding)[0]
match = distance < 0.6   # tolerance threshold
confidence = (1 - distance) * 100
```

### Layer 3 — Behavioral AI
- **Model:** Isolation Forest (scikit-learn)
- **Tracked features:** Keystroke dynamics · mouse trajectory · login timing · device fingerprint
- **Output:** Risk score 0–1 (block if score > 0.3)

```python
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(normal_behaviour_data)

score = model.decision_function([user_features])[0]
risk  = 1 / (1 + np.exp(score))      # normalize to 0–1
# block user if risk > 0.3
```

### Layer 4 — Vote Lock
- **Mechanism:** DB constraint + session check
- **Protection against:** Double voting

```python
if db.votes.find_one({"user_id": user_id, "election_id": election_id}):
    return jsonify({"error": "Already voted"}), 403
```

### Layer 5 — Blockchain Audit
- **Algorithm:** SHA-256 cryptographic hashing
- **Each block contains:** vote hash · timestamp · previous block hash · encrypted user ref
- **Protection against:** Vote tampering, result manipulation

```python
import hashlib, json

def add_vote(self, vote_data):
    block = {
        "block_id":  len(self.chain),
        "timestamp": datetime.now().isoformat(),
        "data":      vote_data,
        "prev_hash": self.chain[-1]["hash"]
    }
    block["hash"] = hashlib.sha256(
        json.dumps(block, sort_keys=True).encode()
    ).hexdigest()
    self.chain.append(block)
    return block
```

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        BROWSER (UI)                           │
│   HTML5 · TailwindCSS · Chart.js · Webcam API · behavior.js  │
└───────────────────────┬──────────────────────────────────────┘
                        │ HTTP / REST
┌───────────────────────▼──────────────────────────────────────┐
│                    FLASK BACKEND                              │
│  auth_routes.py   vote_routes.py   admin_routes.py           │
│       │                │                 │                    │
│  face_auth.py    behavior_model.py    audit.py               │
│  (dlib / 128-D)  (Isolation Forest)   (SHA-256 chain)        │
└───────────────────────┬──────────────────────────────────────┘
                        │ PyMongo
┌───────────────────────▼──────────────────────────────────────┐
│                    MONGODB                                    │
│   users · votes · audit_chain · sessions                     │
└──────────────────────────────────────────────────────────────┘
```

### Data Flow — Casting a Vote

```
Enter Credentials
      │
      ▼
Password Check ──FAIL──▶ Access Denied
      │ PASS
      ▼
Face Verification ──FAIL──▶ Access Denied
      │ PASS
      ▼
Behavioral AI Score ──HIGH RISK──▶ Access Denied
      │ LOW RISK
      ▼
Already Voted? ──YES──▶ Blocked
      │ NO
      ▼
Store Vote → SHA-256 Hash → Append Blockchain Block
      │
      ▼
Show Confirmation + Update Live Results
```

---

## 📸 User Journey

```mermaid
graph TD
    A[Visit Homepage] --> B[Register]
    B --> C[Fill Form]
    C --> D[Capture Face via Webcam]
    D --> E[Submit Registration]
    E --> F[Login Page]
    F --> G[Enter Password]
    G --> H[Face Verification]
    H --> I{Face Match?}
    I -->|No| J[Access Denied]
    I -->|Yes| K[Behavioral Analysis]
    K --> L{Risk Score under 0.3?}
    L -->|No| J
    L -->|Yes| M[Vote Page]
    M --> N[Select Candidate]
    N --> O[Confirm Vote]
    O --> P[Generate Blockchain Hash]
    P --> Q[Vote Recorded]
    Q --> R[View Results Dashboard]
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|---|---|---|
| Python | 3.11+ | Core language |
| Flask | 2.3.0 | Web framework |
| MongoDB | 6.0 | NoSQL database |
| PyMongo | 4.5.0 | MongoDB driver |
| bcrypt | 4.0.1 | Password hashing |

### AI / ML
| Technology | Version | Purpose |
|---|---|---|
| dlib | 19.24.0 | Face detection |
| face_recognition | 1.3.0 | Face encoding + comparison |
| scikit-learn | 1.3.0 | Isolation Forest model |
| NumPy | 1.24.0 | Numerical operations |

### Frontend
| Technology | Version | Purpose |
|---|---|---|
| HTML5 / CSS3 / JS | — | Structure and styling |
| TailwindCSS | 3.3.0 | Utility-first CSS |
| Chart.js | 4.4.0 | Live data charts |

### Security
| Technology | Purpose |
|---|---|
| SHA-256 | Blockchain hashing |
| Flask Sessions | Secure session management |
| CORS Protection | Cross-origin request security |

---

## 📁 Project Structure

```
SentinelVote-AI/
├── app.py                     # Application entry point
├── config.py                  # Configuration settings
│
├── routes/
│   ├── auth_routes.py         # /register  /login  /logout
│   ├── vote_routes.py         # /vote-page  /cast-vote
│   └── admin_routes.py        # /dashboard  /results
│
├── models/
│   ├── user_model.py          # User schema + operations
│   ├── vote_model.py          # Vote schema + operations
│   └── candidate_model.py     # Candidate schema
│
├── ml/
│   ├── face_auth.py           # Face recognition logic
│   └── behavior_model.py      # Isolation Forest model
│
├── database/
│   └── db.py                  # MongoDB connection
│
├── security/
│   └── audit.py               # Blockchain implementation
│
├── templates/
│   ├── register.html
│   ├── login.html
│   ├── vote.html
│   ├── results.html
│   ├── dashboard.html
│   └── confirmation.html
│
├── static/
│   ├── js/
│   │   ├── behavior.js        # Keystroke + mouse tracking
│   │   ├── face-capture.js    # Webcam integration
│   │   └── charts.js          # Chart.js configs
│   └── css/
│       └── style.css
│
├── scripts/
│   └── seed_data.py           # Load demo candidates + admin user
│
├── .env.example
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.11+
- MongoDB 6.0 (or [MongoDB Atlas](https://www.mongodb.com/atlas))
- Git
- Webcam (for face recognition)

### Step 1 — Clone the repo
```bash
git clone https://github.com/RuchikaaVerma/SentinelVote-AI.git
cd SentinelVote-AI
```

### Step 2 — Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

> **dlib not installing?** Try the precompiled wheel:
> ```bash
> pip install dlib-bin
> ```

### Step 4 — Configure environment
```bash
cp .env.example .env
```

Edit `.env`:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/sentinelvote
DB_NAME=sentinelvoteai_production

BCRYPT_LOG_ROUNDS=12
SESSION_TIMEOUT=3600
FACE_TOLERANCE=0.6
BEHAVIOR_THRESHOLD=0.3
```

### Step 5 — Seed the database
```bash
python scripts/seed_data.py
```
Creates 3 demo candidates and 1 admin user. **Admin credentials are printed to terminal — save them.**

---

## 🚀 Running the App

```bash
python app.py
```

Open **http://localhost:5000** in your browser.

| Route | Description |
|---|---|
| `/` | Login page |
| `/register-page` | Voter registration |
| `/vote-page` | Cast your vote |
| `/results-page` | Live election results |
| `/dashboard` | Admin dashboard |

### Docker (optional)
```bash
docker compose up --build
```

---

## 🧪 Testing

```bash
pytest tests/ -v
```

### Manual Checklist
- [ ] Register a new voter with face capture
- [ ] Login with correct credentials + matching face
- [ ] Login with wrong face → should be denied
- [ ] Login with wrong password → should be denied
- [ ] Cast a vote successfully
- [ ] Attempt to vote twice → should be blocked
- [ ] View live results and blockchain audit trail
- [ ] Access admin dashboard with admin account

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Register new voter |
| POST | `/login` | Authenticate voter |
| GET | `/vote-page` | Load voting interface |
| POST | `/cast-vote` | Submit vote |
| GET | `/results-page` | Fetch live results |
| GET | `/dashboard` | Admin dashboard |
| GET | `/logout` | End session |

---

## 👥 Team

| Name | Role | LinkedIn |
|---|---|---|
| **Ruchika Verma** | Full Stack · AI/ML Lead | [Profile](https://www.linkedin.com/in/ruchika-verma-888bb6309) |
| **Divyanshi Singh** | Backend Engineer | [Profile](https://linkedin.com/in/member2) |
| **Archana Agahari** | Frontend · UI/UX | [Profile](https://linkedin.com/in/member3) |
| **Rashmi** | Security Engineer | [Profile](https://linkedin.com/in/member4) |

---

## 🗺️ Roadmap

### Phase 1 — In Progress
- [ ] WebAuthn integration (passwordless login)
- [ ] Mobile app (iOS + Android)
- [ ] Multi-language support
- [ ] WCAG 2.1 AA accessibility

### Phase 2
- [ ] WebSocket real-time vote updates
- [ ] Advanced analytics dashboard
- [ ] Load testing for 1M+ concurrent users

### Phase 3
- [ ] Distributed blockchain network
- [ ] Smart contracts for vote validation
- [ ] National ID system integration

---

<div align="center">

**Made with ❤️ by the SentinelVote AI Team**

*"Security is not optional in democracy. It's fundamental."*

[⬆ Back to Top](#️-sentinelvote-ai)

</div>
