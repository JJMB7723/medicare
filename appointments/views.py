from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from accounts.mixins import ReceptionistOrAdminRequiredMixin
from patients.models import Patient
from .models import Appointment
from .forms import AppointmentBookingForm

class AppointmentBookView(LoginRequiredMixin, FormView):
    template_name = 'appointments/book.html'
    form_class = AppointmentBookingForm
    success_url = reverse_lazy('accounts:dashboard')

    def dispatch(self, request, *args, **kwargs):
        # Ensure user is a Patient and has a patient profile
        if request.user.role != 'Patient':
            messages.error(request, "Only registered patients can book appointments online.")
            return redirect('accounts:dashboard')
        try:
            request.user.patient_profile
        except Patient.DoesNotExist:
            messages.error(request, "Please register your patient profile details before booking an appointment.")
            return redirect('patients:register')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        appointment = form.save(commit=False)
        appointment.patient = self.request.user.patient_profile
        appointment.appointment_status = 'Pending'
        appointment.save()
        messages.success(self.request, f"Your appointment with Dr. {appointment.doctor.doctor_name} has been booked. Please wait for approval.")
        return super().form_valid(form)


class AppointmentHistoryView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/history.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        # Patients see only their own history
        if hasattr(self.request.user, 'patient_profile'):
            return Appointment.objects.filter(patient=self.request.user.patient_profile).order_by('-appointment_date', '-appointment_time')
        return Appointment.objects.none()


class AppointmentListView(ReceptionistOrAdminRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/list.html'
    context_object_name = 'appointments'
    ordering = ['-appointment_date', '-appointment_time']


class AppointmentStatusUpdateView(ReceptionistOrAdminRequiredMixin, View):
    def post(self, request, pk, status, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk)
        if status in ['Approved', 'Completed', 'Cancelled']:
            appointment.appointment_status = status
            appointment.save()
            messages.success(request, f"Appointment status updated to '{status}' successfully.")
        else:
            messages.error(request, "Invalid status choice.")
        
        # Redirect back to the referrer or dashboard
        return redirect(request.META.get('HTTP_REFERER', 'accounts:dashboard'))

