from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from controlefrota.models_veiculo import Veiculo

@login_required
def home(request):
    # Calculate vehicle KPIs
    total_veiculo = Veiculo.objects.count()

    context = {
        'total': total_veiculo,
        'total_requisicoes': 0,  # You'll need to implement this when you add requisitions
        'requisicoes_pendentes': 0,
        'requisicoes_aprovadas': 0,
    }
    
    return render(request, 'home.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # redireciona para login após logout