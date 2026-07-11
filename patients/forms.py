from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Patient

User = get_user_model()

class PatientRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = Patient
        fields = [
            'patient_name', 'patient_age', 'gender', 'patient_phone',
            'patient_email', 'address', 'blood_group', 'patient_problem'
        ]
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'patient_age': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'patient_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'patient_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'patient_problem': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Symptoms / complaint...'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_patient_email(self):
        email = self.cleaned_data.get('patient_email')
        if User.objects.filter(email=email).exists() or Patient.objects.filter(patient_email=email).exists():
            raise ValidationError("A user with this email address already exists.")
        return email

    def clean_patient_phone(self):
        phone = self.cleaned_data.get('patient_phone')
        digits = ''.join(c for c in phone if c.isdigit())
        if len(digits) < 7 or len(digits) > 15:
            raise ValidationError("Please enter a valid phone number containing between 7 and 15 digits.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise ValidationError({"confirm_password": "Passwords do not match."})
        return cleaned_data


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'patient_name', 'patient_age', 'gender', 'patient_phone',
            'patient_email', 'address', 'blood_group', 'patient_problem'
        ]
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_age': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'patient_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'patient_problem': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_patient_phone(self):
        phone = self.cleaned_data.get('patient_phone')
        digits = ''.join(c for c in phone if c.isdigit())
        if len(digits) < 7 or len(digits) > 15:
            raise ValidationError("Please enter a valid phone number containing between 7 and 15 digits.")
        return phone
