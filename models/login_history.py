from datetime import datetime
from models.user import db
from models import db
class LoginHistory(db.Model):

    __tablename__ = "login_history"

    id = db.Column(db.Integer, primary_key=True)

    # 🔥 FIXED FOREIGN KEY
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),   # FIX HERE
        nullable=False
    )

    ip_address = db.Column(db.String(100))
    browser = db.Column(db.String(255))
    operating_system = db.Column(db.String(255))
    device_type = db.Column(db.String(100))
    login_status = db.Column(db.String(50), default="SUCCESS")

    login_time = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship(
        "User",
        backref="login_history",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "ip_address": self.ip_address,
            "browser": self.browser,
            "operating_system": self.operating_system,
            "device_type": self.device_type,
            "login_status": self.login_status,
            "login_time": self.login_time
        }

    def __repr__(self):
        return f"<LoginHistory {self.user_id} {self.login_time}>"