# Django
from django.urls import include, path

from apps.accounts import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]