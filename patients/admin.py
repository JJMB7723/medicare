from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'patient_age', 'gender', 'patient_phone', 'patient_email', 'blood_group', 'created_at')
    search_fields = ('patient_name', 'patient_email', 'patient_phone')
    list_filter = ('gender', 'blood_group', 'created_at')
    ordering = ('-created_at',)

