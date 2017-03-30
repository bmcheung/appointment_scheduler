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
from django.db.models import When, F, Q
from .models import Appointment
from .forms import UserForm, NewAppointmentForm, UpdateAppointmentForm
import datetime

from django.contrib.auth.models import User
# Create your views here.

def toCleanedTime(string):
    return ' '.join(string.split('T'))

def fromCleanedTime(string):
    return 'T'.join(string.split(' '))[:16]

def home(request):
    return redirect(reverse('scheduler:login'))

class Log_In(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect(reverse('scheduler:dashboard'))
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
    if request.user.is_authenticated():
        logout(request)
    return redirect('/')

class Dashboard(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        Appointment.objects.filter(time__lt=timezone.now(),status='Pending').update(status='Missed')
        todayappointments = Appointment.objects.filter(user=request.user,time__range=(datetime.datetime.combine(datetime.date.today(),datetime.time.min),datetime.datetime.combine(datetime.date.today(),datetime.time.max))).order_by('time')
        futureappointments = Appointment.objects.filter(user=request.user, time__gt=datetime.datetime.combine(datetime.date.today()+datetime.timedelta(days=1),datetime.time.min)).order_by('time')
        pastappointments = Appointment.objects.filter(user=request.user, time__lt=datetime.datetime.combine(datetime.date.today()-datetime.timedelta(days=1),datetime.time.max)).order_by('time')
        context = {}
        if todayappointments is not None:
            context['todayappointments'] = todayappointments
        if futureappointments is not None:
            context['futureappointments'] = futureappointments
        if pastappointments is not None:
            context['pastappointments'] = pastappointments
        return render(request, 'scheduler/dashboard.html', context)

class Detail(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request, pk):
        statuses = ['Pending', 'Missed', 'Completed']
        appointment = get_object_or_404(Appointment, pk = pk)
        appointment.time = fromCleanedTime(str(appointment.time))
        statuses.remove(appointment.status)
        context = {'appointment':appointment, 'statuses':statuses}
        return render(request, 'scheduler/detail.html', context)
    def post(self, request, pk):
        form = UpdateAppointmentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            data = form.cleaned_data
            appointment = Appointment.objects.get(pk = pk)
            appointment.time = toCleanedTime(str(request.POST['appointment_time']))
            appointment.appointment_text = data['appointment_text']
            appointment.status = data['status']
            appointment.save()
        else:
            print "went here"
        return redirect(reverse('scheduler:dashboard'))


class New(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        form = NewAppointmentForm()
        return render(request, 'scheduler/new.html', {'form':form})
    def post(self, request):
        time = toCleanedTime(str(request.POST['appointment_time']))
        form = NewAppointmentForm(request.POST)
        print form.is_valid()
        if form.is_valid() and request.user.is_authenticated():
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
