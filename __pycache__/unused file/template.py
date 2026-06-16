from . import db
from models import db
class ResumeTemplate(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100))
    html_structure = db.Column(db.Text)
    css_style = db.Column(db.Text)