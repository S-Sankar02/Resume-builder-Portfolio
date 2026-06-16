import jwt
import datetime

SECRET = "super-secret-key"

class TokenService:

    @staticmethod
    def generate_token(email, expiry_minutes=30):

        payload = {
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=expiry_minutes)
        }

        return jwt.encode(payload, SECRET, algorithm="HS256")

    @staticmethod
    def verify_token(token):
        try:
            return jwt.decode(token, SECRET, algorithms=["HS256"])
        except:
            return None