from django import forms
from django.core.exceptions import ValidationError
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email Address'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your message here...'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.strip()) < 2:
            raise ValidationError("Name must be at least 2 characters long.")
        return name

    def clean_message(self):
        msg = self.cleaned_data.get('message')
        if len(msg.strip()) < 10:
            raise ValidationError("Message must be at least 10 characters long.")
        return msg
