from flask import Blueprint, request, jsonify
from flask_login import login_required
from models import db
# from models.education import Education

education_bp = Blueprint("education", __name__)

# @education_bp.route("/add", methods=["POST"])
# @login_required
# def add():
#     data = request.json

#     edu = Education(**data)
#     db.session.add(edu)
#     db.session.commit()

#     return jsonify({"message": "Added"})