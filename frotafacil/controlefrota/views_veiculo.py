from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from forms_veiculo import CadastrarVeiculoForm, EditarVeiculoForm, ListarVeiculoForm, ExcluirVeiculoForm
from models_veiculo import Veiculo 

@login_required
def cadastrar_veiculo_views(request):
    if request.method == 'POST':
        form = CadastrarVeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_veiculos')
    else:
        form = CadastrarVeiculoForm()
    return render(request, 'cadastrar_veiculos.html', {'form': form})

@login_required
def editar_veiculo_view(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)

    if request.method == 'POST':
        form = EditarVeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            return redirect('listar_veiculos')
    else:
        form = EditarVeiculoForm(instance=veiculo)

    return render(request, 'editar_veiculos.html', {'form': form, 'veiculo': veiculo})

@login_required
def listar_veiculos_views(request):
    form = ListarVeiculoForm(request.GET or None)
    veiculos = Veiculo.objects.all()

    if form.is_valid():
        if form.cleaned_data['grupo']:
            veiculos = veiculos.filter(grupo=form.cleaned_data['grupo'])
        if form.cleaned_data['tipo_placa']:
            veiculos = veiculos.filter(tipo_placa=form.cleaned_data['tipo_placa'])
        if form.cleaned_data['placa']:
            veiculos = veiculos.filter(placa__icontains=form.cleaned_data['placa'])

    return render(request, 'listar_veiculos.html', {'form': form, 'veiculos': veiculos})

@login_required
def excluir_veiculo_view(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)

    if request.method == 'POST':
        veiculo.delete()
        return redirect('listar_veiculos')

    return render(request, 'excluir_veiculos.html', {'veiculo': veiculo})