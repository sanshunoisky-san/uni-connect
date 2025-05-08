from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User, Appointment, Therapist, ForumPost, Comment, Feedback
from .utils import Observer

routes = Blueprint('routes', __name__)
notifier = Observer()

""" login route """
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

""" logout route """
@routes.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("routes.login"))

""" register route """
@routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        if role not in ["student", "therapist", "admin"]:
            flash("Invalid role.")
            return redirect(url_for("routes.register"))
        if User.query.filter_by(username=username).first():
            flash("Username already taken.")
            return redirect(url_for("routes.register"))
        user = User(username=username, role=role)
        user.set_password(password)
        if role == "therapist":
            therapist1 = Therapist(name=username, slots=["10:00", "11:00", "15:00"])
            db.session.add(therapist1)
        db.session.add(user)
        db.session.commit()

        flash("Account created. Please login.")
        return redirect(url_for("routes.login"))
    return render_template("register.html")

""" landing page """
@routes.route("/")
@login_required
def index():
    return render_template("index.html")

""" checks the role and displays the respective appointments """
@routes.route("/appointments")
@login_required
def show_appointments():
    if current_user.role != "student":
        flash("Only students can book appointments.")
        return redirect(url_for("routes.index"))
    therapists = Therapist.query.all()
    if not therapists:
        return render_template("status.html", message="No therapists are available at the moment.")
    return render_template("appointments.html", therapists=therapists)

""" checks the roles, creates an appointment with associations """
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
        return render_template("status.html", message="This slot is already booked.")
    appointment = Appointment(
        therapist_id=therapist_id,
        user_id=current_user.id,
        slot=slot,
        status="pending"
    )
    db.session.add(appointment)
    db.session.commit()
    notifier.notify(appointment)
    return render_template("status.html", message="Appointment requested and pending approval.")

""" update the appointment and commit to db """
@routes.route("/appointments/update/<int:appointment_id>/<action>")
@login_required
def update_appointment_status(appointment_id, action):
    if current_user.role != "therapist":
        flash("Unauthorized.")
        return redirect(url_for("routes.index"))
    appointment = Appointment.query.get_or_404(appointment_id)
    if action == "accept":
        appointment.status = "booked"
    elif action == "reject":
        appointment.status = "cancelled"
    else:
        flash("Invalid action.")
        return redirect(url_for("routes.manage_appointments"))
    db.session.commit()
    notifier.notify(appointment)
    return redirect(url_for("routes.manage_appointments"))

""" manage the appointments by checking roles """
@routes.route("/appointments/manage")
@login_required
def manage_appointments():
    if current_user.role != "therapist":
        flash("Only therapists can manage appointments.")
        return redirect(url_for("routes.index"))
    therapist = Therapist.query.filter_by(name=current_user.username).first()
    if not therapist:
        flash("No profile found.")
        return redirect(url_for("routes.index"))
    appointments = Appointment.query.filter_by(therapist_id=therapist.id).all()
    return render_template("manage_appointments.html", appointments=appointments)

""" check roles and display appointment """
@routes.route("/my-appointments")
@login_required
def my_appointments():
    if current_user.role != "student":
        flash("Only students can view their appointments.")
        return redirect(url_for("routes.index"))
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    return render_template("my_appointments.html", appointments=appointments)

""" display the forum """
@routes.route("/forum", methods=["GET"])
@login_required
def forum():
    posts = ForumPost.query.all()
    return render_template("forum.html", posts=posts)

""" create and add comment """
@routes.route("/comment/<int:post_id>", methods=["POST"])
@login_required
def comment(post_id):
    comment_text = request.form["comment"]
    comment = Comment(post_id=post_id, user_id=current_user.id, text=comment_text)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("routes.forum"))

""" updates the comment by checking the roles """
@routes.route("/comment/update/<int:comment_id>", methods=["POST"])
@login_required
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        flash("You can only edit your own comments.")
        return redirect(url_for("routes.forum"))
    new_text = request.form["new_text"]
    comment.text = new_text
    db.session.commit()
    flash("Comment updated.")
    return redirect(url_for("routes.forum"))

""" deletes the comment by checking the roles """
@routes.route("/comment/delete/<int:comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        flash("You can only delete your own comments.")
        return redirect(url_for("routes.forum"))
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted.")
    return redirect(url_for("routes.forum"))

""" post feedback """
@routes.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]
        feedback = Feedback(name=name or "Anonymous", message=message)
        db.session.add(feedback)
        db.session.commit()
        return render_template("status.html", message="Feedback submitted successfully.")
    return render_template("feedback.html")

""" view feedbacks based on role """
@routes.route("/feedbacks/view")
@login_required
def view_feedbacks():
    if current_user.role != "admin":
        flash("Access denied.")
        return redirect(url_for("routes.index"))
    feedbacks = Feedback.query.order_by(Feedback.timestamp.desc()).all()
    return render_template("view_feedbacks.html", feedbacks=feedbacks)
