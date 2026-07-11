from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from accounts.mixins import AdminRequiredMixin
from .models import ContactMessage
from .forms import ContactForm

class ContactView(SuccessMessageMixin, CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = 'contact/contact.html'
    success_url = reverse_lazy('contact:contact')
    success_message = "Your message was sent successfully! Our administrative team will reach out shortly."


class ContactMessagesListView(AdminRequiredMixin, ListView):
    model = ContactMessage
    template_name = 'contact/messages_list.html'
    context_object_name = 'contact_messages'
    ordering = ['-created_at']

