from django.db import models
from patients.models import Patient
from doctors.models import Doctor

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medical_records')
    diagnosis = models.TextField()
    prescription = models.TextField()
    report_file = models.FileField(upload_to='medical_reports/', blank=True, null=True)
    visit_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record for {self.patient.patient_name} - {self.diagnosis[:30]} ({self.visit_date})"

