from datetime import datetime
from models import db


class Resume(db.Model):
    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # Basic Information
    title = db.Column(db.String(150), nullable=False)

    role = db.Column(
        db.String(200),
        default=""
    )

    contact = db.Column(
        db.String(300),
        default=""
    )

    # Resume Sections
    summary = db.Column(
        db.Text,
        default=""
    )

    skills = db.Column(
        db.Text,
        default=""
    )

    experience = db.Column(
        db.Text,
        default=""
    )

    education = db.Column(
        db.Text,
        default=""
    )

    projects = db.Column(
        db.Text,
        default=""
    )

    template_id = db.Column(
        db.String(50),
        default="basic"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "role": self.role,
            "contact": self.contact,
            "summary": self.summary,
            "skills": self.skills,
            "experience": self.experience,
            "education": self.education,
            "projects": self.projects,
            "template_id": self.template_id,
            "created_at": self.created_at.isoformat()
            if self.created_at else None,
            "updated_at": self.updated_at.isoformat()
            if self.updated_at else None
        }

    def __repr__(self):
        return f"<Resume {self.id}: {self.title}>"