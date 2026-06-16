from flask import Blueprint, render_template
from flask_login import login_required

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/ats-checker")
@login_required
def ats_checker():
    return render_template("ats_checker.html")
