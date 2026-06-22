import os
import PyPDF2
import docx
from werkzeug.utils import secure_filename
from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from flask_login import LoginManager, login_required, current_user
from flask_bcrypt import Bcrypt
from config import Config
from models.user import db, User
from models.portfolio import Portfolio
from models.resume import Resume
from models.login_history import LoginHistory
from services.email_service import mail
from routes.auth import auth
from routes.ai import ai_bp
from routes.resume import resume_bp
from routes.portfolio import portfolio_bp
from routes.admin import admin_bp

# =========================
# APP INIT
# =========================
app = Flask(__name__)
app.config.from_object(Config)
bcrypt = Bcrypt(app)

db.init_app(app)
mail.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# =========================
# BLUEPRINTS
# =========================
app.register_blueprint(auth)
app.register_blueprint(ai_bp, url_prefix="/ai")
app.register_blueprint(resume_bp, url_prefix="/resume")
app.register_blueprint(portfolio_bp, url_prefix="/portfolio")
app.register_blueprint(admin_bp, url_prefix="/admin")


# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("auth.login"))

@app.route("/dashboard")
@login_required
def dashboard():

    resume_count = Resume.query.filter_by(
        user_id=current_user.id
    ).count()

    portfolio_count = Portfolio.query.filter_by(
        user_id=current_user.id
    ).count()

    login_count = LoginHistory.query.filter_by(
        user_id=current_user.id
    ).count()

    recent_activity = LoginHistory.query.filter_by(
        user_id=current_user.id
    ).order_by(
        LoginHistory.login_time.desc()
    ).limit(5).all()

    return render_template(
        "dashboard.html",
        user=current_user,
        resume_count=resume_count,
        portfolio_count=portfolio_count,
        login_count=login_count,
        recent_activity=recent_activity
    )
@app.route("/portfolio-builder")
@login_required
def portfolio_builder():
    portfolio = Portfolio.query.filter_by(user_id=current_user.id).first()

    if not portfolio:
        portfolio = Portfolio(
            user_id=current_user.id,
            title="My Portfolio",
            data={}
        )
        db.session.add(portfolio)
        db.session.commit()
    print("Loaded Portfolio ID:", portfolio.id if portfolio else None)
    return render_template("portfolio.html", portfolio=portfolio)


@app.route("/resume-builder")
@login_required
def resume_builder():
    return render_template("resume_builder.html")

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    if request.method == "POST":

        # Update name only if provided
        name = request.form.get("name")

        if name:
            current_user.name = name


        # Password update
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password:

            if password != confirm_password:

                flash("Passwords do not match", "danger")

                return redirect(url_for("settings"))

            current_user.password = bcrypt.generate_password_hash(
                password
            ).decode("utf-8")


        # Profile image upload
        image = request.files.get("profile_image")

        print("IMAGE =", image)


        if image and image.filename:

            upload_folder = os.path.join(
                app.root_path,
                "static",
                "uploads"
            )

            os.makedirs(upload_folder, exist_ok=True)

            filename = secure_filename(image.filename)

            image_path = os.path.join(
                upload_folder,
                filename
            )

            image.save(image_path)

            current_user.profile_image = (
                "/static/uploads/" + filename
            )

            print(
                "DB PATH =",
                current_user.profile_image
            )


        db.session.commit()

        flash(
            "Settings updated successfully!",
            "success"
        )

        return redirect(url_for("settings"))

    return render_template("settings.html")



@app.route("/ats-checker")
@login_required
def ats_checker_redirect():
    return redirect(url_for("ai.ats_checker"))


# =========================
# SKILL SYSTEM (CLEAN)
# =========================
SKILL_DB = {
    "python", "flask", "django", "fastapi",
    "sql", "mysql", "postgresql",
    "docker", "kubernetes",
    "aws", "azure", "gcp",
    "rest", "api",
    "git", "github",
    "html", "css", "javascript",
    "react", "node", "express",
    "machine learning", "deep learning",
    "pandas", "numpy"
}

ROLE_SKILL_MAP = {
    "backend": ["python", "flask", "django", "sql", "api", "docker"],
    "frontend": ["html", "css", "javascript", "react"],
    "fullstack": ["python", "flask", "react", "sql", "api"],
    "data": ["python", "pandas", "numpy", "machine learning"],
    "devops": ["docker", "kubernetes", "aws", "linux"]
}


# =========================
# TEXT EXTRACTION
# =========================
def extract_text(file):
    try:
        filename = file.filename.lower()

        if filename.endswith(".pdf"):
            reader = PyPDF2.PdfReader(file)
            return " ".join([p.extract_text() or "" for p in reader.pages])

        elif filename.endswith(".docx"):
            doc = docx.Document(file)
            return " ".join([p.text for p in doc.paragraphs])

        elif filename.endswith(".txt"):
            return file.read().decode("utf-8", errors="ignore")

        return ""

    except Exception as e:
        print("File error:", str(e))
        return ""


# =========================
# SKILL EXTRACTION
# =========================
def extract_skills(text):
    text = text.lower()
    return {skill for skill in SKILL_DB if skill in text}


# =========================
# ROLE DETECTION ENGINE
# =========================
def detect_role_skills(text):
    text = text.lower()
    skills = set()

    for role, skill_list in ROLE_SKILL_MAP.items():
        if role in text:
            skills.update(skill_list)

    skills.update(extract_skills(text))
    return skills


# =========================
# ATS API (PRO VERSION)
# =========================
@app.route("/api/ats/analyze", methods=["POST"])
@login_required
def ats_analyze():
    try:
        job_desc = request.form.get("job_description", "").strip()
        resume_file = request.files.get("resume_file")

        if not job_desc or not resume_file:
            return jsonify({
                "success": False,
                "message": "Job description and resume are required"
            }), 400

        resume_text = extract_text(resume_file)

        if not resume_text:
            return jsonify({
                "success": False,
                "message": "Could not read resume"
            }), 400

        job_desc = job_desc.lower()
        resume_text = resume_text.lower()

        job_skills = detect_role_skills(job_desc)
        resume_skills = extract_skills(resume_text)

        matched = job_skills & resume_skills
        missing = job_skills - resume_skills

        score = round((len(matched) / len(job_skills)) * 100) if job_skills else 0

        if score >= 85:
            label = "Strong Match 🚀"
        elif score >= 60:
            label = "Good Match 👍"
        elif score >= 40:
            label = "Average Match ⚠️"
        else:
            label = "Weak Match ❌"

        return jsonify({
            "success": True,
            "score": score,
            "label": label,
            "matched": list(matched),
            "missing": list(missing)
        })

    except Exception as e:
        print("ATS ERROR:", str(e))
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), 500


# =========================
# ERROR HANDLERS
# =========================
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    db.session.rollback()
    return render_template("500.html"), 500


@app.route("/favicon.ico")
def favicon():
    return "", 204


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

    