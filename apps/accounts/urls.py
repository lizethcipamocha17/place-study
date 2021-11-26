# Django
from django.urls import path

from apps.accounts import views

urlpatterns = [
    path('login', views.login, name="Login"),
    path('register', views.register, name="Register"),
    path('reset_password', views.reset_password, name="Reset Password"),
    path('', views.dashboard, name='dashboard'),
]
