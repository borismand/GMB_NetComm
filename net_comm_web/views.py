from django.shortcuts import render, redirect
from .form import RegisterForm

# Create your views here.


def index(request):
    return render(request, "pages/index.html")


def login(request):
    return render(request, "pages/login.html")


def register(request):
    form = RegisterForm()
    return render(request, "pages/register.html", {'register_form': form})


def change_password(request):
    return render(request, "pages/changepassword.html")


def dashboard(request):
    return render(request, "pages/dashboard.html")
