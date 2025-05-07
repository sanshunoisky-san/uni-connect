from app.models import db, User
from run import app

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        student_user = User(username="student1", role="student")
        student_user.set_password("student123")
        db.session.add(student_user)

        db.session.commit()
        print("Seed data inserted:")
        print("Student user: student1")
