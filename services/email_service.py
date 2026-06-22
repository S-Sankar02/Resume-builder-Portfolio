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

        print("EMAIL SENT SUCCESS")

        return {"success": True}

    except Exception as e:
        print("EMAIL ERROR:", str(e))
        traceback.print_exc()
        return {"success": False, "error": str(e)}


# =========================
# VERIFY EMAIL (FIXED MISSING FUNCTION)
# =========================
def send_verification_email(recipient, verification_link):
    subject = "Verify Your Email"

    body = f"""
    <h2>Email Verification</h2>
    <p>Click below to verify:</p>
    <a href="{verification_link}">Verify Email</a>
    """

    return send_email(recipient, subject, body)


# =========================
# RESET PASSWORD
# =========================
def send_reset_password_email(recipient, reset_link):
    subject = "Reset Your Password"

    body = f"""
    <h2>Password Reset</h2>
    <p>Click below:</p>
    <a href="{reset_link}">Reset Password</a>
    """

    return send_email(recipient, subject, body)


# =========================
# ACCOUNT LOCK ALERT
# =========================
def send_account_locked_email(recipient):
    subject = "Account Locked"

    body = """
    <h2>Security Alert</h2>
    <p>Your account has been locked due to failed login attempts.</p>
    """

    return send_email(recipient, subject, body)


# =========================
# TEST EMAIL
# =========================
def test_email_connection():
    try:
        msg = Message(
            subject="SMTP Test",
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[current_app.config["MAIL_USERNAME"]],
            html="<h1>SMTP Working</h1>"
        )

        mail.send(msg)
        return True

    except Exception as e:
        print("SMTP ERROR:", str(e))
        return False