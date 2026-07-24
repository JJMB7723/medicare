from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
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
        
        # 1. Prevent past dates
        if self.appointment_date and self.appointment_date < timezone.now().date():
            raise ValidationError({'appointment_date': "You cannot book an appointment in the past."})
            
        # 2. Prevent double booking for the same doctor and time
        if self.doctor and self.appointment_date and self.appointment_time:
            # Query for duplicate appointments
            duplicates = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date=self.appointment_date,
                appointment_time=self.appointment_time
            ).exclude(appointment_status='Cancelled') # Ignore cancelled ones
            
            # Exclude current instance if editing
            if self.pk:
                duplicates = duplicates.exclude(pk=self.pk)
                
            if duplicates.exists():
                raise ValidationError("This time slot is already booked for Dr. " + self.doctor.doctor_name + ". Please choose another slot.")

    def __str__(self):
        return f"{self.patient.patient_name} with Dr. {self.doctor.doctor_name} on {self.appointment_date} at {self.appointment_time}"
