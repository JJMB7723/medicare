from django.db import models
from django.conf import settings
from departments.models import Department

class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctor_profile'
    )
    doctor_name = models.CharField(max_length=100)
    doctor_specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    experience = models.PositiveIntegerField(help_text="Experience in years")
    doctor_image = models.ImageField(upload_to='doctors/', blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='doctors')
    available_days = models.CharField(max_length=100, help_text="e.g. Monday, Wednesday, Friday")
    available_time = models.CharField(max_length=100, help_text="e.g. 09:00 AM - 01:00 PM")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.doctor_name} ({self.department.department_name})"

