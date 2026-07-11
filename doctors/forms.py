from django import forms
from django.core.exceptions import ValidationError
from .models import Doctor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'user', 'doctor_name', 'doctor_specialization', 'qualification',
            'experience', 'doctor_image', 'phone', 'email', 'consultation_fee',
            'department', 'available_days', 'available_time'
        ]
        widgets = {
            'doctor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'doctor_specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Cardiologist'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. MD, PhD'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +1234567890'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'doctor@medicare.com'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'available_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mon, Wed, Fri'}),
            'available_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 09:00 AM - 01:00 PM'}),
            'user': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Simple phone verification: strip formatting characters and verify digits
        digits = ''.join(c for c in phone if c.isdigit())
        if len(digits) < 7 or len(digits) > 15:
            raise ValidationError("Please enter a valid phone number containing between 7 and 15 digits.")
        return phone

    def clean_experience(self):
        exp = self.cleaned_data.get('experience')
        if exp is not None and exp < 0:
            raise ValidationError("Years of experience cannot be negative.")
        return exp

    def clean_consultation_fee(self):
        fee = self.cleaned_data.get('consultation_fee')
        if fee is not None and fee < 0:
            raise ValidationError("Consultation fee cannot be negative.")
        return fee

    def clean_doctor_image(self):
        img = self.cleaned_data.get('doctor_image')
        if img:
            # File size limit check (e.g., 5MB)
            if img.size > 5 * 1024 * 1024:
                raise ValidationError("Image file size must not exceed 5MB.")
            # File extension check
            ext = img.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                raise ValidationError("Only JPG, JPEG, PNG, and WEBP image formats are supported.")
        return img
