from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from models import db

class User(UserMixin, db.Model):

    __tablename__ = "users"

    # =========================
    # Primary Key
    # =========================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =========================
    # Basic Information
    # =========================

    name = db.Column(
    db.String(100),
    nullable=False
    )

    email = db.Column(
    db.String(120),
    unique=True,
    nullable=False
    )

    password = db.Column(
    db.String(255),
    nullable=False
    )

    # =========================
    # Profile Image
    # =========================

    profile_image = db.Column(
    db.String(255),
    nullable=True
    )

    # =========================
    # Email Verification
    # =========================

    is_verified = db.Column(
    db.Boolean,
    default=False
    )

    email_verify_token = db.Column(
        db.String(255),
        nullable=True
    )

  
    # =========================
    # Password Reset
    # =========================

    reset_token = db.Column(
        db.String(255),
        nullable=True
    )

    reset_expiry = db.Column(
        db.DateTime,
        nullable=True
    )

    # =========================
    # Login Security
    # =========================

    failed_attempts = db.Column(
        db.Integer,
        default=0
    )

    account_locked = db.Column(
        db.Boolean,
        default=False
    )

    # =========================
    # Login Tracking
    # =========================

    last_login = db.Column(
        db.DateTime,
        nullable=True
    )

    last_ip = db.Column(
        db.String(100),
        nullable=True
    )

    last_device = db.Column(
        db.String(255),
        nullable=True
    )

    # =========================
    # Timestamps
    # =========================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # =========================
    # Flask-Login
    # =========================

    def get_id(self):
        return str(self.id)

    # =========================
    # Helper Methods
    # =========================

    def lock_account(self):
        self.account_locked = True

    def unlock_account(self):
        self.account_locked = False
        self.failed_attempts = 0

    def verify_email(self):
        self.is_verified = True
        self.email_verify_token = None

    def clear_reset_token(self):
        self.reset_token = None
        self.reset_expiry = None

    # =========================
    # Serialization
    # =========================
def to_dict(self):

    return {
        "id": self.id,
        "name": self.name,
        "email": self.email,
        "profile_image": self.profile_image,
        "is_verified": self.is_verified,
        "account_locked": self.account_locked,
        "failed_attempts": self.failed_attempts,
        "last_login": self.last_login,
        "created_at": self.created_at
    }

    # =========================
    # Debug Representation
    # =========================

    def __repr__(self):

        return (
            f"<User {self.id} "
            f"{self.email}>"
        )
