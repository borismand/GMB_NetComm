from django import forms
from .models import Customer



class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=15)
    last_name = forms.CharField(max_length=15)
    email = forms.CharField()
    password = forms.PasswordInput()
    confirm_password = forms.PasswordInput()


class AddCustomerForm(forms.Form):
    first_name = forms.CharField(max_length=15)
    last_name = forms.CharField(max_length=15)
    email = forms.EmailField()
    personal_id = forms.IntegerField()
    mobile_phone = forms.CharField(max_length=14)
    subscription = forms.ChoiceField(choices=Customer.PROGRAM)
