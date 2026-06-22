from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import traceback

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import current_app
import traceback


def send_email(recipient, subject, html):

    try:

        message = Mail(
            from_email=current_app.config["MAIL_DEFAULT_SENDER"],
            to_emails=recipient,
            subject=subject,
            html_content=html
        )

        sg = SendGridAPIClient(
            current_app.config["MAIL_PASSWORD"]
        )

        response = sg.send(message)

        print(
            "SENDGRID STATUS:",
            response.status_code
        )

        return {"success": True}

    except Exception as e:

        print("EMAIL ERROR:", str(e))

        return {
            "success": False,
            "error": str(e)
        }
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