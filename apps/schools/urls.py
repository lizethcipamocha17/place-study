from django.urls import path, include
from apps.schools.api.views import views

# Django REST Framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'v1/schools', views.SchoolViewSet, basename='schools')


urlpatterns = [
    path('schools', views.school_list),
    path('', include(router.urls))
]