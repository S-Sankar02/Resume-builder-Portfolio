from flask_mail import Mail
from flask_mail import Message
from flask import current_app
import traceback


mail = Mail()


# ====================================
# GENERIC EMAIL SENDER
# ====================================

def send_email(
    recipient,
    subject,
    body
):

    try:

        msg = Message(
            subject=subject,
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[recipient]
        )


        # HTML email
        msg.html = body


        mail.send(msg)


        print("EMAIL SENT SUCCESS")

        return True


    except Exception as e:

        print(
            f"Email Error: {str(e)}"
        )

        traceback.print_exc()

        return False



# ====================================
# VERIFY EMAIL
# ====================================
def send_verification_email(
    recipient,
    verification_link
):

    subject = "Verify Your Email"

    body = f"""
    <html>
    <body>

    <h2>Verify Email</h2>

    <p>Click the button below to verify your account.</p>

    <a href="{verification_link}">
        Verify Email
    </a>

    </body>
    </html>
    """

    return send_email(
        recipient,
        subject,
        body
    )

# ====================================
# RESET PASSWORD
# ====================================

def send_reset_password_email(
    recipient,
    reset_link
):


    subject = "Reset Your Password"


    body = f"""


<html>

<body>


<h2>
Password Reset Request
</h2>


<p>
A password reset request was received.
</p>


<p>
Click below to reset your password:
</p>


<a href="{reset_link}"
style="
background:#dc3545;
color:white;
padding:12px 25px;
text-decoration:none;
border-radius:6px;
">

Reset Password

</a>


<br><br>


<p>
This link expires in 1 hour.
</p>


<p>
If you did not request this, ignore this email.
</p>


</body>

</html>


"""


    return send_email(
        recipient,
        subject,
        body
    )




# ====================================
# LOGIN OTP
# ====================================

def send_login_otp_email(
    recipient,
    otp
):


    subject = "Your Login OTP"


    body = f"""


<html>

<body>


<h2>
Login OTP
</h2>


<p>
Your OTP is:
</p>


<h1>
{otp}
</h1>


<p>
Valid for 5 minutes.
</p>


<p>
Do not share this OTP.
</p>


</body>

</html>


"""


    return send_email(
        recipient,
        subject,
        body
    )




# ====================================
# WELCOME EMAIL
# ====================================

def send_welcome_email(
    recipient,
    username
):


    subject = "Welcome to AI Resume Builder"


    body = f"""


<html>

<body>


<h2>
Welcome {username} 🎉
</h2>


<p>
Your account was created successfully.
</p>


<ul>

<li>
AI Resume Builder
</li>

<li>
Portfolio Builder
</li>

<li>
ATS Resume Checker
</li>

<li>
PDF Export
</li>

</ul>


<p>

Regards,<br>

AI Resume Builder Team

</p>


</body>

</html>


"""


    return send_email(
        recipient,
        subject,
        body
    )




# ====================================
# ACCOUNT LOCK ALERT
# ====================================

def send_account_locked_email(
    recipient
):


    subject = "Security Alert"


    body = """

<html>

<body>


<h2>
Account Locked
</h2>


<p>

Your account has been locked because of multiple failed login attempts.

</p>


<p>

Please reset your password.

</p>


</body>

</html>


"""


    return send_email(
        recipient,
        subject,
        body
    )




# ====================================
# SMTP TEST
# ====================================

def test_email_connection():


    try:


        msg = Message(

            subject="SMTP Test",

            sender=current_app.config["MAIL_USERNAME"],

            recipients=[
                current_app.config["MAIL_USERNAME"]
            ]

        )


        msg.html = """

<h2>
SMTP Test Successful
</h2>

<p>
Your Flask email system is working.
</p>

"""


        mail.send(msg)


        return True



    except Exception as e:


        print(
            f"SMTP Test Failed: {e}"
        )


        return False