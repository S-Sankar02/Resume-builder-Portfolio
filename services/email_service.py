from flask_mail import Mail, Message
from flask import current_app
import traceback

mail = Mail()


# =========================
# CORE EMAIL SENDER
# =========================
def send_email(recipient, subject, body):
    try:
        msg = Message(
            subject=subject,
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[recipient],
            html=body
        )

        mail.send(msg)
        return True

    except Exception as e:
        print("EMAIL ERROR:", str(e))
        traceback.print_exc()
        return False


# =========================
# VERIFY EMAIL (FIX FOR auth.py)
# =========================
def send_verification_email(recipient, link):
    return send_email(
        recipient,
        "Verify Email",
        f"<h2>Verify Email</h2><a href='{link}'>Click here</a>"
    )


# =========================
# RESET PASSWORD
# =========================
def send_reset_password_email(recipient, link):
    return send_email(
        recipient,
        "Reset Password",
        f"<h2>Reset Password</h2><a href='{link}'>Reset</a>"
    )


# =========================
# ACCOUNT LOCK EMAIL
# =========================
def send_account_locked_email(recipient):
    return send_email(
        recipient,
        "Account Locked",
        "<h2>Your account is locked due to failed attempts</h2>"
    )