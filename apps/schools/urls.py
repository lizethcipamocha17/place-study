from django.urls import path
from apps.schools import views

urlpatterns = [
    path('schools', views.school_list),
]