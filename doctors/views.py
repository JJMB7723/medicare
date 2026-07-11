from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from accounts.mixins import AdminRequiredMixin
from departments.models import Department
from .models import Doctor
from .forms import DoctorForm

class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctors/list.html'
    context_object_name = 'doctors'
    ordering = ['doctor_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        dept_id = self.request.GET.get('department')
        if dept_id:
            queryset = queryset.filter(department_id=dept_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        context['selected_dept'] = self.request.GET.get('department')
        return context

class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'doctors/detail.html'
    context_object_name = 'doctor'

class DoctorCreateView(AdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctors/form.html'
    success_url = reverse_lazy('doctors:list')
    success_message = "Dr. %(doctor_name)s profile was created successfully."

class DoctorUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctors/form.html'
    success_url = reverse_lazy('doctors:list')
    success_message = "Dr. %(doctor_name)s profile was updated successfully."

class DoctorDeleteView(AdminRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Doctor
    template_name = 'doctors/confirm_delete.html'
    success_url = reverse_lazy('doctors:list')
    success_message = "Doctor profile was deleted successfully."

