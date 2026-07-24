from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'department', 'doctor_specialization', 'consultation_fee', 'image_preview')
    list_filter = ('department', 'doctor_specialization')
    search_fields = ('doctor_name', 'doctor_specialization', 'qualification', 'phone', 'email')
    ordering = ('doctor_name',)
    
    def image_preview(self, obj):
        if obj.doctor_image:
            return mark_safe(f'<img src="{obj.doctor_image.url}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />')
        return "No Image"
    image_preview.short_description = 'Photo'
