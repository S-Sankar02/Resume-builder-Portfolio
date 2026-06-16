from . import db
from models import db
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, nullable=False)

    name = db.Column(db.String(100))
    level = db.Column(db.String(50))