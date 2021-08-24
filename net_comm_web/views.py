from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .form import RegisterForm, AddCustomerForm, ChangePassword, SearchUserForm
from .validators import *

# Create your views here.
from .models import Customer


def index(request):
    return render(request, "pages/index.html")


def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('/')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, "Login failed, this combination of username and password is incorrect")
    else:
        form = AuthenticationForm()
    return render(request, "pages/login.html", {'login_form': form})


def sign_out(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method == "POST":
        # Create a form instance with the submitted data
        form = RegisterForm(request.POST)

        # Validate the form
        if form.is_valid():
            print(form.errors)
            # If the form is valid, save the user and login
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(
                request, "Registration successful, You are now logged in")
            # Redirect to homepage
            return redirect('/')
        messages.error(
            request, "Error, registration failed! Please verify the information is correct and try again")
        print(form.errors)
        print(form.cleaned_data)
        return HttpResponseRedirect("/register")
        print(form.errors)
    form = RegisterForm()
    return render(request=request, template_name="pages/register.html", context={"register_form": form})


def change_password(request):
    if request.user.is_authenticated:
        username = request.user.get_username()
        if request.method == 'POST':
            form = ChangePassword(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                confirm_new_password = form.cleaned_data['confirm_new_password']
                if new_password != confirm_new_password:
                    form.add_error('confirm_new_password', 'The passwords do not match')
                else:
                    pass_check = validate_password_complexity(new_password)
                    num_of_not_valid = [item for item in pass_check if item is not True]
                    if len(num_of_not_valid) != 0:
                        form.add_error('new_password', num_of_not_valid)
                    # elif not PastPassValidator().validate(new_password, User.objects.get(username=request.user).id):
                    #     form.add_error('new_password', PastPassValidator().get_help_text())
                    else:
                        u = User.objects.get(username=username)
                        u.set_password(confirm_new_password)
                        u.save()
                        messages.success(request, "The password has been changed successfully")
                        return redirect("/")
        else:
            form = ChangePassword()

    return render(request, "pages/changepassword.html", {'change_password_form': form})


# def search_user(request):
#     form = SearchUserForm()
#     if request.method == 'POST':
#
#     return render(request, "pages/clients.html")


def add_customer(request):
    costs = {'200': 80, '500': 100, '1000': 130}
    form = AddCustomerForm()
    if request.user.is_authenticated:
        customers = Customer.objects.all()
        if request.method == 'POST':
            form = AddCustomerForm(request.POST)
            if form.is_valid():
                f_name = form.cleaned_data['first_name']
                l_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                personal_id = form.cleaned_data['personal_id']
                mobile_phone = form.cleaned_data['mobile_phone']
                subscription = form.cleaned_data['subscription']
                program_cost = costs[subscription]
                try:
                    customer = Customer.objects.create(f_name=f_name,
                                                       l_name=l_name,
                                                       email=email,
                                                       personal_id=personal_id,
                                                       mobile_num=mobile_phone,
                                                       subscription=subscription,
                                                       program_cost=program_cost)

                    messages.success(
                        request, f"You have successfully added a new client: {customer}.")
                    # Redirect to clients page
                    return render(request=request, template_name="pages/clients.html",
                                  context={'add_customer_form': form})
                except Exception as e:
                    print(e)
                    messages.error(request, "Error: could not create db record")
            else:
                messages.error(request, "Error: form is not valid")
        return render(request, "pages/clients.html", {'add_customer_form': form,
                                                      'customers_table': customers})
    else:
        return render(request, "Errors/401.html")
