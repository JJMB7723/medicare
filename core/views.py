from django.views.generic import TemplateView
from .models import GalleryImage
from doctors.models import Doctor
from departments.models import Department
from patients.models import Patient
from appointments.models import Appointment

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()[:4]
        context['doctors'] = Doctor.objects.all()[:4]
        context['total_departments'] = Department.objects.count()
        context['total_doctors'] = Doctor.objects.count()
        context['total_patients'] = Patient.objects.count() + 120  # offset for demo stats
        context['total_appointments'] = Appointment.objects.count() + 350
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_images'] = GalleryImage.objects.all()
        return context

