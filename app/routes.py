import json

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User, Appointment, Therapist

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

@routes.route("/appointments")
@login_required
def show_appointments():
    if current_user.role != "student":
        flash("Only students can book appointments.")
        return redirect(url_for("routes.index"))
    therapists = Therapist.query.all()
    if not therapists:
        return json.dumps("statusCode: 404")
    return render_template("appointments.html", therapists=therapists)

@routes.route("/book", methods=["POST"])
@login_required
def book_appointment():
    if current_user.role != "student":
        flash("Only students can book appointments.")
        return redirect(url_for("routes.index"))
    therapist_id = int(request.form["therapist"])
    slot = request.form["slot"]
    existing = Appointment.query.filter_by(
        therapist_id=therapist_id,
        slot=slot
    ).filter(Appointment.status != "cancelled").first()
    if existing:
        return json.dumps("statusCode:403")
    appointment = Appointment(
        therapist_id=therapist_id,
        user_id=current_user.id,
        slot=slot,
        status="pending"
    )
    db.session.add(appointment)
    db.session.commit()
    return json.dumps("statusCode: 200")
