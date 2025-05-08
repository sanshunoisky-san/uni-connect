UniSupport - A Mental Health Support System (Prototype)

1. Description of the system:
     UniSupport offers a mental health and welfare support system tailored for university environments. Through this system, students can book their appointment, contribute in discussion forums, and give their feedback with options to stay anonymous.
     The system allows therapists to accept or reject the appointments, while all submitted feedback is restricted to administrators. This prototype illustrates the core design and functionalities which were proposed in Assignment 1, highlighting its usability, role-based access control and scalability.
     This system is built using Python's Flask framework, utilizing Flask-Login for user authentication and Flask-SQLAlchemy for database management. The software engineering practices followed includes the MVC pattern, Observer design pattern and Separation of Concerns (RBACs). Each user role (student, therapist, admin) uniquely reflects their permissions. A dedicated test suite validates all the critical features using a range of positive and negative test cases.
     This prototype successfully demonstrates the feasibility of the system's architecture and its potential for scalability. With all the business logic being modular and tested, Git version control maintains a clear history of development.

2. How to set up and run the project: 
    - create a new conda env with python version 3.9 (conda_env_name)
    - conda activate conda_env_name
      (or just open a new terminal if the above step is not preferred)
    - conda install -y -c conda-forge --file requirements.txt

    (if the above code does not work, follow the below 3 steps)
    - conda install flask
    - conda install -c conda-forge flask-sqlalchemy
    - conda install -c conda-forge flask-login

    run seed.py to populate the db 
    start the project by running the run.py file
    
    TEST CASES:
    run test_app.py main to see the positive and negative test cases

3. Technologies used:
   - Language: Python 3.9
   - Framework: Flask
   - Database: Flask-SQLAlchemy
   - Authentication: Flask-Login
   - Version Control: Git

4. Implemented Features
   Fundamentals:
   - 3 roles - student, therapist and admin.
   - Therapists and students may register and login based on role-based access.
   - Admins are only populated from seed data.
   - Default set of students and therapists are also provided in the seed data to start with.
   - A user can enroll as a student or therapist based on which the flow and rendered data changes (interactive).
   - Navigation is implemented using role based access controls, separate set of nav links for each role.
   Main Feature 1: Appointment Booking system:
   - Students can request appointments with available therapists.
   - Therapists can accept or reject an appointment request.
   - Students(my appointments page) and Therapists(manage appointments page) can view their bookings.
   - A student can have more than 1 booking.
   - A doctor can also have more than 1 booking.
   Main Feature 2: Discussion forum
   - Students are able to add and edit their comments on the welfare discussion forum.
   - Comments from different students(if commented) are displayed over the commented posts.
   - A student can comment more than once on the same post.
   Main Feature 3: Feedbacks
   - Students may provide feedback with their names or anonymously.
   - Admins can view the feedback posted by the students.
   - A student can provide more than 1 feedback.
   Design patterns followed:
   - Observer pattern is applied to mimic appointment notifications.
   - MVC pattern is followed.
   - Separation of Concerns (RBACs).
   Test cases incorporated:
   - Duplicate and positive appointment booking
   - Empty and valid feedback submission
   - Forum commenting (logged-in and not logged-in)
    
5. Contributions:
   | Student Name                   | ID               | Contribution (%) | Work Done                                                                                             |
   | ---                            | ---              | ---              | ---                                                                                                   |
   | Sanjay Sethu Madhavan          | 2810612          |       25         | login functionality, manage appointments, rbacs, display feedbacks, observer pattern and documentation|
   | Devang Raut                    | 2870619          |       22         | book appointments, display appointments, registration functionality and documentation                 |
   | Deepak Talele                  | 2796076          |       22         | discussion forum with display posts and comments, and add comments                                    |
   | Ashwin Sathiyanarayanan Renuka | 2838000          |       16         | test cases and edit/delete comments                                                                   |
   | Sheran Paththinikuttige        | 2506307          |       15         | post feedbacks                                                                                        |
