from django.shortcuts import render, redirect, get_object_or_404
from .models_requisicao import Requisicao
from .forms_requisicao import RequisicaoForm, FiltrarRequisicaoForm, FinalizarRequisicaoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models_veiculo import Veiculo
from django.http import JsonResponse, HttpResponse
from .models import ControleAprovacoes, Notificacao
from django.views.decorators.http import require_POST
from django.conf import settings
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models_agente import Agente
from django.core.exceptions import PermissionDenied

@login_required
def listar_requisicao(request):
    form = FiltrarRequisicaoForm(request.GET or None)
    requisicoes = Requisicao.objects.all().order_by('-id')
    if form.is_valid():
        if form.cleaned_data['veiculo']:
            requisicoes = requisicoes.filter(veiculo=form.cleaned_data['veiculo'])
        if form.cleaned_data['usuario']:
            requisicoes = requisicoes.filter(usuario=form.cleaned_data['usuario'])
        if form.cleaned_data['data_especifica']:
            requisicoes = requisicoes.filter(data_utilizacao=form.cleaned_data['data_especifica'])
        else:
            if form.cleaned_data['data_inicial']:
                requisicoes = requisicoes.filter(data_utilizacao__gte=form.cleaned_data['data_inicial'])
            if form.cleaned_data['data_final']:
                requisicoes = requisicoes.filter(data_utilizacao__lte=form.cleaned_data['data_final'])
    # Buscar status de aprovação automática
    config = ControleAprovacoes.objects.first()
    aprovacao_automatica = config.aprovacao_automatica if config else False
    pode_reivindicar = False
    if request.user.is_superuser:
        pode_reivindicar = True
    else:
        pode_reivindicar = Agente.objects.filter(email=request.user.email).exists()
    return render(request, 'listar_requisicao.html', {'requisicoes': requisicoes, 'form': form, 'aprovacao_automatica': aprovacao_automatica, 'pode_reivindicar': pode_reivindicar})

@login_required
def cadastrar_requisicao(request):
    if request.method == 'POST':
        form = RequisicaoForm(request.POST, user=request.user)
        if form.is_valid():
            requisicao = form.save(commit=False)
            requisicao.usuario = request.user
            # Aprovação automática
            try:
                config = ControleAprovacoes.objects.first()
                if config and config.aprovacao_automatica:
                    requisicao.status_aprovacao = 'aprovada'
            except Exception:
                pass
            requisicao.save()
            return redirect('listar_requisicao')
    else:
        form = RequisicaoForm(user=request.user)
    # Montar lista de veículos com informações de ocupação
    veiculos_info = []
    for v in form.fields['veiculo'].queryset:
        ocupado = v.id in getattr(form, 'veiculos_ocupados_ids', [])
        info = getattr(form, 'veiculos_ocupados_info', {}).get(v.id, {})
        veiculos_info.append({
            'id': v.id,
            'label': str(v),
            'ocupado': ocupado,
            'requisicao_id': info.get('requisicao_id'),
            'previsao_termino': info.get('previsao_termino'),
        })
    return render(request, 'cadastrar_requisicao.html', {'form': form, 'veiculos_info': veiculos_info})

@login_required
def finalizar_requisicao(request, pk):
    requisicao = get_object_or_404(Requisicao, pk=pk)
    if requisicao.status_aprovacao != 'aprovada':
        messages.error(request, 'A requisição só pode ser finalizada se estiver aprovada.')
        return redirect('listar_requisicao')
    if not requisicao.nome_motorista:
        messages.error(request, 'A requisição deve ser reivindicada por um motorista antes de ser finalizada.')
        return redirect('listar_requisicao')
    if request.method == 'POST':
        form = FinalizarRequisicaoForm(request.POST, instance=requisicao, veiculo=requisicao.veiculo)
        if form.is_valid():
            req = form.save(commit=False)
            req.status = 'finalizada'
            req.save()
            return redirect('listar_requisicao')
    else:
        form = FinalizarRequisicaoForm(instance=requisicao, veiculo=requisicao.veiculo)
    km_saida_sugerido = getattr(form, 'km_saida_sugerido', '')
    return render(request, 'finalizar_requisicao.html', {'form': form, 'requisicao': requisicao, 'km_saida_sugerido': km_saida_sugerido})

@login_required
def home_requisicao(request):
    total = Requisicao.objects.count()
    ativas = Requisicao.objects.filter(status='ativa').count()
    finalizadas = Requisicao.objects.filter(status='finalizada').count()
    aprovadas = Requisicao.objects.filter(status_aprovacao='aprovada').count()
    requisicoes_pendentes = Requisicao.objects.filter(status_aprovacao='pendente')
    # Buscar status de aprovação automática
    config = ControleAprovacoes.objects.first()
    aprovacao_automatica = config.aprovacao_automatica if config else False
    return render(request, 'home_requisicao.html', {
        'total': total,
        'ativas': ativas,
        'finalizadas': finalizadas,
        'aprovadas': aprovadas,
        'requisicoes_pendentes': requisicoes_pendentes,
        'aprovacao_automatica': aprovacao_automatica,
    })

@staff_member_required
def aprovar_requisicao(request, pk):
    requisicao = get_object_or_404(Requisicao, pk=pk)
    if request.method == 'POST':
        requisicao.status_aprovacao = 'aprovada'
        requisicao.save()
        messages.success(request, 'Requisição aprovada com sucesso!')
        return redirect('listar_requisicao')
    return render(request, 'aprovar_requisicao.html', {'requisicao': requisicao})

@staff_member_required
def recusar_requisicao(request, pk):
    requisicao = get_object_or_404(Requisicao, pk=pk)
    if request.method == 'POST':
        requisicao.status_aprovacao = 'recusada'
        requisicao.save()
        messages.success(request, 'Requisição recusada com sucesso!')
        return redirect('listar_requisicao')
    return render(request, 'recusar_requisicao.html', {'requisicao': requisicao})

@login_required
def editar_requisicao(request, pk):
    requisicao = get_object_or_404(Requisicao, pk=pk)
    if requisicao.status_aprovacao == 'aprovada' and not request.user.is_staff:
        messages.error(request, 'Apenas administradores podem editar requisições aprovadas.')
        return redirect('listar_requisicao')
    if request.method == 'POST':
        form = RequisicaoForm(request.POST, instance=requisicao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Requisição editada com sucesso!')
            return redirect('listar_requisicao')
    else:
        form = RequisicaoForm(instance=requisicao)
    return render(request, 'editar_requisicao.html', {'form': form, 'requisicao': requisicao})

@login_required
def excluir_requisicao(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied
    requisicao = get_object_or_404(Requisicao, pk=pk)
    if request.method == 'POST':
        requisicao.delete()
        messages.success(request, 'Requisição excluída com sucesso!')
        return redirect('listar_requisicao')
    return render(request, 'excluir_requisicao.html', {'requisicao': requisicao})

@login_required
def visualizar_requisicao(request, pk):
    requisicao = get_object_or_404(Requisicao, pk=pk)
    km_saida_sugerido = None
    if requisicao.veiculo:
        req_anterior = requisicao.veiculo.requisicoes.filter(status='finalizada').exclude(id=requisicao.id).order_by('-data_chegada').first()
        if req_anterior:
            km_saida_sugerido = req_anterior.km_chegada
    return render(request, 'visualizar_requisicao.html', {'requisicao': requisicao, 'km_saida_sugerido': km_saida_sugerido})

@login_required
def api_ultimo_km_chegada(request, veiculo_id):
    req = Requisicao.objects.filter(veiculo_id=veiculo_id, status='finalizada').order_by('-data_chegada').first()
    return JsonResponse({'km_chegada': req.km_chegada if req else ''})

@staff_member_required
@require_POST
def toggle_aprovacao_automatica(request):
    config, _ = ControleAprovacoes.objects.get_or_create(id=1)
    config.aprovacao_automatica = not config.aprovacao_automatica
    config.save()
    messages.success(request, f"Aprovação automática {'ativada' if config.aprovacao_automatica else 'desativada'} com sucesso!")
    return redirect('home_requisicao')

@login_required
def exportar_requisicoes_pdf(request):
    requisicoes = Requisicao.objects.all()
    html_string = render_to_string('requisicoes_pdf.html', {'requisicoes': requisicoes})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="requisicoes.pdf"'
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    return response 

@login_required
def reivindicar_requisicao(request, pk):
    requisicao = get_object_or_404(Requisicao, pk=pk)
    pode_reivindicar = request.user.is_superuser or Agente.objects.filter(email=request.user.email).exists()
    if not pode_reivindicar:
        messages.error(request, 'Você não tem permissão para reivindicar esta requisição.')
        return redirect('listar_requisicao')
    if requisicao.nome_motorista:
        messages.warning(request, 'Esta requisição já possui motorista vinculado.')
        return redirect('listar_requisicao')
    if request.user.is_superuser:
        nome_motorista = request.user.get_full_name() or request.user.username
    else:
        agente = Agente.objects.get(email=request.user.email)
        nome_motorista = agente.nome
    requisicao.nome_motorista = nome_motorista
    requisicao.save()
    # Notificação persistente
    Notificacao.objects.create(
        usuario=request.user,
        mensagem=f'Você foi vinculado como motorista da requisição #{requisicao.id} do veículo {requisicao.veiculo}.'
    )
    messages.success(request, 'Você foi vinculado como motorista desta requisição!')
    return redirect('listar_requisicao') 

@login_required
def notificacoes_usuario(request):
    notificacoes = Notificacao.objects.filter(usuario=request.user, lida=False).order_by('-criada_em')
    data = [
        {
            'id': n.id,
            'mensagem': n.mensagem,
            'criada_em': n.criada_em.strftime('%d/%m/%Y %H:%M')
        } for n in notificacoes
    ]
    return JsonResponse({'notificacoes': data})

@login_required
@require_POST
def marcar_notificacoes_lidas(request):
    Notificacao.objects.filter(usuario=request.user, lida=False).update(lida=True)
    return JsonResponse({'ok': True}) 
