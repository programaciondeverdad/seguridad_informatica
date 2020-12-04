from django.contrib import admin
from django.urls import path


from django.conf.urls import include, url

from . import views

urlpatterns = [
     url(r'^$', views.welcome, name='index'),
    path('register', views.register),
    path('login', views.login, name='login_path'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),

    
]