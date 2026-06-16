from flask import Blueprint, request, jsonify
from flask_login import login_required
from models import db
from models.experience import Experience

experience_bp = Blueprint("experience", __name__)

@experience_bp.route("/add", methods=["POST"])
@login_required
def add():
    exp = Experience(**request.json)
    db.session.add(exp)
    db.session.commit()
    return jsonify({"message": "Added"})