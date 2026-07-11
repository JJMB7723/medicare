from django import forms
from django.core.exceptions import ValidationError
import datetime
from .models import MedicalRecord
from doctors.models import Doctor

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'diagnosis', 'prescription', 'report_file', 'visit_date']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe symptoms and findings...'}),
            'prescription': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Provide medication instructions...'}),
            'report_file': forms.FileInput(attrs={'class': 'form-control'}),
            'visit_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'max': datetime.date.today().strftime('%Y-%m-%d')
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.role == 'Admin':
            self.fields['doctor'] = forms.ModelChoiceField(
                queryset=Doctor.objects.all(),
                widget=forms.Select(attrs={'class': 'form-select'}),
                required=True,
                empty_label="-- Select Doctor --"
            )

    def clean_report_file(self):
        report_file = self.cleaned_data.get('report_file')
        if report_file:
            if report_file.size > 10 * 1024 * 1024:
                raise ValidationError("Report file size must not exceed 10MB.")
            ext = report_file.name.split('.')[-1].lower()
            if ext not in ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx']:
                raise ValidationError("Only PDF, JPG, JPEG, PNG, DOC, and DOCX files are allowed.")
        return report_file

    def clean_visit_date(self):
        visit_date = self.cleaned_data.get('visit_date')
        if visit_date and visit_date > datetime.date.today():
            raise ValidationError("The visit date cannot be in the future.")
        return visit_date

