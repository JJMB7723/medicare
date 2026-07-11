from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
from patients.models import Patient
from doctors.models import Doctor

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    appointment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        # Prevent booking past dates
        if self.appointment_date and self.appointment_date < datetime.date.today():
            raise ValidationError({'appointment_date': "You cannot book an appointment for a past date."})

        # Prevent double booking for same doctor at same date and time
        if self.appointment_date and self.appointment_time and self.doctor_id:
            overlap = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date=self.appointment_date,
                appointment_time=self.appointment_time
            ).exclude(appointment_status='Cancelled')
            
            if self.pk:
                overlap = overlap.exclude(pk=self.pk)
                
            if overlap.exists():
                raise ValidationError("This doctor is already booked for this specific date and time.")

    def __str__(self):
        return f"{self.patient.patient_name} - Dr. {self.doctor.doctor_name} ({self.appointment_date} {self.appointment_time})"

