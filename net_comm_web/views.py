from django.shortcuts import render, redirect

from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.db import connection
from django.contrib.auth.models import User


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
