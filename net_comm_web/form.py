from django import forms


class RegisterForm(forms.Form):
    full_name = forms.CharField()
    email = forms.CharField()
    password = forms.PasswordInput()
    confirm_password = forms.PasswordInput()

