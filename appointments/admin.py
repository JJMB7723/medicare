from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time', 'appointment_status', 'created_at')
    list_filter = ('appointment_status', 'appointment_date', 'doctor')
    search_fields = ('patient__patient_name', 'doctor__doctor_name', 'remarks')
    ordering = ('-appointment_date', '-appointment_time')
    actions = ['approve_appointments', 'cancel_appointments', 'complete_appointments']

    def approve_appointments(self, request, queryset):
        queryset.update(appointment_status='Approved')
    approve_appointments.short_description = "Approve selected appointments"

    def cancel_appointments(self, request, queryset):
        queryset.update(appointment_status='Cancelled')
    cancel_appointments.short_description = "Cancel selected appointments"

    def complete_appointments(self, request, queryset):
        queryset.update(appointment_status='Completed')
    complete_appointments.short_description = "Mark selected appointments as Completed"

