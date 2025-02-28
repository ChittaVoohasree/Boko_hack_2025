from flask import Blueprint, render_template, session, redirect, url_for
from extensions import db
from sqlalchemy import text

hub_bp = Blueprint("hub", __name__)

@hub_bp.route("/hub")
def hub():
    if "user" in session:
        is_admin = session.get("is_admin", False)
        sql = f"SELECT * from users where id in (SELECT user_id FROM admin_credentials)"
        result = db.session.execute(text(sql))
        admin_usernames = [row[1] for row in result]
        is_admin = session["user"] in admin_usernames
        return render_template("hub.html", username=session["user"], is_admin=is_admin)
    else:
        return redirect(url_for("login.login"))
