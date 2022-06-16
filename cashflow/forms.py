from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import XMLUpload


class XMLForm(forms.ModelForm):
    class Meta:
        model = XMLUpload
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True})
        }
