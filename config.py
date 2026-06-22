import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:

    # =========================
    # Flask Security
    # =========================
    SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret_key")

    # =========================
    # Database
    # =========================


    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = (
      "sqlite:///" + os.path.join(BASE_DIR, "resume_builder.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # =========================
    # Mail
    # =========================
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv(
    "MAIL_DEFAULT_SENDER",
    "supporthub.mail@gmail.com"
    )
    MAIL_TIMEOUT = 20


    # =========================
    # Session Security
    # =========================
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = True

    # =========================
    # OTP / Reset
    # =========================
    OTP_EXPIRY_MINUTES = 5
    RESET_TOKEN_EXPIRY_HOURS = 1

    # =========================
    # Login Security
    # =========================
    MAX_LOGIN_ATTEMPTS = 5
    ACCOUNT_LOCK_MINUTES = 30

    # =========================
    # App Info
    # =========================
    APP_NAME = "AI Resume Builder"
    APP_URL = os.getenv("APP_URL", "http://127.0.0.1:5000")

    # =========================
    # AI Keys
    # =========================
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")