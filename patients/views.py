from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Patient
from .forms import PatientRegistrationForm, PatientForm

@login_required
def patient_list(request):
    if request.user.role not in ('admin', 'doctor', 'receptionist'):
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    patients = Patient.objects.all().order_by('-created_at')
    return render(request, 'patients/patient_list.html', {'patients': patients})

def patient_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save()
            login(request, patient.user)
            messages.success(request, f"Registration successful! Welcome to MediCare, {patient.patient_name}.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = PatientRegistrationForm()
    return render(request, 'patients/patient_register.html', {'form': form})

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if not request.user.is_admin() and not request.user.is_doctor() and not request.user.is_receptionist() and getattr(request.user, 'patient_profile', None) != patient:
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    
    appointments = patient.appointments.all().order_by('-appointment_date')
    medical_records = patient.medical_records.all().order_by('-visit_date')
    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'appointments': appointments,
        'medical_records': medical_records
    })

@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if not request.user.is_admin() and not request.user.is_receptionist() and getattr(request.user, 'patient_profile', None) != patient:
        messages.error(request, "Access denied.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient details updated successfully.")
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_form.html', {'form': form, 'patient': patient})

@login_required
def patient_delete(request, pk):
    if not request.user.is_admin():
        messages.error(request, "Access denied. Only administrators can delete records.")
        return redirect('patient_list')
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        if patient.user:
            patient.user.delete()
        else:
            patient.delete()
        messages.success(request, "Patient record and account deleted successfully.")
        return redirect('patient_list')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})
