from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import User
from accounts.mixins import ReceptionistOrAdminRequiredMixin
from .models import Patient
from .forms import PatientRegistrationForm, PatientForm

class PatientRegisterView(FormView):
    template_name = 'patients/register.html'
    form_class = PatientRegistrationForm
    success_url = reverse_lazy('accounts:dashboard')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['patient_email']

        # Create user account with Patient role
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='Patient'
        )

        # Create patient record linked to the user
        patient = form.save(commit=False)
        patient.user = user
        patient.save()

        # Automatically log the patient in
        login(self.request, user)

        messages.success(self.request, f"Welcome {patient.patient_name}! Your patient portal account has been registered successfully.")
        return super().form_valid(form)


class PatientListView(ReceptionistOrAdminRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/list.html'
    context_object_name = 'patients'
    ordering = ['-created_at']


class PatientUpdateView(ReceptionistOrAdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/form.html'
    success_url = reverse_lazy('patients:list')
    success_message = "Patient details updated successfully."

