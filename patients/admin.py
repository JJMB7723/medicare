from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'patient_age', 'gender', 'patient_phone', 'patient_email', 'blood_group', 'created_at')
    list_filter = ('gender', 'blood_group')
    search_fields = ('patient_name', 'patient_phone', 'patient_email', 'patient_problem')
    ordering = ('-created_at',)
