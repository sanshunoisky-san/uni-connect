import unittest
from app.models import db, User, Therapist, Appointment, ForumPost, Comment, Feedback
from run import app

class UniSupportTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        with app.app_context():
            db.drop_all()
            db.create_all()
            self.seed_data()

    def seed_data(self):
        student = User(username="student1", role="student")
        student.set_password("pass")

        therapist = User(username="therapist1", role="therapist")
        therapist.set_password("pass")

        profile = Therapist(name="therapist1", slots=["10:00"])
        db.session.add_all([student, therapist, profile])
        db.session.commit()

    def login(self, username, password):
        return self.app.post("/login", data=dict(username=username, password=password), follow_redirects=True)

    """ appointments """

    def test_book_appointment_positive(self):
        self.login("student1", "pass")
        response = self.app.post("/book", data={"therapist": 1, "slot": "10:00"}, follow_redirects=True)
        self.assertIn(b"pending approval", response.data)

    def test_book_appointment_negative_duplicate(self):
        self.login("student1", "pass")
        self.app.post("/book", data={"therapist": 1, "slot": "10:00"}, follow_redirects=True)
        response = self.app.post("/book", data={"therapist": 1, "slot": "10:00"}, follow_redirects=True)
        self.assertIn(b"already booked", response.data)

    """ feedback """

    def test_feedback_positive(self):
        self.login("student1", "pass")
        response = self.app.post("/feedback", data={"name": "Test", "message": "Good job"}, follow_redirects=True)
        self.assertIn(b"Feedback submitted", response.data)

    def test_feedback_negative_empty(self):
        self.login("student1", "pass")
        response = self.app.post("/feedback", data={"name": "", "message": ""}, follow_redirects=True)
        self.assertIn(b"Feedback submitted", response.data)

    """ forum comments """

    def test_forum_comment_positive(self):
        with app.app_context():
            post = ForumPost(title="Test", content="Test content")
            db.session.add(post)
            db.session.commit()
        self.login("student1", "pass")
        response = self.app.post("/comment/1", data={"comment": "Nice post!"}, follow_redirects=True)
        self.assertIn(b"Nice post", response.data)

    def test_forum_comment_negative_not_logged_in(self):
        response = self.app.post("/comment/1", data={"comment": "Bad"}, follow_redirects=True)
        self.assertIn(b"Please log in", response.data)

if __name__ == "__main__":
    unittest.main()
