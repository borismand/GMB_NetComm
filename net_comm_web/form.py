from django import forms
from .models import Program


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=15)
    last_name = forms.CharField(max_length=15)
    email = forms.EmailField()
    personal_id = forms.IntegerField(min_value=100000000, max_value=999999999)
    mobile_phone = forms.CharField(max_length=14)
    password = forms.PasswordInput()
    confirm_password = forms.PasswordInput()


class AddCustomerForm(forms.Form):
    first_name = forms.CharField(max_length=15)
    last_name = forms.CharField(max_length=15)
    email = forms.EmailField()
    personal_id = forms.IntegerField(min_value=100000000, max_value=999999999)
    mobile_phone = forms.CharField(max_length=14)
    subscription = forms.ChoiceField(choices=Program.PROGRAM)
