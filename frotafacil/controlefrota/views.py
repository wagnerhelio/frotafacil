from django.shortcuts import render
from django.conf import settings

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'controlefrota/listar_veiculo.html', {'PREFIX': settings.PREFIX})

def listar_veiculo(request):
    return render(request, 'controlefrota/listar_veiculo.html', {'PREFIX': settings.PREFIX})