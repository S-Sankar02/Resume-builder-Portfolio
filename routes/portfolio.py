from flask import Blueprint, redirect, request, jsonify, render_template, send_file
from flask_login import login_required, current_user

from models.portfolio import Portfolio
from services.portfolio_service import PortfolioService
from services.export_service import ExportService

portfolio_bp = Blueprint("portfolio", __name__)

# =========================
# CREATE
# =========================
@portfolio_bp.route("/create", methods=["POST"])
@login_required
def create():
    data = request.json
    pid = PortfolioService.create(current_user.id, data)
    return jsonify({"success": True, "portfolio_id": pid})


# =========================
# GET (CANVA LOAD)
# =========================
@portfolio_bp.route("/get/<int:pid>")
@login_required
def get(pid):
    p = PortfolioService.get(pid)
    return jsonify({
        "success": True,
        "data": p.data
    })


# =========================
# UPDATE (CANVA SAVE CORE)
# =========================
@portfolio_bp.route("/update/<int:pid>", methods=["POST"])
@login_required
def update(pid):
    data = request.json
    PortfolioService.update(pid, data)
    return jsonify({"success": True})


# =========================
# PUBLIC PAGE
# =========================
@portfolio_bp.route("/p/<int:pid>")
def public(pid):
    p = Portfolio.query.get_or_404(pid)
    return render_template("portfolio/public.html", data=p.data)


# =========================
# EXPORT PDF
# =========================
@portfolio_bp.route("/export/<int:pid>")
@login_required
def export_portfolio(pid):
    file_url = ExportService.export_pdf(pid)
    return redirect(file_url)