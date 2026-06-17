from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from services.ai.ats_service import ATSService
import PyPDF2
import docx


ai_bp = Blueprint("ai", __name__)

# =========================
# ATS PAGE
# =========================


@ai_bp.route("/ats-checker")
@login_required
def ats_checker():

    return render_template("ats_checker.html")


# =========================
# EXTRACT FILE TEXT
# =========================


def extract_text(file):

    filename = file.filename.lower()

    try:

        if filename.endswith(".pdf"):

            reader = PyPDF2.PdfReader(file)

            text = ""

            for page in reader.pages:

                text += page.extract_text() or ""

            return text

        elif filename.endswith(".docx"):

            document = docx.Document(file)

            return "\n".join(p.text for p in document.paragraphs)

        elif filename.endswith(".txt"):

            return file.read().decode("utf-8")

        return ""

    except Exception as e:

        print("FILE ERROR:", e)

        return ""


# =========================
# ATS API
# =========================


@ai_bp.route("/api/ats/analyze", methods=["POST"])
@login_required
def analyze_ats():

    try:

        job_description = request.form.get("job_description", "")

        resume_file = request.files.get("resume_file")

        if not job_description:

            return jsonify({"success": False, "message": "Job description required"})

        if not resume_file:

            return jsonify({"success": False, "message": "Resume file required"})

        resume_text = extract_text(resume_file)

        result = ATSService.calculate(
            provider="groq", resume_text=resume_text, job_description=job_description
        )

        return jsonify({"success": True, "result": result})

    except Exception as e:

        print("ATS ERROR:", str(e))

        return jsonify({"success": False, "message": str(e)})
