from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('changepassword/', views.change_password, name='change_pass'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('client/', views.add_customer, name='client')
]
