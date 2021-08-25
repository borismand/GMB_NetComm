from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.sign_in, name='login'),
    path('register/', views.register, name='register'),
    path('changepassword/', views.change_password, name='change_pass'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('clients/', views.add_customer, name='client'),
    path('logout/', views.sign_out, name='logout'),
    path("password_reset", views.password_reset_request, name="password_reset")
]

urlpatterns += staticfiles_urlpatterns()