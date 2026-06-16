from datetime import datetime
from models import db

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)

    title = db.Column(db.String(150), default="My Portfolio")
    template = db.Column(db.String(50), default="modern")

    # ALL UI DATA HERE (NO bio/github columns anymore)
    data = db.Column(db.JSON, default=dict)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)