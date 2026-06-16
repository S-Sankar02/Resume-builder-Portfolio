from flask import Blueprint, render_template
from models.user import User
from models.resume import Resume
from models.portfolio import Portfolio

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard")
def dashboard():

    users = User.query.all()
    resumes = Resume.query.all()
    portfolios = Portfolio.query.all()

    return render_template(
        "admin/dashboard.html",
        users=users,
        resumes=resumes,
        portfolios=portfolios
    )

