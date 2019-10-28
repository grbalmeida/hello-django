from django.db import models
from django import forms
from contacts.models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('show',)
