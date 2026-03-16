# 🛡️ SentinelVote AI

**AI-Secured Smart Voting System with Multi-Layer Security**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.0-green.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0-green.svg)](https://www.mongodb.com/)

> **What if digital elections could be more secure than physical ones?**

SentinelVote AI is a next-generation electronic voting platform that combines **facial recognition**, **behavioral AI**, and **blockchain audit trails** to create a tamper-proof, transparent, and trustworthy voting system.

---

## 📋 Table of Contents

- [🌟 Features](#-features)
- [🎯 Problem Statement](#-problem-statement)
- [💡 Our Solution](#-our-solution)
- [🏗️ System Architecture](#️-system-architecture)
- [🔐 Security Layers](#-security-layers)
- [🛠️ Tech Stack](#️-tech-stack)
- [📁 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#️-installation--setup)
- [🚀 Getting Started](#-getting-started)
- [📸 User Journey](#-user-journey)
- [🔬 How It Works](#-how-it-works)
- [🧪 Testing](#-testing)
- [🤝 Contributing](#-contributing)
- [👥 Team](#-team)

---

## 🌟 Features

### ✨ **Core Features**

- **🔐 Multi-Factor Authentication**
  - Password-based login
  - Real-time face verification using dlib
  - Behavioral biometrics (keystroke dynamics, mouse patterns)

- **🤖 AI-Powered Fraud Detection**
  - Isolation Forest ML model for anomaly detection
  - Real-time risk scoring (0-1 scale)
  - Automatic blocking of suspicious activity

- **⛓️ Blockchain Audit Trail**
  - SHA-256 cryptographic hashing
  - Immutable vote records
  - Tamper-proof verification
  - Real-time chain integrity checks

- **📊 Live Results Dashboard**
  - Real-time vote counting
  - Interactive charts (Chart.js)
  - Voter turnout analytics
  - Security event monitoring

- **🛡️ Security Analytics**
  - Face mismatch tracking
  - Login attempt monitoring
  - Behavioral anomaly alerts
  - System health dashboard

### 🚀 **Advanced Features**

- **Double Vote Prevention** — One vote per registered user
- **Session Management** — Secure Flask sessions with timeout
- **Responsive Design** — Mobile-first UI (works on all devices)
- **Real-Time Updates** — Live vote counts without refresh
- **Audit Logging** — Complete trail of all system events
- **Role-Based Access** — Voter vs Admin permissions

---

## 🎯 Problem Statement

### The Trust Crisis in Digital Voting

Traditional e-voting systems face critical challenges:

| Problem | Impact |
|---------|--------|
| 🚨 **Identity Fraud** | Fake voters, stolen credentials |
| 🔁 **Multiple Voting** | Same user votes multiple times |
| ⚠️ **Insider Tampering** | Database manipulation by admins |
| 📋 **No Transparency** | Black-box systems, no public audit |
| 🕵️ **Behavioral Attacks** | Bots, automated voting scripts |

**Result:** Only **37% trust** in digital voting systems globally (Source: Pew Research 2023)

---

## 💡 Our Solution

### Multi-Layer AI + Biometrics + Blockchain

SentinelVote AI addresses these challenges through **5 security layers**:

```
Layer 5: Blockchain Audit ⛓️ (Tamper-proof records)
Layer 4: Vote Lock 🔒 (Prevent double voting)
Layer 3: Behavioral AI 🤖 (Detect suspicious patterns)
Layer 2: Face Recognition 👤 (Biometric verification)
Layer 1: Password 🔑 (Traditional authentication)
```

**Key Innovation:** We detect fraud **BEFORE** it happens, not after.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│  (HTML/CSS/JS + TailwindCSS + Chart.js)                    │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                     FLASK BACKEND                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Routes     │  │  Security    │  │  Blockchain  │     │
│  │  /register   │  │  face_auth   │  │  audit.py    │     │
│  │  /login      │  │  behavior    │  │  SHA-256     │     │
│  │  /vote       │  │  ML model    │  │  hashing     │     │
│  │  /dashboard  │  │  IsoForest   │  │              │     │
│  │  /results    │  └──────────────┘  └──────────────┘     │
│  └──────────────┘                                           │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      MONGODB DATABASE                        │
│  Collections: users, votes, audit_chain, sessions           │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow: Vote Casting

```
User Action → Login → Face Capture → Behavioral Analysis → Risk Score
                                                                ↓
                                                         Score < 0.3?
                                                                ↓
                                                              YES
                                                                ↓
                                     Vote Stored → Generate Hash → Blockchain
                                                                ↓
                                                    Update Dashboard → Results
```

---

## 🔐 Security Layers

### Layer 1: Password Authentication
- **Technology:** bcrypt hashing (cost factor: 12)
- **Protection:** Rainbow table attacks, brute force
- **Validation:** Min 8 chars, uppercase, lowercase, number, special char

### Layer 2: Face Recognition
- **Technology:** dlib + face_recognition library
- **Process:**
  1. Capture face during registration
  2. Extract 128-dimensional face encoding
  3. Compare at login (tolerance: 0.6)
  4. Block if mismatch detected
- **Protection:** Impersonation, stolen credentials

### Layer 3: Behavioral AI
- **Model:** Isolation Forest (sklearn)
- **Features Tracked:**
  - Keystroke dynamics (hold times, intervals)
  - Mouse movement patterns (speed, trajectory)
  - Login time patterns
  - Device fingerprint
- **Output:** Risk score (0 = normal, 1 = anomaly)
- **Threshold:** Block if score > 0.3

### Layer 4: Vote Lock
- **Mechanism:** Database constraint + session check
- **Protection:** Double voting prevention
- **Verification:**
  ```python
  if db.votes.find_one({"user_id": user_id, "election_id": election_id}):
      return "Already voted"
  ```

### Layer 5: Blockchain Audit
- **Algorithm:** SHA-256 cryptographic hashing
- **Chain Structure:**
  ```json
  {
    "block_id": 1,
    "timestamp": "2024-12-15T14:23:01",
    "vote_hash": "d4f7e8a9b2c1...",
    "prev_hash": "a3f5d7c9e1b2...",
    "user_ref": "encrypted_id"
  }
  ```
- **Verification:** Each block contains hash of previous block
- **Protection:** Vote tampering, result manipulation

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Core language |
| **Flask** | 2.3.0 | Web framework |
| **MongoDB** | 6.0 | Database (NoSQL) |
| **PyMongo** | 4.5.0 | MongoDB driver |
| **bcrypt** | 4.0.1 | Password hashing |

### AI/ML
| Technology | Version | Purpose |
|------------|---------|---------|
| **dlib** | 19.24.0 | Face detection |
| **face_recognition** | 1.3.0 | Face encoding/comparison |
| **scikit-learn** | 1.3.0 | Isolation Forest model |
| **NumPy** | 1.24.0 | Numerical operations |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **HTML5/CSS3** | - | Structure & styling |
| **JavaScript (ES6)** | - | Interactivity |
| **TailwindCSS** | 3.3.0 | Utility-first CSS |
| **Chart.js** | 4.4.0 | Data visualization |

### Security
| Technology | Purpose |
|------------|---------|
| **SHA-256** | Blockchain hashing |
| **RSA-2048** | Future encryption (planned) |
| **Flask Sessions** | Secure session management |
| **CORS Protection** | Cross-origin security |

### Development
| Tool | Purpose |
|------|---------|
| **Git** | Version control |
| **VS Code** | IDE |
| **Postman** | API testing |
| **MongoDB Compass** | Database GUI |

---

## 📁 Project Structure
Demo Vedio-https://drive.google.com/file/d/1Y-2H1yvLYgqMUU-CQWmSPDcPJX9LZdVR/view?usp=sharing

```
SentinelVote-AI/
│
├── app.py                          # Main application file
├── config.py                       # App configuration
├── run.py                          # Application entry point
│
├── 📂 routes/
│   ├── auth_routes.py              # /register, /login, /logout
│   ├── vote_routes.py              # /vote-page, /cast-vote
│   └── admin_routes.py             # /dashboard, /results
│
├── 📂 models/
│   ├── user_model.py               # User schema/operations
│   ├── vote_model.py               # Vote schema/operations
│   └── candidate_model.py          # Candidate schema/operations
│
├── 📂 ml/
│   ├── face_auth.py                # Face recognition logic
│   └── behavior_model.py           # Isolation Forest model
│
├── 📂 database/
│   └── db.py                       # MongoDB connection
│
├── 📂 security/
│   └── security.py                 # Security helpers
│
├── 📂 templates/
│   ├── register.html               # Voter registration
│   ├── login.html                  # Login with face capture
│   ├── dashboard.html              # Admin dashboard
│   ├── vote.html                   # Voting interface
│   ├── results.html                # Election results
│   └── confirmation.html           # Vote confirmation
│
├── 📂 static/
│   ├── 📂 css/
│   │   └── style.css               # Custom styles
│   ├── 📂 js/
│   │   ├── behavior.js             # Behavioral tracking
│   │   ├── face-capture.js         # Webcam integration
│   │   └── charts.js               # Chart.js configs
│   └── 📂 face_encodings/          # Stored face data (gitignored)
│
├── 📂 scripts/
│   └── seed_data.py                # Load demo candidates + admin user
│
├── 📂 docs/
│   ├── ARCHITECTURE.md             # System design
│   ├── API.md                      # API documentation
│   └── SECURITY.md                 # Security audit
│
├── .env.example                    # Environment variables template
├── .env                            # Local config (gitignored)
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker container config
├── docker-compose.yml              # Multi-service Docker setup
└── README.md                       # This file
```

---

## ⚙️ Installation & Setup

### Prerequisites

Ensure you have the following installed:

- **Python** 3.11 or higher ([Download](https://www.python.org/downloads/))
- **MongoDB** 6.0 or higher — or use [MongoDB Atlas](https://www.mongodb.com/atlas) (recommended)
- **Git** ([Download](https://git-scm.com/downloads))
- **Webcam** (for face recognition)

### Step 1: Clone the Repository

```bash
git clone https://github.com/RuchikaaVerma/SentinelVote-AI.git
cd SentinelVote-AI
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** If `dlib` installation fails, use the precompiled version:
> ```bash
> pip install dlib-bin
> ```

### Step 4: Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/sentinelvoteai_production?retryWrites=true&w=majority&appName=Cluster0
DB_NAME=sentinelvoteai_production

BCRYPT_LOG_ROUNDS=12
SESSION_TIMEOUT=3600
FACE_TOLERANCE=0.6
BEHAVIOR_THRESHOLD=0.3

UPLOAD_FOLDER=static/face_encodings
MAX_FILE_SIZE=5242880
```

### Step 5: Seed the Database

Run the seed script to create candidates and the admin user:

```bash
python scripts/seed_data.py
```

This creates:
- 3 demo election candidates
- 1 admin user account

> **Admin credentials are printed to terminal on first run.** Keep them secure.

### Step 6: Run the App

```bash
python app.py
```

Open your browser at:
```
http://localhost:5000
```

---

## 🐳 Docker Deployment

### Quick Start

```bash
# Build and run all services
docker compose up --build

# Run in background
docker compose up -d --build
```

### Production Deployment (Railway / Oracle Cloud)

1. Push your code to GitHub
2. Connect repo to [Railway](https://railway.app)
3. Add environment variables in Railway dashboard
4. Railway auto-deploys from your Dockerfile

**Required environment variables for production:**
```
FLASK_ENV=production
SECRET_KEY=<strong-random-key>
MONGO_URI=<your-atlas-uri>
DB_NAME=sentinelvoteai_production
FACE_TOLERANCE=0.6
BEHAVIOR_THRESHOLD=0.3
```

---

## 🚀 Getting Started

### Access the Application

| Route | Description |
|-------|-------------|
| `/` | Login page |
| `/register-page` | New voter registration |
| `/vote-page` | Cast your vote |
| `/results-page` | Live election results |
| `/dashboard` | Admin dashboard (admin role required) |

---

## 📸 User Journey

### Complete Flow: Registration → Voting → Results

```mermaid
graph TD
    A[Visit Homepage] --> B[Click Register]
    B --> C[Fill Registration Form]
    C --> D[Capture Face Photo]
    D --> E[Submit Registration]
    E --> F[Redirect to Login]
    F --> G[Enter Credentials]
    G --> H[Face Verification]
    H --> I{Face Match?}
    I -->|Yes| J[Behavioral Analysis]
    I -->|No| K[Access Denied]
    J --> L{Risk Score < 0.3?}
    L -->|Yes| M[Vote Page]
    L -->|No| K
    M --> N[Select Candidate]
    N --> O[Confirm Vote]
    O --> P[Generate Blockchain Hash]
    P --> Q[Vote Recorded]
    Q --> R[View Confirmation]
    R --> S[Check Results Dashboard]
```

---

## 🔬 How It Works

### Face Recognition Pipeline

```python
# Registration — extract face encoding
def register_face(image):
    face_locations = face_recognition.face_locations(image)
    face_encoding = face_recognition.face_encodings(image, face_locations)[0]
    return face_encoding  # 128-dimensional vector

# Login — compare faces
def verify_face(stored_encoding, login_image):
    current_encoding = face_recognition.face_encodings(login_image)[0]
    distance = face_recognition.face_distance([stored_encoding], current_encoding)[0]
    match = distance < 0.6
    confidence = (1 - distance) * 100
    return {"match": match, "confidence": confidence}
```

### Behavioral AI Model

```python
from sklearn.ensemble import IsolationForest

def train_model(normal_data):
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(normal_data)
    return model

def predict_sample(model, features):
    score = model.decision_function([features])[0]
    normalized = 1 / (1 + np.exp(score))
    return (-1 if normalized > 0.3 else 1), normalized
```

### Blockchain Implementation

```python
import hashlib, json
from datetime import datetime

class VoteBlockchain:
    def calculate_hash(self, block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    def add_vote(self, vote_data):
        new_block = {
            "block_id": len(self.chain),
            "timestamp": datetime.now().isoformat(),
            "data": vote_data,
            "prev_hash": self.chain[-1]["hash"]
        }
        new_block["hash"] = self.calculate_hash(new_block)
        self.chain.append(new_block)
        return new_block
```

---

## 🧪 Testing

### Run Tests

```bash
pytest tests/ -v
```

### Manual Testing Checklist

- [ ] Register a new voter with face capture
- [ ] Login with correct credentials + matching face
- [ ] Login with wrong face (should fail)
- [ ] Login with wrong password (should fail)
- [ ] Cast a vote successfully
- [ ] Attempt double voting (should be blocked)
- [ ] View live results and blockchain audit
- [ ] Admin dashboard access with admin account
- [ ] Session timeout after 1 hour

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register new voter |
| POST | `/login` | Authenticate voter |
| GET | `/vote-page` | Load voting interface |
| POST | `/cast-vote` | Submit vote |
| GET | `/results-page` | Fetch live results |
| GET | `/dashboard` | Admin dashboard |
| GET | `/logout` | End session |

---

### Production Checklist

- [ ] `SECRET_KEY` set to cryptographically secure random string
- [ ] `FLASK_ENV=production`
- [ ] MongoDB Atlas connected with valid URI
- [ ] HTTPS enabled (SSL certificate)
- [ ] Firewall rules configured
- [ ] `seed_data.py` run against production database
- [ ] Face encodings volume persisted (Docker)
- [ ] Rate limiting active (Nginx config)

---

## 🤝 Contributing

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write unit tests for new features
- Update documentation
- Add comments for complex logic
- Test locally before PR

### Areas for Contribution

- 🔐 Additional security features (WebAuthn, 2FA)
- 🌐 Internationalization (i18n)
- 📱 Mobile app (React Native)
- 🎨 UI/UX improvements
- 🧪 More comprehensive tests
- 🚀 Performance optimizations

---

## 👥 Team

| Name | Role | LinkedIn |
|------|------|----------|
| **Ruchika Verma** | Full Stack + AI/ML | [Profile](https://www.linkedin.com/in/ruchika-verma-888bb6309) |
| **Divyanshi Singh** | Backend | [Profile](https://linkedin.com/in/member2) |
| **Archana Agahari** | Frontend + UI/UX | [Profile](https://linkedin.com/in/member3) |
| **Rashmi** | Security | [Profile](https://linkedin.com/in/member4) |

---

## 🚀 Future Roadmap

### Phase 1
- [ ] WebAuthn integration (passwordless login)
- [ ] Mobile app (iOS + Android)
- [ ] Multi-language support
- [ ] Accessibility features (WCAG 2.1 AA)

### Phase 2
- [ ] WebSocket real-time updates
- [ ] Advanced analytics dashboard
- [ ] Voter registration API for government integration
- [ ] Load testing for 1M+ concurrent users

### Phase 3
- [ ] Distributed blockchain network
- [ ] Smart contracts for vote validation
- [ ] Integration with national ID systems
- [ ] Pilot deployment in local government

### Phase 4
- [ ] National-level deployment
- [ ] Third-party security audit
- [ ] Compliance certifications (ISO 27001)
- [ ] Open API for electoral commissions

---


<div align="center">

**Made with ❤️ by SentinelVote AI Team**

*"Security is not optional in democracy. It's fundamental."*

[⬆ Back to Top](#️-sentinelvote-ai)

</div>
