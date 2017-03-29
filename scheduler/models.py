from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Appointment(models.Model):
    def __str__(self):
        return self.appointment_text
    def appointment_was_missed(self):
        now = timezone.now()
        return now > self.time and self.status == 'Pending'

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='related user')
    appointment_text = models.CharField('appointment description', max_length=200)
    time = models.DateTimeField('scheduled time')
    status = models.CharField('appointment status', max_length=30, default='Pending')
