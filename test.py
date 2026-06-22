import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

server = smtplib.SMTP("smtp.sendgrid.net", 587)
server.starttls()

server.login(
    os.getenv("MAIL_USERNAME"),
    os.getenv("MAIL_PASSWORD")
)

print("LOGIN SUCCESS")