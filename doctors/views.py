from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Doctor
from .forms import DoctorForm
from departments.models import Department

def doctor_list(request):
    dept_id = request.GET.get('department')
    departments = Department.objects.all()
    if dept_id:
        doctors = Doctor.objects.filter(department_id=dept_id)
    else:
        doctors = Doctor.objects.all()
    return render(request, 'doctors/doctor_list.html', {
        'doctors': doctors,
        'departments': departments,
        'selected_dept': int(dept_id) if dept_id and dept_id.isdigit() else None
    })

def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor})

@login_required
def doctor_add(request):
    if not request.user.is_admin():
        messages.error(request, "Access denied. Only administrators can perform this action.")
        return redirect('doctor_list')
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor registered successfully.")
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'doctors/doctor_form.html', {'form': form, 'title': 'Add Doctor'})

@login_required
def doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    # Allow admin or the doctor themselves to edit
    if not request.user.is_admin() and (not request.user.is_doctor() or getattr(request.user, 'doctor_profile', None) != doctor):
        messages.error(request, "Access denied. You do not have permission to edit this profile.")
        return redirect('doctor_list')
    
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor profile updated successfully.")
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctors/doctor_form.html', {'form': form, 'title': 'Edit Doctor', 'doctor': doctor})

@login_required
def doctor_delete(request, pk):
    if not request.user.is_admin():
        messages.error(request, "Access denied. Only administrators can perform this action.")
        return redirect('doctor_list')
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        messages.success(request, "Doctor profile deleted successfully.")
        return redirect('doctor_list')
    return render(request, 'doctors/doctor_confirm_delete.html', {'doctor': doctor})

def load_doctors(request):
    department_id = request.GET.get('department_id')
    doctors = Doctor.objects.filter(department_id=department_id).order_by('doctor_name')
    # Custom serialization for values
    doctors_list = [{'id': doc.id, 'doctor_name': doc.doctor_name} for doc in doctors]
    return JsonResponse(doctors_list, safe=False)
