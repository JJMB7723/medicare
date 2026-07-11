from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from accounts.mixins import DoctorOrAdminRequiredMixin
from .models import MedicalRecord
from .forms import MedicalRecordForm
from doctors.models import Doctor

class MedicalRecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'medical_records/list.html'
    context_object_name = 'records'

    def get_queryset(self):
        user = self.request.user
        if user.role in ['Admin', 'Receptionist']:
            return MedicalRecord.objects.all().order_by('-visit_date')
        elif user.role == 'Doctor':
            if hasattr(user, 'doctor_profile'):
                return MedicalRecord.objects.filter(doctor=user.doctor_profile).order_by('-visit_date')
            return MedicalRecord.objects.none()
        elif user.role == 'Patient':
            if hasattr(user, 'patient_profile'):
                return MedicalRecord.objects.filter(patient=user.patient_profile).order_by('-visit_date')
            return MedicalRecord.objects.none()
        return MedicalRecord.objects.none()


class MedicalRecordDetailView(LoginRequiredMixin, DetailView):
    model = MedicalRecord
    template_name = 'medical_records/detail.html'
    context_object_name = 'record'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        
        # Privacy controls: Patients can only see their own records. Doctors can only see theirs.
        if user.role == 'Patient' and (not hasattr(user, 'patient_profile') or obj.patient != user.patient_profile):
            raise PermissionDenied("You do not have permission to view this medical record.")
        
        if user.role == 'Doctor' and (not hasattr(user, 'doctor_profile') or obj.doctor != user.doctor_profile):
            raise PermissionDenied("You do not have permission to view this medical record.")
            
        return obj


class MedicalRecordCreateView(DoctorOrAdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'medical_records/form.html'
    success_url = reverse_lazy('medical_records:list')
    success_message = "Medical record added successfully."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        record = form.save(commit=False)
        user = self.request.user
        if user.role == 'Doctor':
            record.doctor = user.doctor_profile
        # If user is Admin, doctor is set by the form field
        record.save()
        return super().form_valid(form)

