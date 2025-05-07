class Observer:
    def notify(self, appointment):
        print(f"Notification: Appointment for user_id={appointment.user_id} "
              f"with therapist_id={appointment.therapist_id} at slot {appointment.slot} is now {appointment.status}.")
