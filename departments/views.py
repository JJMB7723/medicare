from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from accounts.mixins import AdminRequiredMixin
from .models import Department
from .forms import DepartmentForm

class DepartmentListView(ListView):
    model = Department
    template_name = 'departments/list.html'
    context_object_name = 'departments'
    ordering = ['department_name']

class DepartmentCreateView(AdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/form.html'
    success_url = reverse_lazy('departments:list')
    success_message = "Department '%(department_name)s' was created successfully."

class DepartmentUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/form.html'
    success_url = reverse_lazy('departments:list')
    success_message = "Department '%(department_name)s' was updated successfully."

class DepartmentDeleteView(AdminRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Department
    template_name = 'departments/confirm_delete.html'
    success_url = reverse_lazy('departments:list')
    success_message = "Department was deleted successfully."

