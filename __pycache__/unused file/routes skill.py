from flask import Blueprint, request, jsonify
from flask_login import login_required
from models import db
from models.skill import Skill

skill_bp = Blueprint("skill", __name__)

@skill_bp.route("/add", methods=["POST"])
@login_required
def add():
    skill = Skill(**request.json)
    db.session.add(skill)
    db.session.commit()
    return jsonify({"message": "Added"})