from django import forms
from django.contrib.auth import get_user_model
from .models import Patient

User = get_user_model()

class PatientRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Choose a password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}))

    class Meta:
        model = Patient
        fields = [
            'patient_name', 'patient_age', 'gender', 'patient_phone',
            'patient_email', 'address', 'blood_group', 'patient_problem'
        ]
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'patient_age': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Age'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'patient_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'patient_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Patient email'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full residential address'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'patient_problem': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your symptoms or medical concern'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken. Please choose another one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            role='patient'
        )
        
        patient = super().save(commit=False)
        patient.user = user
        if commit:
            patient.save()
        return patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'patient_name', 'patient_age', 'gender', 'patient_phone',
            'patient_email', 'address', 'blood_group', 'patient_problem'
        ]
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'patient_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'patient_problem': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
