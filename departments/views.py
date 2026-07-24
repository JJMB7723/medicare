from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Department
from .forms import DepartmentForm

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/department_list.html', {'departments': departments})

@login_required
def department_add(request):
    if not request.user.is_admin():
        messages.error(request, "Access denied. Only administrators can perform this action.")
        return redirect('department_list')
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department created successfully.")
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'departments/department_form.html', {'form': form, 'title': 'Add Department'})

@login_required
def department_edit(request, pk):
    if not request.user.is_admin():
        messages.error(request, "Access denied. Only administrators can perform this action.")
        return redirect('department_list')
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully.")
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'departments/department_form.html', {'form': form, 'title': 'Edit Department', 'department': department})

@login_required
def department_delete(request, pk):
    if not request.user.is_admin():
        messages.error(request, "Access denied. Only administrators can perform this action.")
        return redirect('department_list')
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, "Department deleted successfully.")
        return redirect('department_list')
    return render(request, 'departments/department_confirm_delete.html', {'department': department})
