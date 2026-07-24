from django import forms
from .models import Appointment
from doctors.models import Doctor
from departments.models import Department

class AppointmentForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_department'})
    )

    class Meta:
        model = Appointment
        fields = ['department', 'doctor', 'appointment_date', 'appointment_time', 'remarks']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-select', 'id': 'id_doctor'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe symptoms or reasons...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Default queryset is empty to enforce dynamic selection
        self.fields['doctor'].queryset = Doctor.objects.none()

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['doctor'].queryset = Doctor.objects.filter(department_id=department_id).order_by('doctor_name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.doctor:
            self.fields['department'].initial = self.instance.doctor.department
            self.fields['doctor'].queryset = Doctor.objects.filter(department=self.instance.doctor.department)
