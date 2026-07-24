import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicare.settings')
django.setup()

from django.contrib.auth import get_user_model
from departments.models import Department
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment

User = get_user_model()

def seed():
    print("Starting database seeding...")

    # 1. Create Portal Roles
    # Admin is already created, let's create Doctor, Patient, and Receptionist accounts
    
    # Receptionist
    receptionist_user, created = User.objects.get_or_create(
        username='receptionist',
        email='receptionist@medicare.com',
        defaults={'role': 'receptionist'}
    )
    if created:
        receptionist_user.set_password('receptionist123')
        receptionist_user.save()
        print("Created Receptionist user: receptionist / receptionist123")
    else:
        print("Receptionist user already exists.")

    # Doctor User
    doctor_user, created = User.objects.get_or_create(
        username='doctor',
        email='doctor@medicare.com',
        defaults={'role': 'doctor'}
    )
    if created:
        doctor_user.set_password('doctor123')
        doctor_user.save()
        print("Created Doctor User: doctor / doctor123")
    else:
        print("Doctor user already exists.")

    # Patient User
    patient_user, created = User.objects.get_or_create(
        username='patient',
        email='patient@medicare.com',
        defaults={'role': 'patient'}
    )
    if created:
        patient_user.set_password('patient123')
        patient_user.save()
        print("Created Patient User: patient / patient123")
    else:
        print("Patient user already exists.")

    # 2. Create Departments
    departments_data = [
        ("Cardiology", "Advanced diagnostics and therapeutic care for cardiovascular and heart health issues."),
        ("Neurology", "Comprehensive diagnosis and clinical therapies for neural systems and brain disorders."),
        ("Pediatrics", "Neonatal care, developmental support, growth safety, and childhood vaccinations."),
        ("Orthopedics", "Treatment for bone trauma, joints, sports medicine injuries, and spinal surgeries."),
        ("Dermatology", "Expert diagnosis and care for skin diseases, allergies, and cosmetic procedures."),
        ("Oncology", "Advanced cancer diagnostics, radiation oncology, chemotherapy, and tumor removals.")
    ]

    departments = {}
    for name, desc in departments_data:
        dept, created = Department.objects.get_or_create(
            department_name=name,
            defaults={'department_description': desc}
        )
        departments[name] = dept
        if created:
            print(f"Created Department: {name}")

    # 3. Create Doctor Profiles
    doctors_data = [
        {
            'doctor_name': 'Sarah Jenkins',
            'doctor_specialization': 'Chief Cardiologist',
            'qualification': 'MD, FACC, Harvard Medical School',
            'experience': 15,
            'phone': '+1 (212) 555-0101',
            'email': 'sjenkins@medicare.com',
            'consultation_fee': 150.00,
            'department': departments['Cardiology'],
            'available_days': 'Monday, Wednesday, Friday',
            'available_time': '09:00 AM - 01:00 PM',
            'user': doctor_user # Link our doctor user to this profile
        },
        {
            'doctor_name': 'Robert Smith',
            'doctor_specialization': 'Senior Neurologist',
            'qualification': 'MD, Ph.D. in Neuroscience, Johns Hopkins',
            'experience': 18,
            'phone': '+1 (212) 555-0102',
            'email': 'rsmith@medicare.com',
            'consultation_fee': 200.00,
            'department': departments['Neurology'],
            'available_days': 'Tuesday, Thursday',
            'available_time': '10:00 AM - 04:00 PM',
        },
        {
            'doctor_name': 'Jane Doe',
            'doctor_specialization': 'Pediatrician Specialist',
            'qualification': 'MD (Pediatrics), Stanford Residency',
            'experience': 12,
            'phone': '+1 (212) 555-0103',
            'email': 'jdoe@medicare.com',
            'consultation_fee': 120.00,
            'department': departments['Pediatrics'],
            'available_days': 'Monday, Tuesday, Wednesday, Thursday',
            'available_time': '02:00 PM - 06:00 PM',
        },
        {
            'doctor_name': 'Alan Cooper',
            'doctor_specialization': 'Orthopedic Surgeon',
            'qualification': 'MS (Ortho), DNB, Spinal Fellowship UK',
            'experience': 10,
            'phone': '+1 (212) 555-0104',
            'email': 'acooper@medicare.com',
            'consultation_fee': 130.00,
            'department': departments['Orthopedics'],
            'available_days': 'Wednesday, Friday',
            'available_time': '09:00 AM - 05:00 PM',
        }
    ]

    for doc_info in doctors_data:
        # Check if doctor profile already exists
        doc, created = Doctor.objects.get_or_create(
            email=doc_info['email'],
            defaults=doc_info
        )
        if created:
            print(f"Created Doctor Profile: Dr. {doc_info['doctor_name']}")
        else:
            # Update user if not linked
            if 'user' in doc_info and not doc.user:
                doc.user = doc_info['user']
                doc.save()

    # 4. Create Patient Profile for our patient user
    patient, created = Patient.objects.get_or_create(
        user=patient_user,
        defaults={
            'patient_name': 'John Miller',
            'patient_age': 35,
            'gender': 'Male',
            'patient_phone': '+1 (212) 555-0199',
            'patient_email': 'patient@medicare.com',
            'address': '789 Broadway Ave, Apt 4B, New York, NY 10003',
            'blood_group': 'O+',
            'patient_problem': 'Experiencing mild chest tightness during morning jogging and occasional breathing issues.'
        }
    )
    if created:
        print(f"Created Patient Profile: {patient.patient_name}")

    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed()
