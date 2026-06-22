from flask_mail import Mail, Message
from flask import current_app
import traceback

mail = Mail()


# ====================================
# CORE EMAIL SENDER (CLEAN + SAFE)
# ====================================

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

        return {
            "success": True,
            "message": "Email sent successfully"
        }

    except Exception as e:
        print("EMAIL ERROR:", str(e))
        traceback.print_exc()

        return {
            "success": False,
            "error": str(e)
        }


# ====================================
# OTP EMAIL
# ====================================

def send_login_otp_email(recipient, otp):
    subject = "Your Login OTP"

    body = f"""
    <h2>Login OTP</h2>
    <p>Your OTP is:</p>
    <h1>{otp}</h1>
    <p>Valid for 5 minutes</p>
    """

    return send_email(recipient, subject, body)


# ====================================
# RESET PASSWORD EMAIL
# ====================================

def send_reset_password_email(recipient, reset_link):
    subject = "Reset Password"

    body = f"""
    <h2>Password Reset</h2>
    <p>Click below to reset:</p>
    <a href="{reset_link}">Reset Password</a>
    """

    return send_email(recipient, subject, body)


# ====================================
# WELCOME EMAIL
# ====================================

def send_welcome_email(recipient, username):
    subject = "Welcome"

    body = f"""
    <h2>Welcome {username}</h2>
    <p>Your account is ready.</p>
    """

    return send_email(recipient, subject, body)