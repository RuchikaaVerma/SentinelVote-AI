from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template
from config import Config
from database.db import init_db
from routes.auth_routes import auth_bp
from routes.vote_routes import vote_bp
from routes.admin_routes import admin_bp
from flask import session, redirect

app = Flask(__name__)
app.config.from_object(Config)

init_db(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(vote_bp)
app.register_blueprint(admin_bp)



# ── Auth Pages ───────────────────────────────
@app.route("/register-page")
def register_page():
    return render_template("register.html")

@app.route("/login-page")
def login_page():
    return render_template("login.html")

# ── Dashboard ────────────────────────────────
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login-page")

    if session.get("role") != "admin":
        return redirect("/vote-page")

    return render_template("dashboard.html")

@app.route("/confirmation")
def confirmation():
    # Get data from session or query params
    timestamp = request.args.get("timestamp", datetime.now().strftime("%d %b %Y, %H:%M:%S"))
    audit_hash = request.args.get("hash", "abc123def456...")  # Replace with real hash
    
    return render_template(
        "confirmation.html",
        timestamp=timestamp,
        audit_hash=audit_hash
    )


# ── Run App ──────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
