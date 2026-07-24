from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from departments.models import Department
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment

def home(request):
    departments = Department.objects.all()[:4]
    doctors = Doctor.objects.all()[:4]
    
    # Hospital statistics
    stats = {
        'departments_count': Department.objects.count(),
        'doctors_count': Doctor.objects.count(),
        'patients_count': Patient.objects.count(),
        'appointments_count': Appointment.objects.count(),
    }
    
    return render(request, 'core/home.html', {
        'departments': departments,
        'doctors': doctors,
        'stats': stats,
    })

def about(request):
    return render(request, 'core/about.html')

@login_required
def dashboard(request):
    user = request.user
    context = {}
    
    if user.is_admin():
        # Administrator view
        context['stats'] = {
            'patients': Patient.objects.count(),
            'doctors': Doctor.objects.count(),
            'appointments': Appointment.objects.count(),
            'departments': Department.objects.count(),
        }
        context['recent_appointments'] = Appointment.objects.order_by('-created_at')[:5]
        
    elif user.is_doctor():
        # Doctor view
        doctor = getattr(user, 'doctor_profile', None)
        if doctor:
            context['doctor'] = doctor
            context['appointments'] = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date', '-appointment_time')
            context['patients'] = Patient.objects.filter(appointments__doctor=doctor).distinct()
            
    elif user.is_receptionist():
        # Receptionist view
        context['stats'] = {
            'patients': Patient.objects.count(),
            'appointments_pending': Appointment.objects.filter(appointment_status='Pending').count(),
            'appointments_approved': Appointment.objects.filter(appointment_status='Approved').count(),
        }
        context['recent_appointments'] = Appointment.objects.order_by('-created_at')[:10]
        
    else:
        # Patient view
        patient = getattr(user, 'patient_profile', None)
        if patient:
            context['patient'] = patient
            context['appointments'] = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
            
    return render(request, 'core/dashboard.html', context)
