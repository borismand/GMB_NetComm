"""
Django settings for GMB_NetComm project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import json
import random
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.


BASE_DIR = Path(__file__).resolve().parent.parent

# Use password requirements config file
with open(os.path.join(BASE_DIR, 'GMB_NetComm/sec_pass_req.json')) as f:
    PASS_MIN_REQUIREMENTS = json.load(f)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q#4f6s#svd(t1!gkz_m1s#jz_3ct_-d=c37ek-u@n(k4nifxma'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'net_comm_web',
    'crispy_forms',
    'django_password_validators',
    'django_password_validators.password_history'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'GMB_NetComm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./net_comm_web/Errors', './net_comm_web/pages'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'GMB_NetComm.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'CommunicationLTD',
        'USER': 'netcomm',
        'PASSWORD': 'Mf439&0$',
        'HOST': '3.12.123.251',
        'PORT': '3306'
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'net_comm_web.validators.NumberValidator'},
    {'NAME': 'net_comm_web.validators.UppercaseValidator'},
    {'NAME': 'net_comm_web.validators.LowercaseValidator'},
    {'NAME': 'net_comm_web.validators.SymbolValidator'},
    {'NAME': 'net_comm_web.validators.LengthValidator'},
    {
        'NAME': 'django_password_validators.password_history.password_validation.UniquePasswordsValidator',
        'OPTIONS': {
            'last_passwords': PASS_MIN_REQUIREMENTS['last_passwords']
        }
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tel_Aviv'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
# MEDIA_URL = '/assets/img/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
    '/var/www/static/',
]

PASSWORD_HASHERS = [
    # 'django.contrib.auth.hashers.PBKDF2_SHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]
