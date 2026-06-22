from flask_mail import Mail, Message
from flask import current_app
import traceback
import threading

mail = Mail()

# ====================================
# INTERNAL SAFE SENDER
# ====================================

def _send(msg):
    try:
        mail.send(msg)
    except Exception as e:
        print("EMAIL FAILED:", str(e))


# ====================================
# CORE EMAIL SENDER (NON-BLOCKING)
# ====================================

def send_email(recipient, subject, body):
    try:
        msg = Message(
            subject=subject,
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[recipient],
            html=body
        )

        # 🔥 IMPORTANT: RUN IN BACKGROUND THREAD
        threading.Thread(target=_send, args=(msg,)).start()

        return {"success": True, "message": "Email queued"}

    except Exception as e:
        print("EMAIL ERROR:", str(e))
        traceback.print_exc()

        return {"success": False, "error": str(e)}


# ====================================
# HELPERS
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