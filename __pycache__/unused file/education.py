from . import db
from models import db
class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, nullable=False)

    institution = db.Column(db.String(200))
    degree = db.Column(db.String(100))
    start_year = db.Column(db.String(10))
    end_year = db.Column(db.String(10))
    description = db.Column(db.Text)