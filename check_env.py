from dotenv import load_dotenv
import os

load_dotenv(override=True)

print("EMAIL =", repr(os.getenv("MAIL_USERNAME")))
print("PASSWORD =", repr(os.getenv("MAIL_PASSWORD")))
print("LENGTH =", len(os.getenv("MAIL_PASSWORD", "")))