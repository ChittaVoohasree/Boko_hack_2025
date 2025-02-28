from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from extensions import db
import re

register_bp = Blueprint("register", __name__)

# Password Validation Function
def is_valid_password(password):
    if len(password) <= 8:
        return "Password must be 8+ characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must contain at least one special character."
    return None

# Username Validation Function
def is_valid_username(username):
    if len(username) < 3:
        return "Username must be at least 3 characters long."
    if not re.search(r"[a-zA-Z]", username):  # Ensure at least one letter
        return "Username must contain at least one letter (A-Z or a-z)."
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return "Username can only contain letters, numbers, and underscores."
    return None

@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        captcha_response = request.form.get("captcha")
        stored_captcha = session.get("captcha_text")

        if not stored_captcha or captcha_response.upper() != stored_captcha:
            flash("Invalid CAPTCHA. Please try again.", "error")
            return redirect(url_for("register.register"))

        session.pop("captcha_text", None)

         # Validate Username
        username_error = is_valid_username(username)
        if username_error:
            flash(username_error, "error")
            return redirect(url_for("register.register"))

        # Validate Password
        password_error = is_valid_password(password)
        if password_error:
            flash(password_error, "error")
            return redirect(url_for("register.register"))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
            return redirect(url_for("register.register"))
        

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login.login"))

    return render_template("register.html")

