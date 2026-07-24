from django.contrib import admin
from .models import MedicalRecord

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'visit_date', 'created_at')
    list_filter = ('visit_date', 'doctor')
    search_fields = ('patient__patient_name', 'doctor__doctor_name', 'diagnosis', 'prescription')
    ordering = ('-visit_date',)
