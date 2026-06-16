from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db
from models.resume import Resume

resume_bp = Blueprint("resume", __name__)

# ==========================
# GET ALL RESUMES
# ==========================
@resume_bp.route("/", methods=["GET"])
@login_required
def get_resumes():
    resumes = Resume.query.filter_by(user_id=current_user.id).all()

    return jsonify([
        r.to_dict()
        for r in resumes
    ])


# ==========================
# GET SINGLE RESUME
# ==========================
@resume_bp.route("/<int:id>", methods=["GET"])
@login_required
def get_resume(id):
    resume = Resume.query.filter_by(id=id, user_id=current_user.id).first()

    if not resume:
        return jsonify({"error": "Resume not found"}), 404

    return jsonify(resume.to_dict())


# ==========================
# CREATE RESUME
# ==========================
# @resume_bp.route("/create", methods=["POST"])
# @login_required
# def create_resume():
#     data = request.get_json() or {}

#     title = data.get("title")
#     if not title:
#         return jsonify({"error": "Title is required"}), 400

#     # resume = Resume(
#     #     user_id=current_user.id,
#     #     title=title,
#     #     summary=data.get("summary", ""),
#     #     template_id=data.get("template_id", "basic")
#     # )
#     resume = Resume(
#     user_id=current_user.id,
#     title=data.get("title", ""),
#     summary=data.get("summary", ""),
#     template_id=data.get("template_id", "basic"),

#     full_name=data.get("full_name", ""),
#     email=data.get("email", ""),
#     phone=data.get("phone", ""),
#     location=data.get("location", ""),
#     linkedin=data.get("linkedin", ""),
#     github=data.get("github", ""),

#     skills=data.get("skills", ""),
#     experience=data.get("experience", ""),
#     education=data.get("education", ""),
#     projects=data.get("projects", ""),
#     certifications=data.get("certifications", ""),
#     languages=data.get("languages", "")
# )

#     db.session.add(resume)
#     db.session.commit()

#     return jsonify({
#         "id": resume.id,
#         "message": "Resume created successfully"
#     }), 201


# ==========================
# UPDATE RESUME
# ==========================
@resume_bp.route("/<int:id>", methods=["PUT"])
@login_required
def update_resume(id):
    resume = Resume.query.filter_by(id=id, user_id=current_user.id).first()

    if not resume:
        return jsonify({"error": "Resume not found"}), 404

    data = request.get_json() or {}


    resume.title = data.get("title", resume.title)
    resume.role = data.get("role", resume.role)
    resume.contact = data.get("contact", resume.contact)
    resume.summary = data.get("summary", resume.summary)
    resume.skills = data.get("skills", resume.skills)
    resume.experience = data.get("experience", resume.experience)
    resume.education = data.get("education", resume.education)
    resume.projects = data.get("projects", resume.projects)

    if "template_id" in data:
        resume.template_id = data["template_id"]

    db.session.commit()

    return jsonify({"message": "Resume updated successfully"})


# ==========================
# DELETE RESUME
# ==========================
@resume_bp.route("/<int:id>", methods=["DELETE"])
@login_required
def delete_resume(id):
    resume = Resume.query.filter_by(id=id, user_id=current_user.id).first()

    if not resume:
        return jsonify({"error": "Resume not found"}), 404

    db.session.delete(resume)
    db.session.commit()

    return jsonify({"message": "Resume deleted successfully"})

@resume_bp.route("/create", methods=["POST"])
@login_required
def create_resume():

    try:

        data = request.get_json()
        print("DATA RECEIVED:", data)

        resume = Resume(
            user_id=current_user.id,
            title=data.get("title", "New Resume"),
            role=data.get("role", ""),
            contact=data.get("contact", ""),
            summary=data.get("summary", ""),
            skills=data.get("skills", ""),
            experience=data.get("experience", ""),
            education=data.get("education", ""),
            projects=data.get("projects", "")
        )

        db.session.add(resume)
        db.session.commit()

        return jsonify(resume.to_dict())

    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500