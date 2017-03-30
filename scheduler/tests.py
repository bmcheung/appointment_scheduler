import datetime

from django.test import TestCase
from django.utils import timezone
from .models import Appointment
# Create your tests here.

class AppointmentMethodTests(TestCase):
    def test_appointment_was_missed_with_status_Pending(self):
        """
        appointment_was_missed should return True if
        the appointment is scheduled for a time before
        current and status is Pending
        """
        past_date = timezone.now() - datetime.timedelta(days=30)
        past_appointment = Appointment(time = past_date, status='Pending')
        self.assertIs(past_appointment.appointment_was_missed(), True)
    def test_appointment_was_not_missed_with_status_Completed(self):
        """
        appointment_was_missed should return False if
        the appointment is scheduled for a time before
        current and status is Completed
        """
        past_date = timezone.now() - datetime.timedelta(days=30)
        past_appointment = Appointment(time = past_date, status='Completed')
        self.assertIs(past_appointment.appointment_was_missed(), False)
