
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.schools.models import Content

# def login(request):
#     return render(request, 'account/login.html')

# Comprueba si el usuario actual esta autenticado para poder mostrar el dashboard
@login_required
def dashboard(request):
    content = Content.objects.all()
    return render(request, 'accounts/dashboard.html', {"contents": content})