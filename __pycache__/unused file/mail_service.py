from flask_mail import Mail, Message

mail = Mail()

class EmailService:

    @staticmethod
    def send_verification(email, token):
        msg = Message(
            "Verify Your Account",
            recipients=[email]
        )

        msg.body = f"""
        Click to verify your account:
        http://localhost:5000/auth/verify/{token}
        """

        mail.send(msg)

    @staticmethod
    def send_reset(email, token):
        msg = Message(
            "Reset Password",
            recipients=[email]
        )

        msg.body = f"""
        Reset your password:
        http://localhost:5000/auth/reset/{token}
        """

        mail.send(msg)