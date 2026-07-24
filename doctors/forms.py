from django import forms
from .models import Doctor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'doctor_name', 'doctor_specialization', 'qualification', 'experience',
            'doctor_image', 'phone', 'email', 'consultation_fee', 'department',
            'available_days', 'available_time'
        ]
        widgets = {
            'doctor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. John Doe'}),
            'doctor_specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Cardiologist'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. MD, FACC'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Years of experience'}),
            'doctor_image': forms.FileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Consultation fee'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'available_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Monday, Wednesday, Friday'}),
            'available_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 09:00 AM - 05:00 PM'}),
        }
