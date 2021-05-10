from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# def login(request):
#     return render(request, 'account/login.html')


# Comprueba si el usuario actual esta autenticado para poder mostrar el dashboard
@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'section': 'dashboard'})
