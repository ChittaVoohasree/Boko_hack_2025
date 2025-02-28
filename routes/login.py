from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from models.user import User
from extensions import db
from datetime import timedelta
from flask import make_response
import os

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session.permanent = True
            session_lifetime = timedelta(minutes=1)
            session.permanent_session_lifetime = session_lifetime

            session["user"] = user.username
            session.modified = True
            session["session_id"] = os.urandom(16).hex()
            flash("Login successful!", "success")
            return redirect(url_for("hub.hub"))
        else:
            flash("Invalid username or password.", "error")

    return render_template("login.html")

@login_bp.route("/logout")
def logout():
    session.clear()
    session.pop("user", None)
    session.pop('_flashes',None)
    flash("You have been logged out.", "info")
    response = make_response(redirect(url_for("login.login")))
    response.set_cookie('session', '', expires=0)
    return redirect(url_for("login.login"))
