from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('receptionist', 'Receptionist'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')

    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    def is_doctor(self):
        return self.role == 'doctor'

    def is_patient(self):
        return self.role == 'patient'

    def is_receptionist(self):
        return self.role == 'receptionist'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
