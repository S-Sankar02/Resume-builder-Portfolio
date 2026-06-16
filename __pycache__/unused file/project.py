from . import db
from models import db
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, nullable=False)

    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    link = db.Column(db.String(300))