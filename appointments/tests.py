from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import datetime
from departments.models import Department
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment

User = get_user_model()

class AppointmentValidationTestCase(TestCase):
    def setUp(self):
        self.doc_user = User.objects.create_user(username='docuser', password='password123', role='Doctor')
        self.pat_user = User.objects.create_user(username='patuser', password='password123', role='Patient')
        
        self.department = Department.objects.create(
            department_name="Cardiology",
            department_description="Heart Care"
        )
        
        self.doctor = Doctor.objects.create(
            user=self.doc_user,
            doctor_name="Alice Smith",
            doctor_specialization="Cardiologist",
            qualification="MD",
            experience=10,
            phone="+1234567890",
            email="alice@medicare.com",
            consultation_fee=150.00,
            department=self.department,
            available_days="Mon, Wed",
            available_time="09:00 AM - 01:00 PM"
        )
        
        self.patient = Patient.objects.create(
            user=self.pat_user,
            patient_name="Bob Jones",
            patient_age=45,
            gender="Male",
            patient_phone="+1987654321",
            patient_email="bob@example.com",
            address="123 Main St",
            blood_group="O+",
            patient_problem="Chest pain"
        )

    def test_successful_appointment_booking(self):
        """Test booking a valid appointment is successful."""
        future_date = datetime.date.today() + datetime.timedelta(days=2)
        appt = Appointment(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=future_date,
            appointment_time=datetime.time(10, 0),
            appointment_status='Pending'
        )
        appt.full_clean()
        appt.save()
        self.assertEqual(Appointment.objects.count(), 1)

    def test_past_date_booking_prevention(self):
        """Test that booking an appointment on a past date raises a validation error."""
        past_date = datetime.date.today() - datetime.timedelta(days=1)
        appt = Appointment(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=past_date,
            appointment_time=datetime.time(10, 0)
        )
        with self.assertRaises(ValidationError) as context:
            appt.full_clean()
        self.assertIn('appointment_date', context.exception.message_dict)

    def test_double_booking_prevention(self):
        """Test that booking the same doctor on the same date and time raises a validation error."""
        future_date = datetime.date.today() + datetime.timedelta(days=5)
        time_slot = datetime.time(11, 0)
        
        appt1 = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=future_date,
            appointment_time=time_slot,
            appointment_status='Approved'
        )
        
        appt2 = Appointment(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=future_date,
            appointment_time=time_slot,
            appointment_status='Pending'
        )
        
        with self.assertRaises(ValidationError):
            appt2.full_clean()

