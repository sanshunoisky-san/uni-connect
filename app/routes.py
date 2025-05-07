from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User

routes = Blueprint('routes', __name__)


@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully.")
            return redirect(url_for("routes.index"))
        flash("Invalid credentials.")
    return render_template("login.html")

@routes.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("routes.login"))

@routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        if role not in ["student", "therapist"]:
            flash("Invalid role.")
            return redirect(url_for("routes.register"))
        if User.query.filter_by(username=username).first():
            flash("Username already taken.")
            return redirect(url_for("routes.register"))
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Account created. Please login.")
        return redirect(url_for("routes.login"))
    return render_template("register.html")

@routes.route("/")
@login_required
def index():
    return render_template("index.html")
