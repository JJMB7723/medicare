from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from datetime import timedelta, time
from departments.models import Department
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment

User = get_user_model()

class AppointmentValidationTests(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(
            department_name="Cardiology",
            department_description="Heart Care"
        )
        self.doctor = Doctor.objects.create(
            doctor_name="Sarah Jenkins",
            doctor_specialization="Cardiologist",
            qualification="MD",
            experience=10,
            phone="12345",
            email="sjenkins@test.com",
            consultation_fee=100.00,
            department=self.dept,
            available_days="Monday",
            available_time="09:00 AM - 05:00 PM"
        )
        self.patient = Patient.objects.create(
            patient_name="John Miller",
            patient_age=30,
            gender="Male",
            patient_phone="98765",
            patient_email="jmiller@test.com",
            address="123 Street",
            blood_group="O+",
            patient_problem="Chest Pain"
        )

    def test_prevent_past_date_booking(self):
        """Should raise ValidationError if appointment is booked for a past date."""
        past_date = timezone.now().date() - timedelta(days=1)
        appointment = Appointment(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=past_date,
            appointment_time=time(10, 0),
            appointment_status="Pending"
        )
        with self.assertRaises(ValidationError):
            appointment.full_clean()

    def test_allow_future_date_booking(self):
        """Should succeed when booking for a future date."""
        future_date = timezone.now().date() + timedelta(days=5)
        appointment = Appointment(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=future_date,
            appointment_time=time(10, 0),
            appointment_status="Pending"
        )
        # Should execute successfully without throwing errors
        appointment.full_clean()

    def test_prevent_double_booking_same_doctor_and_time(self):
        """Should raise ValidationError if doctor is booked for the same date and time slot."""
        future_date = timezone.now().date() + timedelta(days=5)
        app_time = time(11, 30)

        # Create first booking
        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=future_date,
            appointment_time=app_time,
            appointment_status="Pending"
        )

        # Attempt to book second appointment for same doctor, date, time
        app2 = Appointment(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=future_date,
            appointment_time=app_time,
            appointment_status="Pending"
        )

        with self.assertRaises(ValidationError):
            app2.full_clean()
