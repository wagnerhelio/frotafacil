from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.conf import settings

# Create your views here.

PREFIX = settings.PREFIX

@login_required
def home(request):
    # Exemplo de contexto, ajuste conforme necessário
    context = {}
    context['PREFIX'] = PREFIX
    return render(request, 'home.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'registration/login.html', {'PREFIX': PREFIX})

@login_required
def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
