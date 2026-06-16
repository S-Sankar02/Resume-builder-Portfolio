from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import url_for

from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

from flask_bcrypt import Bcrypt

from datetime import datetime
from datetime import timedelta

import secrets
import random

from models.user import db
from models.user import User

from models.login_history import LoginHistory

from services.email_service import (
    send_verification_email,
    send_reset_password_email,
    send_login_otp_email,
    send_welcome_email,
    send_account_locked_email
)

auth = Blueprint(
    "auth",
    __name__
)

bcrypt = Bcrypt()


# ====================================
# REGISTER
# ====================================

@auth.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get(
            "name"
        )

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "Email already registered."
            )

            return redirect(
                "/register"
            )

        hashed_password = (
            bcrypt.generate_password_hash(
                password
            ).decode("utf-8")
        )

        verification_token = (
            secrets.token_urlsafe(
                32
            )
        )

        user = User(
            name=name,
            email=email,
            password=hashed_password,
            email_verify_token=verification_token,
            is_verified=False
        )

        db.session.add(user)
        db.session.commit()

        verification_link = (
            f"http://127.0.0.1:5000/"
            f"verify-email/"
            f"{verification_token}"
        )

        send_verification_email(
            email,
            verification_link
        )

        send_welcome_email(
            email,
            name
        )

        flash(
            "Registration successful. Verify your email."
        )

        return redirect(
            "/login"
        )

    return render_template(
        "register.html"
    )


# ====================================
# VERIFY EMAIL
# ====================================

@auth.route(
    "/verify-email/<token>"
)
def verify_email(token):

    user = User.query.filter_by(
        email_verify_token=token
    ).first()

    if not user:

        flash(
            "Invalid verification link."
        )

        return redirect(
            "/login"
        )

    user.is_verified = True

    user.email_verify_token = None

    db.session.commit()

    flash(
        "Email verified successfully."
    )

    return redirect(
        "/login"
    )


# ====================================
# LOGIN
# ====================================
@auth.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Invalid credentials.")
            return redirect("/login")

        if user.account_locked:
            flash("Account locked.")
            return redirect("/login")

        if not user.is_verified:
            flash("Please verify your email first.")
            return redirect("/login")

        password_valid = bcrypt.check_password_hash(
            user.password,
            password
        )

        if password_valid:

            user.failed_attempts = 0
            user.last_login = datetime.utcnow()

            history = LoginHistory(
                user_id=user.id,
                ip_address=request.remote_addr,
                browser=request.user_agent.string,
                login_status="SUCCESS"
            )

            db.session.add(history)
            db.session.commit()

            login_user(user, remember=True)

            flash("Login successful.")
            return redirect("/dashboard")

        else:

            user.failed_attempts += 1

            if user.failed_attempts >= 5:
                user.account_locked = True
                send_account_locked_email(user.email)

            db.session.commit()

            flash("Invalid credentials.")
            return redirect("/login")

    return render_template("login.html")

# ====================================
# OTP VERIFY
# ====================================

@auth.route(
    "/verify-otp/<int:user_id>",
    methods=["GET", "POST"]
)
def verify_otp(user_id):

    user = User.query.get(
        user_id
    )

    if not user:

        return redirect(
            "/login"
        )

    if request.method == "POST":

        otp = request.form.get(
            "otp"
        )

        if (
            user.login_otp == otp
            and datetime.utcnow()
            <= user.login_otp_expiry
        ):

            login_user(
                user,
                remember=True
            )

            user.login_otp = None

            user.last_login = (
                datetime.utcnow()
            )

            history = LoginHistory(
                user_id=user.id,
                ip_address=request.remote_addr,
                browser=request.user_agent.string,
                login_status="SUCCESS"
            )

            db.session.add(
                history
            )

            db.session.commit()

            flash(
                "Login successful."
            )

            return redirect(
                "/dashboard"
            )

        flash(
            "Invalid OTP."
        )

    return render_template(
        "verify_otp.html"
    )


# ====================================
# LOGOUT
# ====================================

@auth.route(
    "/logout"
)
@login_required
def logout():

    logout_user()

    flash(
        "Logged out successfully."
    )

    return redirect(
        "/login"
    )


# ====================================
# FORGOT PASSWORD
# ====================================

@auth.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():

    if request.method == "POST":

        email = request.form.get(
            "email"
        )

        user = User.query.filter_by(
            email=email
        ).first()

        if user:

            token = (
                secrets.token_urlsafe(
                    32
                )
            )

            user.reset_token = token

            user.reset_expiry = (
                datetime.utcnow()
                + timedelta(hours=1)
            )

            db.session.commit()

            reset_link = (
                f"http://127.0.0.1:5000/"
                f"reset-password/"
                f"{token}"
            )

            send_reset_password_email(
                email,
                reset_link
            )

        flash(
            "Password reset link sent."
        )

        return redirect(
            "/login"
        )

    return render_template(
        "forgot_password.html"
    )


# ====================================
# RESET PASSWORD
# ====================================

@auth.route(
    "/reset-password/<token>",
    methods=["GET", "POST"]
)
def reset_password(token):

    user = User.query.filter_by(
        reset_token=token
    ).first()

    if not user:

        return "Invalid token"

    if (
        user.reset_expiry
        < datetime.utcnow()
    ):
        return "Token expired"

    if request.method == "POST":

        password = request.form.get(
            "password"
        )

        hashed_password = (
            bcrypt.generate_password_hash(
                password
            ).decode("utf-8")
        )

        user.password = (
            hashed_password
        )

        user.reset_token = None

        user.reset_expiry = None

        user.failed_attempts = 0

        user.account_locked = False

        db.session.commit()

        flash(
            "Password updated successfully."
        )

        return redirect(
            "/login"
        )

    return render_template(
        "reset_password.html"
    )