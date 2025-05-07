from app.models import db, User, Therapist
from run import app

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        therapist1_user = User(username="drsmith", role="therapist")
        therapist1_user.set_password("smith123")

        therapist2_user = User(username="dralice", role="therapist")
        therapist2_user.set_password("alice123")

        db.session.add_all([therapist1_user, therapist2_user])
        db.session.flush()

        therapist1 = Therapist(name="drsmith", slots=["10:00", "11:00", "15:00"])
        therapist2 = Therapist(name="dralice", slots=["13:00", "14:30", "16:00"])
        db.session.add_all([therapist1,therapist2])

        student_user = User(username="student1", role="student")
        student_user.set_password("student123")
        db.session.add(student_user)

        db.session.commit()
        print("Seed data inserted:")
        print("Student user: student1")
