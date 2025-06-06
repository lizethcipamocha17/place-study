"""webchatboot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  # Django Admin
                  path(settings.ADMIN_URL, admin.site.urls),
                  # Django Allauth
                  path('views/accounts/', include('apps.accounts.urls')),

                  path('api/', include('apps.accounts.api.urls'), name='accounts'),
                  path('api/', include('apps.schools.api.urls'), name='schools'),
                  path('api/', include('apps.contents.api.urls'), name='contents')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
