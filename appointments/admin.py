from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time', 'appointment_status', 'created_at')
    list_filter = ('appointment_status', 'appointment_date', 'doctor', 'doctor__department')
    search_fields = ('patient__patient_name', 'doctor__doctor_name', 'remarks')
    ordering = ('-appointment_date', '-appointment_time')
    actions = ['approve_appointments', 'cancel_appointments']

    def approve_appointments(self, request, queryset):
        queryset.update(appointment_status='Approved')
        self.message_user(request, "Selected appointments have been approved.")
    approve_appointments.short_description = "Approve selected appointments"

    def cancel_appointments(self, request, queryset):
        queryset.update(appointment_status='Cancelled')
        self.message_user(request, "Selected appointments have been cancelled.")
    cancel_appointments.short_description = "Cancel selected appointments"
