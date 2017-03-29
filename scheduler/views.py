# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Appointment
from .forms import UserForm, AppointmentForm
import datetime

from django.contrib.auth.models import User
# Create your views here.

def home(request):
    return redirect(reverse('scheduler:login'))

class Log_In(View):
    def get(self, request):
        form = UserForm()
        return render(request, 'scheduler/login.html', {'form':form})

    def post(self, request):
        form = UserForm(request.POST)
        form_type = request.POST['extra']
        if form.is_valid():
            data = form.cleaned_data
            if form_type == '0':
                try:
                    user = User.objects.create_user(username = data['username'], password = data['password'])
                    if user is not None:
                        login(request, user)
                        return redirect(reverse('scheduler:dashboard'))
                except:
                    messages.add_message(request, messages.ERROR, 'Username must be unique.')
            elif form_type == '1':
                user = authenticate(username=data['username'], password=data['password'])
                if user is not None:
                    login(request, user)
                    return redirect(reverse('scheduler:dashboard'))
                else:
                    messages.add_message(request, messages.ERROR, 'Username or password is incorrect')
        return redirect(reverse('scheduler:home'))

def log_out(request):
    logout(request)
    return redirect('/')

class Dashboard(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        appointments = Appointment.objects.filter(user=request.user)
        if appointments is not None:
            # print appointments
            context = {
                'appointments':appointments
            }
        else:
            context = {}
        return render(request, 'scheduler/dashboard.html', context)
    # def post(self, request):
    #     return redirect(reverse('scheduler:home'))


class Detail(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request, pk):
        statuses = ['Pending', 'Missed', 'Completed']
        appointment = get_object_or_404(Appointment, pk = pk)
        statuses.remove(appointment.status)
        context = {'appointment':appointment, 'statuses':statuses}
        return render(request, 'scheduler/detail.html', context)
    def post(self, request, pk):
        time = str(request.POST['appointment_time'])
        time = ' '.join(time.split('T'))
        form = AppointmentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            data = form.cleaned_data
            appointment = Appointment.objects.get(pk = pk)
            appointment.time = time
            appointment.appointment_text = data['appointment_text']
            appointment.status = data['status']
            appointment.save()
        return redirect(reverse('scheduler:dashboard'))


class New(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        form = AppointmentForm()
        return render(request, 'scheduler/new.html', {'form':form})
    def post(self, request):
        time = str(request.POST['appointment_time'])
        time = ' '.join(time.split('T'))
        form = AppointmentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            data = form.cleaned_data
            appointment = Appointment.objects.create(user = request.user,appointment_text = data['appointment_text'],time = time)
        else:
            return redirect(reverse('scheduler:new'))
        return redirect(reverse('scheduler:dashboard'))

class Delete(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request, pk):
        appointment = Appointment.objects.get(pk = pk)
        return render(request, 'scheduler/delete.html', {'appointment':appointment})
    def post(self, request, pk):
        Appointment.objects.get(pk=pk).delete()
        return redirect(reverse('scheduler:dashboard'))
