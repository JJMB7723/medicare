from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Appointment
from .forms import AppointmentForm
from patients.models import Patient

@login_required
def appointment_list(request):
    user = request.user
    if user.is_admin() or user.is_receptionist():
        appointments = Appointment.objects.all().order_by('-appointment_date', '-appointment_time')
    elif user.is_doctor():
        doctor = getattr(user, 'doctor_profile', None)
        appointments = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date', '-appointment_time') if doctor else Appointment.objects.none()
    else:
        patient = getattr(user, 'patient_profile', None)
        appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date', '-appointment_time') if patient else Appointment.objects.none()
        
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

@login_required
def appointment_book(request):
    user = request.user
    patient = None
    if user.role == 'patient':
        patient = getattr(user, 'patient_profile', None)
        if not patient:
            messages.error(request, "You must complete your patient details before booking an appointment.")
            # Create a default profile if they register, or redirect to register profile
            # Let's redirect to patient_register for ease, but since they have user account, 
            # we should redirect to patient edit / register profile
            return redirect('patient_register')
            
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if 'department' in request.POST:
            from doctors.models import Doctor
            form.fields['doctor'].queryset = Doctor.objects.filter(department_id=request.POST.get('department'))
            
        if form.is_valid():
            appointment = form.save(commit=False)
            if user.role == 'patient':
                appointment.patient = patient
            else:
                patient_id = request.POST.get('patient_id')
                if not patient_id:
                    form.add_error(None, "Please select a patient for this appointment.")
                    return render(request, 'appointments/appointment_form.html', {
                        'form': form,
                        'patients': Patient.objects.all()
                    })
                appointment.patient = get_object_or_404(Patient, id=patient_id)
                
            try:
                appointment.full_clean()
                appointment.save()
                messages.success(request, "Appointment booked successfully.")
                return redirect('appointment_list')
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        if field == '__all__':
                            form.add_error(None, error)
                        else:
                            form.add_error(field, error)
    else:
        form = AppointmentForm()
        
    patients = Patient.objects.all() if user.role in ('admin', 'receptionist') else None
    return render(request, 'appointments/appointment_form.html', {
        'form': form,
        'patients': patients
    })

@login_required
def appointment_update_status(request, pk, status):
    appointment = get_object_or_404(Appointment, pk=pk)
    user = request.user
    
    if status not in ('Approved', 'Completed', 'Cancelled'):
        messages.error(request, "Invalid status transition.")
        return redirect('appointment_list')
        
    allowed = False
    if user.is_admin() or user.is_receptionist():
        allowed = True
    elif user.is_doctor():
        if getattr(user, 'doctor_profile', None) == appointment.doctor:
            allowed = True
    elif user.role == 'patient':
        if getattr(user, 'patient_profile', None) == appointment.patient and status == 'Cancelled':
            allowed = True
            
    if not allowed:
        messages.error(request, "You do not have permission to modify this appointment status.")
        return redirect('appointment_list')
        
    appointment.appointment_status = status
    appointment.save()
    messages.success(request, f"Appointment status updated to '{status}' successfully.")
    return redirect('appointment_list')

@login_required
def appointment_history(request):
    user = request.user
    if user.role == 'patient':
        patient = getattr(user, 'patient_profile', None)
        appointments = Appointment.objects.filter(patient=patient, appointment_status__in=('Completed', 'Cancelled')).order_by('-appointment_date') if patient else Appointment.objects.none()
    elif user.is_doctor():
        doctor = getattr(user, 'doctor_profile', None)
        appointments = Appointment.objects.filter(doctor=doctor, appointment_status__in=('Completed', 'Cancelled')).order_by('-appointment_date') if doctor else Appointment.objects.none()
    else:
        appointments = Appointment.objects.filter(appointment_status__in=('Completed', 'Cancelled')).order_by('-appointment_date')
        
    return render(request, 'appointments/appointment_history.html', {'appointments': appointments})
