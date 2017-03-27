from django import forms
from django.contrib.auth.models import User

from .models import Appointment

class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=16, required=True)
    password = forms.CharField(label='Password', min_length=8, required=True, widget=forms.PasswordInput())

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username','password']

class AppointmentForm(forms.Form):
    appointment_text = forms.CharField(label='Description', max_length=200, required=True)
    appointment_time = forms.DateTimeField(label='Date and Time', required=True, input_formats=['%Y-%m-%dT%H:%M'])
    status = forms.CharField(label='Status')

# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ['appointment_text', 'time']
