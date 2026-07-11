from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
from .models import Appointment
from doctors.models import Doctor
from departments.models import Department

class AppointmentBookingForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_department'}),
        required=True,
        empty_label="-- Select Department --"
    )

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time', 'remarks']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-select', 'id': 'id_doctor'}),
            'appointment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': datetime.date.today().strftime('%Y-%m-%d')
            }),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional remarks or reasons for visit...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].empty_label = "-- Select Doctor --"
        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['doctor'].queryset = Doctor.objects.filter(department_id=department_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.doctor:
            self.fields['department'].initial = self.instance.doctor.department
            self.fields['doctor'].queryset = Doctor.objects.filter(department=self.instance.doctor.department)

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time = cleaned_data.get('appointment_time')

        if appointment_date and appointment_date < datetime.date.today():
            self.add_error('appointment_date', "You cannot book an appointment for a past date.")

        if doctor and appointment_date and appointment_time:
            # Prevent double booking for same doctor at same date and time
            overlap = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time
            ).exclude(appointment_status='Cancelled')
            
            if self.instance.pk:
                overlap = overlap.exclude(pk=self.instance.pk)

            if overlap.exists():
                raise ValidationError("This doctor is already booked for this specific date and time.")
        return cleaned_data
