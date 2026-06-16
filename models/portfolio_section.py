from models import db
from models import db
class PortfolioSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    portfolio_id = db.Column(db.Integer, nullable=False)

    type = db.Column(db.String(50))  # about, skills, projects

    title = db.Column(db.String(100))
    content = db.Column(db.Text)