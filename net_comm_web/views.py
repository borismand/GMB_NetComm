from django.shortcuts import render, redirect

# Create your views here.


def index(request):
    return render(request, "pages/index.html")


def login(request):
    return render(request, "pages/login.html")


def register(request):
    return render(request, "pages/register.html")


def change_password(request):
    return render(request, "pages/changepassword.html")


def dashboard(request):
    return render(request, "pages/dashboard.html")
