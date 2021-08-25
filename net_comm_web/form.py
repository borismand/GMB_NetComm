from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Customer


class RegisterForm(UserCreationForm):
    # For vulnerable registration form
    # email_address = forms.CharField()
    email_address = forms.EmailField()

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email_address']
        if commit:
            user.save()
        return user

    def clean(self):
        email = self.cleaned_data.get('email_address')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'email_address')


class AddCustomerForm(forms.Form):
    # XSS Vulnerable
    # first_name = forms.CharField()

    # XSS Protected by length limitation
    first_name = forms.CharField(max_length=15)
    last_name = forms.CharField(max_length=15)

    # SQLI Vulnerable
    # email = forms.CharField()
    # personal_id = forms.CharField()

    # Protected
    '''
    EmailField us protection from malicious inputs by validating the input.
    It checks everything that comes after the "@" sign and verifies that it complies with the conventions 
    of an email address
    '''
    email = forms.EmailField()
    personal_id = forms.IntegerField(min_value=100000000, max_value=999999999)
    mobile_phone = forms.CharField(max_length=14)
    subscription = forms.ChoiceField(choices=Customer.PROGRAM)


class ChangePassword(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_new_password = forms.CharField(widget=forms.PasswordInput())
