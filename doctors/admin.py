from django.contrib import admin
from django.utils.html import format_html
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'department', 'doctor_specialization', 'consultation_fee', 'phone', 'email', 'get_image_preview')
    search_fields = ('doctor_name', 'doctor_specialization', 'department__department_name')
    list_filter = ('department', 'available_days')
    readonly_fields = ('get_image_preview',)

    def get_image_preview(self, obj):
        if obj.doctor_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />', obj.doctor_image.url)
        return "No Image"
    get_image_preview.short_description = 'Preview'

