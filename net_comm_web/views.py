from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.safestring import mark_safe

from .form import RegisterForm, AddCustomerForm, ChangePassword
from .validators import *

# Create your views here.
from .models import Customer


def index(request):
    return render(request, "pages/index.html")


# A sign_in method which is SQLI vulnerable
# def sign_in(request):
#     if request.method == 'POST':
#         # Form Creation
#         form = AuthenticationForm(request.POST)
#
#         # Gather username and password as a string
#         username = request.POST['username']
#         password = request.POST['password']
#
#         '''
#         Create a raw sql query for gathering the user data from the DB
#         The username should be a existing one otherwise it will not be found on the DB
#         but the password can be whatever it can be as long as it has the ending: ' OR 1=1#
#         We user the user: Admin and password: 123wqeasd ' OR 1=1#
#         The symbol " ' " is used for separating between the password check and the OR 1=1 field.
#         The symbol " # " at the end of the query is mandatory for disabling the last apostrophe
#         '''
#
#         sql_query = f'SELECT * FROM auth_user WHERE username=\'{username}\' AND password=\'{password}\''
#         # Create a connector
#         cursor = connection.cursor()
#         # Execute the sql query on the database and authenticate with the received user if exists
#         if cursor.execute(sql_query):
#             user = User.objects.get(username=username)
#             login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             # Display the username logged in
#             messages.info(request, f'You are now logged in as {username}')
#             return redirect('/')
#         else:
#             # Error in case the username or password is incorrect
#             messages.error(request, "Login failed, this combination of username and password is incorrect")
#     else:
#         form = AuthenticationForm()
#     return render(request, "pages/login.html", {'login_form': form})

# Protected
def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            messages.info(request, f'You are now logged in as {username}')
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


# A register method which is SQLI vulnerable
# def register(request):
#     if request.method == 'POST':
#         # Create a form instance with the submitted data
#         form = RegisterForm(request.POST)
#         # Validate the form data
#         username = request.POST['username']
#         email = request.POST['email_address']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#
#         # Create raw SQL queries in order to check if the username or email is exists.
#         '''
#         The username validation in this form check if the user exists with the following query.
#         If the user exists, it will return its appearance from the DB.
#         If a user decides to exploit a SQLI attack he can use any username he wants and add " ' OR 1=1#"
#         and in the error about the user existence he will get a list of the registered usernames.
#         Same applies to the email address.
#         '''
#         username_query = f'SELECT username FROM auth_user WHERE username=\'{username}\''
#         email_query = f'SELECT email FROM auth_user WHERE email=\'{email}\''
#
#         # Create connections to the DB
#         username_cursor = connection.cursor()
#         email_cursor = connection.cursor()
#
#         # Execute the SQL queries in order to check the uniqueness of the username and email
#         if username_cursor.execute(username_query):
#             messages.error(request, f'A user with the username {username_cursor.fetchall()} already exist')
#             return HttpResponseRedirect("/register")
#         elif email_cursor.execute(email_query):
#             messages.error(request, f'A user with the email {email_cursor.fetchall()} already exist')
#             return HttpResponseRedirect("/register")
#
#         # Verify that the passwords are identical
#         elif password1 != password2:
#             messages.error(request, 'The passwords didn\'t match')
#             return HttpResponseRedirect("/register")
#         else:
#             # Register the user and log him in
#             user = form.save()
#             login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             messages.success(request, "Registration successful, You are now logged in")
#
#     form = RegisterForm()
#     return render(request=request, template_name="pages/register.html", context={"register_form": form})

# Protected
def register(request):
    if request.method == "POST":
        # Create a form instance with the submitted data
        form = RegisterForm(request.POST)

        # Validate the form
        if form.is_valid():
            # If the form is valid, save the user and login
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(
                request, "Registration successful, You are now logged in")
            # Redirect to homepage
            return redirect('/')
        messages.error(
            request, "Error, registration failed! Please verify the information is correct and try again")
        return HttpResponseRedirect("/register")
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
                    else:
                        u = User.objects.get(username=username)
                        u.set_password(confirm_new_password)
                        u.save()
                        messages.success(request, "The password has been changed successfully")
                        return redirect("/")
        else:
            form = ChangePassword()

    return render(request, "pages/changepassword.html", {'change_password_form': form})


# # A register method which is SQLI vulnerable
# def add_customer(request):
#     costs = {'200': 80, '500': 100, '1000': 130}
#     if request.user.is_authenticated:
#         customers = Customer.objects.all()
#         if request.method == 'POST':
#             form = AddCustomerForm(request.POST)
#             # Check the form validity
#             if form.is_valid():
#                 f_name = form.cleaned_data['first_name']
#                 l_name = form.cleaned_data['last_name']
#                 email = form.cleaned_data['email']
#                 personal_id = form.cleaned_data['personal_id']
#                 mobile_phone = form.cleaned_data['mobile_phone']
#                 subscription = form.cleaned_data['subscription']
#                 program_cost = costs[subscription]
#
#                 '''
#                 The email validation in this form check if the user exists with the following query.
#                 If the user exists, it will display its appearance from the DB.
#                 If a user decides to exploit a SQLI attack he can use any email he wants and add " ' OR 1=1#"
#                 and in the error about the user existence he will get a list of the registered emails.
#                 Same applies to the email address.
#                 '''
#                 email_query = f'SELECT email FROM net_comm_web_customer WHERE email=\'{email}\''
#                 personal_id_query = f'SELECT personal_id FROM net_comm_web_customer WHERE personal_id=\'{personal_id}\''
#
#                 # Create DB connectors
#                 email_cursor = connection.cursor()
#                 personal_id_cursor = connection.cursor()
#
#                 # Check if a customer with this email address exists
#                 if email_cursor.execute(email_query):
#                     messages.error(request, f'A customer with the email address: '
#                                             f'{email_cursor.fetchall()} already exists')
#                     return redirect('/clients')
#
#                 # Check if a customer with this personal_id exists
#                 if personal_id_cursor.execute(personal_id_query):
#                     messages.error(request, f'A customer with the personal_id: '
#                                             f'{personal_id_cursor.fetchall()} already exists')
#                     return redirect('/clients')
#                 try:
#                     customer = Customer.objects.create(f_name=f_name,
#                                                        l_name=l_name,
#                                                        email=email,
#                                                        personal_id=personal_id,
#                                                        mobile_num=mobile_phone,
#                                                        subscription=subscription,
#                                                        program_cost=program_cost)
#
#                     messages.success(
#                         request, f"You have successfully added a new client: {customer}.")
#                     # Redirect to clients page
#                     return render(request, "pages/clients.html", {'add_customer_form': form})
#                 except Exception as e:
#                     print(e)
#                     messages.error(request, "Error: could not create db record")
#             else:
#                 messages.error(request, "Error: form is not valid")
#         else:
#             form = AddCustomerForm()
#             return render(request, "pages/clients.html", {'add_customer_form': form, 'customers_table': customers})
#     else:
#         return render(request, "Errors/401.html")

# Protected
def add_customer(request):
    costs = {'200': 80, '500': 100, '1000': 130}
    form = AddCustomerForm()
    if request.user.is_authenticated:
        customers = Customer.objects.all()
        if request.method == 'POST':
            form = AddCustomerForm(request.POST)

            # Validate the form fields
            if form.is_valid():
                f_name = form.cleaned_data['first_name']
                l_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                personal_id = form.cleaned_data['personal_id']
                mobile_phone = form.cleaned_data['mobile_phone']
                subscription = form.cleaned_data['subscription']
                program_cost = costs[subscription]

                # Check if the customer with this email exists
                if Customer.objects.filter(email=email):
                    messages.error(request, 'A customer with this email address already exists')
                    return redirect('/clients')

                # Check if a customer with this personal_id exists
                if Customer.objects.filter(personal_id=personal_id):
                    messages.error(request, 'A customer with this personal_id already exists')
                    return redirect('/clients')

                # Add customer record to the DB

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
                    messages.error(request, "Error: could not create db record")
            else:
                messages.error(request, "Error: form is not valid")
        return render(request, "pages/clients.html", {'add_customer_form': form,
                                                      'customers_table': customers})
    else:
        return render(request, "Errors/401.html")
