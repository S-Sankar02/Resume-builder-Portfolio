from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import (login_user,logout_user,login_required)
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import secrets
from models.user import db, User
from models.login_history import LoginHistory
from services.email_service import (send_verification_email,send_reset_password_email,send_account_locked_email)
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
    methods=["GET","POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get("name","").strip()
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        if not name or not email or not password:
            flash(
                "All fields are required.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            flash(
                "Email already registered.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )
        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")
        token = secrets.token_urlsafe(32)
        user = User(
            name=name,
            email=email,
            password=hashed_password,
            email_verify_token=token,
            is_verified=False
        )

        db.session.add(user)
        db.session.commit()
        verification_link = (
            request.host_url
            +
            "verify-email/"
            +
            token
        )
        send_verification_email(
            email,
            verification_link
        )
        flash(
            "Registration successful. Check your email.",
            "success"
        )
        return redirect(
            url_for("auth.login")
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
            "Invalid verification link.",
            "danger"
        )
        return redirect(
            url_for("auth.login")
        )
    user.is_verified = True
    user.email_verify_token = None
    db.session.commit()
    flash(
        "Email verified successfully.",
        "success"
    )
    return redirect(
        url_for("auth.login")
    )
# ====================================
# LOGIN
# ====================================

@auth.route(
    "/login",
    methods=["GET","POST"]
)

def login():

    if request.method=="POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()
        password = request.form.get(
            "password",
            ""
        )
        user = User.query.filter_by(
            email=email
        ).first()
        if not user:

            flash(
                "Invalid credentials.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        if user.account_locked:


            flash(
                "Account locked.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )
        if not user.is_verified:

            flash(
                "Please verify your email first.",
                "warning"
            )

            return redirect(
                url_for("auth.login")
            )

        if bcrypt.check_password_hash(

            user.password,

            password

        ):
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

            login_user(
                user,
                remember=True
            )

            flash(
                "Login successful.",
                "success"
            )

            return redirect(
                "/dashboard"
            )
        else:
            user.failed_attempts += 1

            if user.failed_attempts >= 5:

                user.account_locked=True
                send_account_locked_email(
                    user.email
                )

            db.session.commit()

            flash(
                "Invalid credentials.",
                "danger"
            )
            return redirect(
                url_for("auth.login")
            )
    return render_template(
        "login.html"
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
        "Logged out successfully.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )
# ====================================
# FORGOT PASSWORD
# ====================================

@auth.route(
    "/forgot-password",
    methods=["GET","POST"]
)

def forgot_password():

    if request.method=="POST":

        email=request.form.get(
            "email",
            ""
        ).strip().lower()

        user=User.query.filter_by(
            email=email
        ).first()

        if user:

            token=secrets.token_urlsafe(32)

            user.reset_token=token

            user.reset_expiry=(

                datetime.utcnow()
                +
                timedelta(hours=1)

            )

            db.session.commit()

            reset_link=(

                request.host_url
                +
                "reset-password/"
                +
                token

            )

            send_reset_password_email(

                email,

                reset_link

            )

        flash(

            "Password reset link sent.",

            "success"

       )

        return redirect(
            url_for("auth.login")
        )


    return render_template(
        "forgot_password.html"
    )
# ====================================
# RESET PASSWORD
# ====================================

@auth.route(
    "/reset-password/<token>",
    methods=["GET","POST"]
)

def reset_password(token):


    user=User.query.filter_by(
        reset_token=token
    ).first()

    if not user:

        return "Invalid token"
 
    if user.reset_expiry < datetime.utcnow():

        return "Token expired"

    if request.method=="POST":

        password=request.form.get(
            "password"
        )

        user.password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        user.reset_token=None
        user.reset_expiry=None
        user.failed_attempts=0
        user.account_locked=False
        db.session.commit()
        flash(
            "Password updated successfully.",
            "success"
        )
        return redirect(
            url_for("auth.login")
        )
    return render_template(
        "reset_password.html"
    )