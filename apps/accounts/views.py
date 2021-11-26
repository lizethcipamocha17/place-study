from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, render


def login(request):
    return render(request, 'accounts/login.html')


def register(request):
    return render(request, 'accounts/register.html')


def reset_password(request):
    return HttpResponse('reset_password')


# Comprueba si el usuario actual esta autenticado para poder mostrar el dashboard
@login_required
def dashboard(request):
    return HttpResponse('Inicio')
