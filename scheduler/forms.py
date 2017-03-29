from django import forms
from django.contrib.auth.models import User

from .models import Appointment

class UserForm(forms.Form):
    username = forms.CharField(label='Username', min_length=4, max_length=16, required=True, error_messages={'required': 'Please enter a username', 'max_length': 'Usernames must contain 16 characters max.', 'min_length': 'Usernames must contain at least 4 characters.'})
    password = forms.CharField(label='Password', min_length=8, required=True, widget=forms.PasswordInput(), error_messages={'required': 'Please enter a password.', 'min_length': 'Passwords must contain at least 8 characters.'})

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username','password']

class AppointmentForm(forms.Form):
    appointment_text = forms.CharField(label='Description', max_length=200, required=True, error_messages={'required': 'Please enter an appointment.', 'max_length': 'Please enter a shorter appointment.'})
    appointment_time = forms.DateTimeField(label='Date and Time', required=True, input_formats=['%Y-%m-%dT%H:%M'], error_messages={'required': 'Please enter a date and time.'})
    status = forms.CharField(label='Status')

# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ['appointment_text', 'time']
