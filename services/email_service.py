from flask_mail import Mail, Message
from flask import current_app
import traceback

mail = Mail()

# ====================================
# CORE EMAIL SENDER
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

        return {"success": True, "message": "Email sent successfully"}

    except Exception as e:
        print("EMAIL ERROR:", str(e))
        traceback.print_exc()

        return {"success": False, "error": str(e)}


# ====================================
# EMAIL HELPERS
# ====================================

def send_verification_email(recipient, verification_link):
    return send_email(
        recipient,
        "Verify Email",
        f'<a href="{verification_link}">Verify Email</a>'
    )


def send_reset_password_email(recipient, reset_link):
    return send_email(
        recipient,
        "Reset Password",
        f'<a href="{reset_link}">Reset Password</a>'
    )


def send_account_locked_email(recipient):
    return send_email(
        recipient,
        "Account Locked",
        "<h3>Your account is locked due to failed attempts.</h3>"
    )