from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

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
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'registration/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
