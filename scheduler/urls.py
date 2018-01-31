from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'scheduler'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^scheduler/login/$', views.Log_In.as_view(), name='login'),
    url(r'^scheduler/dashboard/$', views.Dashboard.as_view(), name='dashboard'),
    url(r'^scheduler/dashboard/detail/(?P<pk>[0-9]+)/$', views.Detail.as_view(), name='detail'),
    url(r'^scheduler/dashboard/new/$', views.New.as_view(), name='new'),
    url(r'^scheduler/dashboard/delete/(?P<pk>[0-9]+)/$', views.Delete.as_view(), name='delete'),
    url(r'^scheduler/logout$', views.log_out, name='logout'),
    url(r'^test$', views.Test.as_view(), name='test'),
    # url(r'^scheduler', views.Log_In.as_view(), name='login'),
]
