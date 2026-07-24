from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MedicalRecord
from .forms import MedicalRecordForm
from patients.models import Patient

@login_required
def record_list(request):
    user = request.user
    if user.is_admin():
        records = MedicalRecord.objects.all().order_by('-visit_date')
    elif user.is_doctor():
        doctor = getattr(user, 'doctor_profile', None)
        records = MedicalRecord.objects.filter(doctor=doctor).order_by('-visit_date') if doctor else MedicalRecord.objects.none()
    elif user.role == 'patient':
        patient = getattr(user, 'patient_profile', None)
        records = MedicalRecord.objects.filter(patient=patient).order_by('-visit_date') if patient else MedicalRecord.objects.none()
    else:
        messages.error(request, "Access denied.")
        return redirect('dashboard')
        
    return render(request, 'medical_records/record_list.html', {'records': records})

@login_required
def record_add(request, patient_id):
    user = request.user
    if not user.is_admin() and not user.is_doctor():
        messages.error(request, "Access denied. Only doctors and administrators can add medical records.")
        return redirect('dashboard')
        
    patient = get_object_or_404(Patient, pk=patient_id)
    doctor = getattr(user, 'doctor_profile', None)
    
    if user.is_doctor() and not doctor:
        messages.error(request, "You must have an active Doctor profile to perform this action.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            if user.is_doctor():
                record.doctor = doctor
            else:
                from doctors.models import Doctor
                first_doctor = Doctor.objects.first()
                if not first_doctor:
                    messages.error(request, "No doctors available in the system. Add a doctor first.")
                    return redirect('dashboard')
                record.doctor = first_doctor
                
            record.save()
            messages.success(request, f"Medical record for {patient.patient_name} added successfully.")
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = MedicalRecordForm()
        
    return render(request, 'medical_records/record_form.html', {
        'form': form,
        'patient': patient
    })

@login_required
def record_detail(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    user = request.user
    
    allowed = False
    if user.is_admin():
        allowed = True
    elif user.is_doctor() and getattr(user, 'doctor_profile', None) == record.doctor:
        allowed = True
    elif user.role == 'patient' and getattr(user, 'patient_profile', None) == record.patient:
        allowed = True
        
    if not allowed:
        messages.error(request, "Access denied.")
        return redirect('dashboard')
        
    return render(request, 'medical_records/record_detail.html', {'record': record})
