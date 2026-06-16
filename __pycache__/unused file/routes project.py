from flask import Blueprint, request, jsonify
from flask_login import login_required
from models import db
from models.project import Project

project_bp = Blueprint("project", __name__)

@project_bp.route("/add", methods=["POST"])
@login_required
def add():
    project = Project(**request.json)
    db.session.add(project)
    db.session.commit()
    return jsonify({"message": "Added"})