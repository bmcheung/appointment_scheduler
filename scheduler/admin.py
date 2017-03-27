from django.contrib import admin
from .models import Appointment
# Register your models here.

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'appointment_text', 'time', 'status')



admin.site.register(Appointment, AppointmentAdmin)
