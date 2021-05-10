from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.accounts.models import User


# class LoginForm(forms.Form):
#     email = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'date_of_birth', 'contact_email', 'email',
            'location', 'school', 'terms'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'autofocus': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'terms': forms.CheckboxInput(attrs={
                'class': 'custom-control-input'
            })

        }
