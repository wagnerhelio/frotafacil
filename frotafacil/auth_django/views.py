from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme

# Create your views here.

@login_required
def home(request):
    # Exemplo de contexto, ajuste conforme necessário
    context = {}
    return render(request, 'home.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect(reverse('home'))
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))
