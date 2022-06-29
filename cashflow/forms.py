from django import forms
from django.contrib.auth.models import User

from .models import XMLUpload, Profile

#class LoginForm(forms.Form):
#    username = forms.CharField()
#    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password dont\' match')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['piva', 'photo']

class XMLForm(forms.ModelForm):
    class Meta:
        model = XMLUpload
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True, 'class' : 'form-control' })
        }
        labels = {
            'file': 'Upload Files',
            'comment': 'Select one or many files'
            }
        help_texts = {
            'comment': 'Is possible to upload all the file together '
            },
        localized_fields = '__all__'
