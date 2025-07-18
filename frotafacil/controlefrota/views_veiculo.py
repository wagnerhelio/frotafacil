from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms_veiculo import CadastrarVeiculoForm, EditarVeiculoForm, ListarVeiculoForm, ExcluirVeiculoForm
from .models_veiculo import Veiculo 
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

@login_required
def home_veiculo_view(request):
    from .models_veiculo import Veiculo
    total_veiculo = Veiculo.objects.filter(ativo=True).count()
    veiculo_ativo = total_veiculo
    veiculo_inativo = Veiculo.objects.filter(ativo=False).count()
    context = {
        'total_veiculo': total_veiculo,
        'veiculo_ativo': veiculo_ativo,
        'veiculo_inativo': veiculo_inativo,
    }
    return render(request, 'home_veiculo.html', context)

@login_required
def cadastrar_veiculo_views(request):
    if request.method == 'POST':
        form = CadastrarVeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_veiculo')
    else:
        form = CadastrarVeiculoForm()
    return render(request, 'cadastrar_veiculo.html', {'form': form})

@login_required
def editar_veiculo_view(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)

    if request.method == 'POST':
        form = EditarVeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            return redirect('listar_veiculo')
    else:
        form = EditarVeiculoForm(instance=veiculo)

    return render(request, 'editar_veiculo.html', {'form': form, 'veiculo': veiculo})

@login_required
def listar_veiculo_views(request):
    form = ListarVeiculoForm(request.GET or None)
    veiculo_list = Veiculo.objects.all()

    if form.is_valid():
        if form.cleaned_data['placa']:
            veiculo_list = veiculo_list.filter(placa__icontains=form.cleaned_data['placa'])
        if form.cleaned_data['marca']:
            veiculo_list = veiculo_list.filter(marca__icontains=form.cleaned_data['marca'])
        if form.cleaned_data['modelo']:
            veiculo_list = veiculo_list.filter(modelo__icontains=form.cleaned_data['modelo'])
        if form.cleaned_data['ano_fabricacao']:
            veiculo_list = veiculo_list.filter(ano_fabricacao=form.cleaned_data['ano_fabricacao'])

    veiculo_ativo = veiculo_list.filter(ativo=True).count()
    veiculo_inativo = veiculo_list.filter(ativo=False).count()
    context = {
        'form': form,
        'veiculo_list': veiculo_list,
        'total_veiculo': veiculo_list.count(),
        'veiculo_ativo': veiculo_ativo,
        'veiculo_inativo': veiculo_inativo,
     }
    return render(request, 'listar_veiculo.html', context)

@login_required
def excluir_veiculo_view(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)

    if request.method == 'POST':
        form = ExcluirVeiculoForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirmar']:
            veiculo.delete()
            return redirect('listar_veiculo')
    else:
        form = ExcluirVeiculoForm()

    return render(request, 'excluir_veiculo.html', {'form': form, 'veiculo': veiculo})

@login_required
def exportar_veiculos_pdf(request):
    veiculos = Veiculo.objects.all()
    html_string = render_to_string('controlefrota/veiculos_pdf.html', {'veiculo_list': veiculos})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="veiculos.pdf"'
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    return response
