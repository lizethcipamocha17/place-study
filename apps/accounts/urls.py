# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# views
from apps.accounts.api.views import accounts_api, users
from apps.accounts import views

router = DefaultRouter()
router.register(r'v1/accounts', accounts_api.AccountViewSet, basename='accounts')
router.register(r'v1/users', users.UserViewSet, basename='users')
router.register(r'v1/users/teachers', users.TeacherViewSet, basename='users/teachers')


urlpatterns = [

    path('', views.dashboard, name='dashboard'),
    path('', include(router.urls))

]
