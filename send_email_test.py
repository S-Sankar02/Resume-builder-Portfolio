from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail, Message
import os

load_dotenv()

app = Flask(__name__)

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)

with app.app_context():
    msg = Message(
        subject="SendGrid Test",
        recipients=["supporthub.mail@gmail.com"]
    )

    msg.body = "If you received this email, SendGrid is working."

    mail.send(msg)

    print("EMAIL SENT SUCCESSFULLY")