from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from appointments.models import Appointment
from patients.models import Patient
from doctors.models import Doctor
from departments.models import Department
from medical_records.models import MedicalRecord
from contact.models import ContactMessage

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        role = user.role

        if role in ['Admin', 'Receptionist']:
            # Administrative Dashboard
            context['total_appointments'] = Appointment.objects.count()
            context['pending_appointments'] = Appointment.objects.filter(appointment_status='Pending').count()
            context['total_doctors'] = Doctor.objects.count()
            context['total_patients'] = Patient.objects.count()
            context['total_departments'] = Department.objects.count()
            
            # Recent items
            context['recent_appointments'] = Appointment.objects.all().order_by('-created_at')[:5]
            context['recent_patients'] = Patient.objects.all().order_by('-created_at')[:5]
            context['recent_messages'] = ContactMessage.objects.all().order_by('-created_at')[:5]

        elif role == 'Doctor':
            # Doctor Dashboard
            try:
                doctor = user.doctor_profile
                context['doctor'] = doctor
                context['appointments'] = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date', '-appointment_time')
                context['total_patients'] = Patient.objects.filter(appointments__doctor=doctor).distinct().count()
                context['medical_records'] = MedicalRecord.objects.filter(doctor=doctor).order_by('-visit_date')
            except Doctor.DoesNotExist:
                context['doctor'] = None
                context['appointments'] = []
                context['total_patients'] = 0
                context['medical_records'] = []

        elif role == 'Patient':
            # Patient Dashboard
            try:
                patient = user.patient_profile
                context['patient'] = patient
                context['appointments'] = Appointment.objects.filter(patient=patient).order_by('-appointment_date', '-appointment_time')
                context['medical_records'] = MedicalRecord.objects.filter(patient=patient).order_by('-visit_date')
            except Patient.DoesNotExist:
                context['patient'] = None
                context['appointments'] = []
                context['medical_records'] = []

        return context

