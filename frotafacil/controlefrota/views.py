from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'controlefrota/listar_veiculo.html')

def listar_veiculo(request):
    return render(request, 'controlefrota/listar_veiculo.html')