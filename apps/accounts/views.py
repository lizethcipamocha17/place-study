from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.accounts.models import User
from apps.schools.models import Content


# def login(request):
#     return render(request, 'account/login.html')

# Comprueba si el usuario actual esta autenticado para poder mostrar el dashboard
@login_required
def dashboard(request):
    content = Content.objects.all()
    return render(request, 'accounts/dashboard.html', {"contents": content})


@login_required
def validation_acount(request):
    user = User.objects.all()
    return render(request, '/accounts/emails/account_activation.html', {"users": user})
