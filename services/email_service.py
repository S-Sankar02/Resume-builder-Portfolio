from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# =====================================
# SEND EMAIL
# =====================================

def send_email(recipient, subject, html_content):
    try:

        message = Mail(
            from_email=current_app.config["MAIL_DEFAULT_SENDER"],
            to_emails=recipient,
            subject=subject,
            html_content=html_content
        )

        sg = SendGridAPIClient(
            current_app.config["MAIL_PASSWORD"]
        )

        response = sg.send(message)

        print("EMAIL STATUS:", response.status_code)

        return {
            "success": True,
            "status": response.status_code
        }

    except Exception as e:
        print("EMAIL ERROR:", str(e))

        return {
            "success": False,
            "error": str(e)
        }


# =====================================
# VERIFY EMAIL
# =====================================

def send_verification_email(recipient, verification_link):

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;padding:20px">

        <h2 style="color:#2563eb;">
            Welcome to AI Resume Builder 🚀
        </h2>

        <p>
            Your account has been created successfully.
        </p>

        <p>
            Please verify your email address:
        </p>

        <p style="margin:30px 0;">
            <a href="{verification_link}"
               style="
               background:#2563eb;
               color:white;
               padding:12px 24px;
               text-decoration:none;
               border-radius:6px;
               font-weight:bold;">
                Verify Email
            </a>
        </p>

        <p>
            If the button does not work, copy this link:
        </p>

        <p style="word-break:break-all;">
            {verification_link}
        </p>

        <hr>

        <p>
            Regards,<br>
            AI Resume Builder Team
        </p>

    </div>
    """

    return send_email(
        recipient,
        "Verify Your Email - AI Resume Builder",
        html
    )


# =====================================
# RESET PASSWORD
# =====================================

def send_reset_password_email(recipient, reset_link):

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;padding:20px">

        <h2 style="color:#dc2626;">
            Password Reset Request
        </h2>

        <p>
            A password reset request was received.
        </p>

        <p>
            Click below to reset your password:
        </p>

        <p style="margin:30px 0;">
            <a href="{reset_link}"
               style="
               background:#dc2626;
               color:white;
               padding:12px 24px;
               text-decoration:none;
               border-radius:6px;
               font-weight:bold;">
                Reset Password
            </a>
        </p>

        <p>
            This link expires in 1 hour.
        </p>

        <p>
            If you did not request this, ignore this email.
        </p>

        <hr>

        <p>
            AI Resume Builder Team
        </p>

    </div>
    """

    return send_email(
        recipient,
        "Password Reset Request",
        html
    )


# =====================================
# ACCOUNT LOCKED
# =====================================

def send_account_locked_email(recipient):

    html = """
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;padding:20px">

        <h2 style="color:#dc2626;">
            Account Locked
        </h2>

        <p>
            Your account has been locked because of multiple failed login attempts.
        </p>

        <p>
            Please wait 30 minutes before trying again.
        </p>

        <hr>

        <p>
            AI Resume Builder Team
        </p>

    </div>
    """

    return send_email(
        recipient,
        "Account Locked",
        html
    )