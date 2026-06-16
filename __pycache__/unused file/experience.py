from . import db
from models import db
class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, nullable=False)

    company = db.Column(db.String(200))
    role = db.Column(db.String(100))
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    description = db.Column(db.Text)