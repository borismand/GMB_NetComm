from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Customer


class RegisterForm(UserCreationForm):

    email_address = forms.EmailField()

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email_address']
        print(user)
        if commit:
            user.save()
            print("Saving")
        return user

    def clean(self):
        email = self.cleaned_data.get('email_address')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'email_address', 'password1', 'password2')




class AddCustomerForm(forms.Form):
    first_name = forms.CharField(max_length=15)
    last_name = forms.CharField(max_length=15)
    email = forms.EmailField()
    personal_id = forms.IntegerField(min_value=100000000, max_value=999999999)
    mobile_phone = forms.CharField(max_length=14)
    subscription = forms.ChoiceField(choices=Customer.PROGRAM)


class ChangePassword(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_new_password = forms.CharField(widget=forms.PasswordInput())
