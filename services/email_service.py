from flask_mail import Mail
from flask_mail import Message
from flask import current_app
import traceback

mail = Mail()

def send_email(
    recipient,
    subject,
    body
):
    """
    Generic Email Sender
    """

    try:

        msg = Message(
            subject=subject,
            recipients=[recipient]
        )

        msg.body = body

        mail.send(msg)

        return True

    except Exception as e:

        print(
            f"Email Error: {str(e)}"
        )

        traceback.print_exc()

        return False


def send_verification_email(
    recipient,
    verification_link
):
    """
    Account Verification Email
    """

    subject = "Verify Your Account"

    body = f"""
Hello,

Welcome to AI Resume Builder.

Please verify your email address by clicking the link below:

{verification_link}

If you did not create an account,
please ignore this email.

Regards,
AI Resume Builder Team
"""

    return send_email(
        recipient,
        subject,
        body
    )


def send_reset_password_email(
    recipient,
    reset_link
):
    """
    Password Reset Email
    """

    subject = "Reset Your Password"

    body = f"""
Hello,

A password reset request was received.

Click the link below to reset your password:

{reset_link}

This link will expire in 1 hour.

If you did not request this,
please ignore this email.

Regards,
AI Resume Builder Team
"""

    return send_email(
        recipient,
        subject,
        body
    )


def send_login_otp_email(
    recipient,
    otp
):
    """
    Login OTP Email
    """

    subject = "Your Login OTP"

    body = f"""
Hello,

Your One-Time Password (OTP) is:

{otp}

This OTP is valid for 5 minutes.

Do not share this OTP with anyone.

Regards,
AI Resume Builder Team
"""

    return send_email(
        recipient,
        subject,
        body
    )


def send_welcome_email(
    recipient,
    username
):
    """
    Welcome Email
    """

    subject = "Welcome to AI Resume Builder"

    body = f"""
Hello {username},

Welcome to AI Resume Builder.

Your account has been created successfully.

You can now:

- Build Professional Resumes
- Generate AI Resume Summaries
- Create Portfolio Websites
- Export PDF Resumes
- Check ATS Scores

Thank you for joining us.

Regards,
AI Resume Builder Team
"""

    return send_email(
        recipient,
        subject,
        body
    )


def send_account_locked_email(
    recipient
):
    """
    Account Lock Alert
    """

    subject = "Security Alert"

    body = """
Hello,

Your account has been temporarily locked due to multiple failed login attempts.

Please reset your password or contact support.

Regards,
AI Resume Builder Security Team
"""

    return send_email(
        recipient,
        subject,
        body
    )


def test_email_connection():
    """
    Test SMTP Configuration
    """

    try:

        msg = Message(
            subject="SMTP Test",
            recipients=[
                current_app.config[
                    "MAIL_USERNAME"
                ]
            ]
        )

        msg.body = "SMTP Test Successful"

        mail.send(msg)

        return True

    except Exception as e:

        print(
            f"SMTP Test Failed: {e}"
        )

        return False