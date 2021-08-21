from django.shortcuts import render, redirect
from django.contrib import messages
from .form import RegisterForm, AddCustomerForm, LoginForm

# Create your views here.
from .models import Customer, Program


def index(request):
    return render(request, "pages/index.html")


def login(request):
    form = LoginForm()
    return render(request, "pages/login.html", {'login_form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm()


    return render(request, "pages/register.html", {'register_form': form})


def change_password(request):
    return render(request, "pages/changepassword.html")


def dashboard(request):
    return render(request, "pages/dashboard.html")


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
                    program = Program.objects.create(subscription=subscription,
                                                     program_cost=program_cost)

                    customer = Customer.objects.create(f_name=f_name,
                                                       l_name=l_name,
                                                       email=email,
                                                       personal_id=personal_id,
                                                       mobile_num=mobile_phone,
                                                       related_program=program)

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

