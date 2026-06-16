import pyotp
import qrcode
import secrets
import string
import os
from datetime import datetime


# ==========================
# Generate OTP Secret
# ==========================

def generate_secret():

    return pyotp.random_base32()


# ==========================
# Generate TOTP Object
# ==========================

def get_totp(secret):

    return pyotp.TOTP(secret)


# ==========================
# Generate Current OTP
# ==========================

def generate_otp(secret):

    totp = get_totp(secret)

    return totp.now()


# ==========================
# Verify OTP
# ==========================

def verify_otp(
    secret,
    otp
):

    try:

        totp = get_totp(secret)

        return totp.verify(
            otp,
            valid_window=1
        )

    except Exception:

        return False


# ==========================
# Generate QR Code
# Google Authenticator
# ==========================

def generate_qr_code(
    email,
    secret,
    issuer_name="AI Resume Builder"
):

    totp = pyotp.TOTP(secret)

    provisioning_uri = (
        totp.provisioning_uri(
            name=email,
            issuer_name=issuer_name
        )
    )

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )

    qr.add_data(
        provisioning_uri
    )

    qr.make(
        fit=True
    )

    image = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    if not os.path.exists(
        "static/qr"
    ):
        os.makedirs(
            "static/qr"
        )

    filename = (
        f"static/qr/"
        f"{email}.png"
    )

    image.save(
        filename
    )

    return filename


# ==========================
# Generate Email OTP
# ==========================

def generate_email_otp():

    return str(
        secrets.randbelow(
            900000
        ) + 100000
    )


# ==========================
# Generate Backup Codes
# ==========================

def generate_backup_codes(
    count=10
):

    codes = []

    for _ in range(count):

        code = ''.join(
            secrets.choice(
                string.ascii_uppercase
                + string.digits
            )
            for _ in range(8)
        )

        codes.append(
            code
        )

    return codes


# ==========================
# Validate Backup Code
# ==========================

def verify_backup_code(
    entered_code,
    stored_codes
):

    return (
        entered_code
        in stored_codes
    )


# ==========================
# Generate Temporary OTP
# Reset Password / Email Verification
# ==========================

def generate_temp_otp():

    return str(
        secrets.randbelow(
            900000
        ) + 100000
    )


# ==========================
# OTP Expiry Checker
# ==========================

def is_otp_expired(
    expiry_time
):

    return datetime.utcnow() > expiry_time


# ==========================
# Create Recovery Secret
# ==========================

def generate_recovery_secret():

    return secrets.token_urlsafe(
        32
    )


# ==========================
# Mask Secret
# ==========================

def mask_secret(secret):

    return (
        secret[:4]
        + "********"
        + secret[-4:]
    )


# ==========================
# Security Helper
# ==========================

def generate_device_token():

    return secrets.token_hex(
        32
    )


# ==========================
# QR URL Helper
# ==========================

def get_qr_path(email):

    return (
        f"static/qr/"
        f"{email}.png"
    )