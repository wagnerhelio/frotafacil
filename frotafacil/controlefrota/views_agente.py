from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models_agente import Agente
from .forms_agente import AgenteForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ldap3 import Server, Connection, NTLM, ALL, ALL_ATTRIBUTES, SUBTREE
import json
import os
from auth_django.models import ConfiguracaoAutenticacao
from django.urls import reverse
from django.contrib import messages
from .models_ferias import FeriasAgente
from calendar import monthrange, monthcalendar
from datetime import date, timedelta
from django.utils import timezone
from .models_agente import PlantaoAgente
import calendar

@login_required
def home_agente_view(request):
    total_agente = Agente.objects.filter(ativo=True).count()
    agente_ativo = total_agente
    agente_inativo = Agente.objects.filter(ativo=False).count()
    context = {
        'total_agente': total_agente,
        'agente_ativo': agente_ativo,
        'agente_inativo': agente_inativo,
    }
    return render(request, 'home_agente.html', context)

@login_required
def listar_agente_view(request):
    agentes = Agente.objects.all()
    return render(request, 'listar_agente.html', {'agentes': agentes})

@login_required
def cadastrar_agente_view(request):
    if request.method == 'POST':
        form = AgenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_agente')
    else:
        form = AgenteForm()
    return render(request, 'cadastrar_agente.html', {'form': form})

@csrf_exempt
@login_required
def buscar_ldap_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            matricula = data.get('matricula')
            
            if matricula:
                # Buscar dados do usuário no LDAP usando a função existente
                resultado = buscar_usuario_por_matricula(matricula)
                
                if resultado:
                    return JsonResponse({
                        'success': True,
                        'nome': resultado['nome_completo'],
                        'email': resultado['email']
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'Usuário não encontrado no AD'
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Matrícula não fornecida'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Dados inválidos'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Método não permitido'
    })

def buscar_usuario_por_matricula(matricula):
    """
    Busca dados do usuário no Active Directory por matrícula usando usuário de serviço
    """
    servidor = Server('go.trf1.gov.br', get_info=ALL)
    base_dn = "DC=go,DC=trf1,DC=gov,DC=br"
    config = ConfiguracaoAutenticacao.objects.first()
    if not config:
        print("[ERRO] Configuração de autenticação de serviço não encontrada no banco de dados.")
        return None
    usuario_servico = config.ad_user
    senha_servico = config.ad_password
    print(f"[DEBUG] Usuário de serviço para busca LDAP: {usuario_servico}")
    print(f"[DEBUG] Usuário de serviço para busca LDAP (repr): {repr(usuario_servico)}")
    try:
        with Connection(servidor, user=usuario_servico, password=senha_servico,
                        authentication=NTLM, auto_bind=True) as conn:
            print(f"[DEBUG] Buscando sAMAccountName no AD: {matricula}")
            conn.search(
                search_base=base_dn,
                search_filter=f'(sAMAccountName={matricula})',
                search_scope=SUBTREE,
                attributes=['displayName', 'mail', 'cn', 'sAMAccountName']
            )
            if conn.entries:
                entry = conn.entries[0]
                nome_completo = entry.displayName.value if hasattr(entry, 'displayName') else entry.cn.value
                email = entry.mail.value if hasattr(entry, 'mail') else f'{matricula}@go.trf1.gov.br'
                print(f"[DEBUG] Usuário encontrado: {nome_completo}, email: {email}")
                return {
                    'nome_completo': nome_completo,
                    'email': email,
                    'matricula': matricula
                }
            else:
                print(f"[DEBUG] Usuário {matricula} não encontrado no AD")
                return None
    except Exception as e:
        print(f"[ERRO] Erro ao buscar usuário no AD: {e}")
        return None 

@login_required
def editar_agente_view(request, pk):
    agente = get_object_or_404(Agente, pk=pk)
    if request.method == 'POST':
        form = AgenteForm(request.POST, instance=agente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agente atualizado com sucesso!')
            return redirect('listar_agente')
    else:
        form = AgenteForm(instance=agente)
    return render(request, 'editar_agente.html', {'form': form, 'agente': agente})

@login_required
def excluir_agente_view(request, pk):
    agente = get_object_or_404(Agente, pk=pk)
    if request.method == 'POST':
        agente.delete()
        messages.success(request, 'Agente excluído com sucesso!')
        return redirect('listar_agente')
    return render(request, 'excluir_agente.html', {'form': None, 'agente': agente})

@login_required
def controle_ferias_view(request):
    # import locale
    # locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')  # Linha removida, não é mais necessária
    today = timezone.now().date()
    mes = int(request.GET.get('mes', today.month))
    ano = int(request.GET.get('ano', today.year))
    dias_no_mes = monthrange(ano, mes)[1]
    dias = [date(ano, mes, d) for d in range(1, dias_no_mes+1)]

    # Busca agentes com férias que intersectam o mês
    agentes = Agente.objects.exclude(ferias_inicio__isnull=True).exclude(ferias_fim__isnull=True)
    agentes_ferias = []
    for agente in agentes:
        if agente.ferias_fim >= date(ano, mes, 1) and agente.ferias_inicio <= date(ano, mes, dias_no_mes):
            agentes_ferias.append(agente)

    # Mapeia cada dia para lista de agentes de férias
    agentes_por_dia = {d: [] for d in dias}
    for agente in agentes_ferias:
        for d in dias:
            if agente.ferias_inicio <= d <= agente.ferias_fim:
                agentes_por_dia[d].append({'nome': agente.nome})

    # Monta estrutura de calendário (lista de semanas)
    calendar.setfirstweekday(calendar.MONDAY)
    cal = monthcalendar(ano, mes)  # cada semana é uma lista de 7 ints (0 = vazio)
    calendario = []
    for semana in cal:
        semana_dias = []
        for i, dia_num in enumerate(semana):
            if dia_num == 0:
                semana_dias.append(None)
            else:
                d = date(ano, mes, dia_num)
                semana_dias.append({'day': dia_num, 'agentes': agentes_por_dia.get(d, [])})
        calendario.append(semana_dias)

    # Lista de meses para o filtro em português
    meses_pt = [
        {'value': 1, 'nome': 'Janeiro'},
        {'value': 2, 'nome': 'Fevereiro'},
        {'value': 3, 'nome': 'Março'},
        {'value': 4, 'nome': 'Abril'},
        {'value': 5, 'nome': 'Maio'},
        {'value': 6, 'nome': 'Junho'},
        {'value': 7, 'nome': 'Julho'},
        {'value': 8, 'nome': 'Agosto'},
        {'value': 9, 'nome': 'Setembro'},
        {'value': 10, 'nome': 'Outubro'},
        {'value': 11, 'nome': 'Novembro'},
        {'value': 12, 'nome': 'Dezembro'},
    ]

    return render(request, 'controle_ferias.html', {
        'calendario': calendario,
        'mes': mes,
        'ano': ano,
        'meses': meses_pt,
    }) 

@login_required
def controle_escala_view(request):
    today = timezone.now().date()
    mes = int(request.GET.get('mes', today.month))
    ano = int(request.GET.get('ano', today.year))
    dias_no_mes = monthrange(ano, mes)[1]
    dias = [date(ano, mes, d) for d in range(1, dias_no_mes+1)]
    agentes = Agente.objects.exclude(data_inicio_escala__isnull=True)
    # Remover filtro de agentes de férias para exibir todos na escala
    # agentes_nao_ferias = []
    # for agente in agentes:
    #     if agente.ferias_inicio and agente.ferias_fim:
    #         if not (agente.ferias_fim < dias[0] or agente.ferias_inicio > dias[-1]):
    #             continue
    #     agentes_nao_ferias.append(agente)
    # agentes = agentes_nao_ferias

    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('recalcular'):
            # Apagar plantões do mês
            PlantaoAgente.objects.filter(data__month=mes, data__year=ano).delete()
            # Gerar escala automática 12x36 + rodízio de finais de semana
            horas_por_agente = {agente.id: 0 for agente in agentes}
            # Dias do mês
            sabados = []
            domingos = []
            for d in dias:
                if d.weekday() == 5:
                    sabados.append(d)
                elif d.weekday() == 6:
                    domingos.append(d)
            # Rodízio de finais de semana
            agentes_list = list(agentes)
            num_pares = len(agentes_list) // 2
            resto = len(agentes_list) % 2
            rodizio = []
            for i in range(num_pares):
                rodizio.append([agentes_list[2*i], agentes_list[2*i+1]])
            if resto:
                rodizio.append([agentes_list[-1], None])
            # Alternância sábado/domingo
            if len(rodizio) > 0:
                for idx, (sab, dom) in enumerate(zip(sabados, domingos)):
                    par = rodizio[idx % len(rodizio)]
                    if idx % 2 == 0:
                        ag_sab, ag_dom = par[0], par[1]
                    else:
                        ag_sab, ag_dom = par[1], par[0]
                    # Sábado
                    if ag_sab and horas_por_agente[ag_sab.id] < 120:
                        if ag_sab.data_inicio_escala and sab < ag_sab.data_inicio_escala:
                            continue  # Não escala antes do início
                        if ag_sab.ferias_inicio and ag_sab.ferias_fim and ag_sab.ferias_inicio <= sab <= ag_sab.ferias_fim:
                            PlantaoAgente.objects.create(agente=ag_sab, data=sab, horas=0, status='F')
                        else:
                            PlantaoAgente.objects.create(agente=ag_sab, data=sab, horas=12, status='X')
                            horas_por_agente[ag_sab.id] += 12
                    # Domingo
                    if ag_dom and horas_por_agente[ag_dom.id] < 120:
                        if ag_dom.data_inicio_escala and dom < ag_dom.data_inicio_escala:
                            continue  # Não escala antes do início
                        if ag_dom.ferias_inicio and ag_dom.ferias_fim and ag_dom.ferias_inicio <= dom <= ag_dom.ferias_fim:
                            PlantaoAgente.objects.create(agente=ag_dom, data=dom, horas=0, status='F')
                        else:
                            PlantaoAgente.objects.create(agente=ag_dom, data=dom, horas=12, status='X')
                            horas_por_agente[ag_dom.id] += 12
            # Dias de semana (12x36 normal)
            for agente in agentes:
                inicio = agente.data_inicio_escala
                ciclo = 2
                for d in dias:
                    if d.weekday() in [5,6]:
                        continue  # já tratado no rodízio
                    if inicio and (d - inicio).days >= 0 and ((d - inicio).days % ciclo) == 0:
                        if horas_por_agente[agente.id] < 120:
                            if agente.ferias_inicio and agente.ferias_fim and agente.ferias_inicio <= d <= agente.ferias_fim:
                                PlantaoAgente.objects.create(
                                    agente=agente,
                                    data=d,
                                    horas=0,
                                    status='F'
                                )
                            else:
                                PlantaoAgente.objects.create(
                                    agente=agente,
                                    data=d,
                                    horas=12,
                                    status='X'
                                )
                                horas_por_agente[agente.id] += 12
            return JsonResponse({'success': True})
        escala = data.get('escala', {})  # { 'YYYY-MM-DD': { 'agente_id': 'status', ... } }
        # Apagar plantões do mês
        PlantaoAgente.objects.filter(data__month=mes, data__year=ano).delete()
        # Criar novos plantões
        for dia_str, agentes_status in escala.items():
            for agente_id, status in agentes_status.items():
                if not status:
                    continue  # Não cria plantão para status vazio
                horas = 12 if status == 'X' else 0
                PlantaoAgente.objects.create(
                    agente_id=agente_id,
                    data=dia_str,
                    horas=horas,
                    status=status
                )
        return JsonResponse({'success': True})

    # GET: buscar plantões salvos
    plantoes = PlantaoAgente.objects.filter(data__month=mes, data__year=ano)
    escala_dias = {}
    horas_por_agente = {agente.id: 0 for agente in agentes}
    status_por_agente_dia = {}
    if plantoes.exists():
        for plantao in plantoes:
            if plantao.data not in escala_dias:
                escala_dias[plantao.data] = []
            escala_dias[plantao.data].append(plantao.agente)
            if plantao.status:
                status_por_agente_dia[(plantao.agente.id, plantao.data)] = plantao.status
            if plantao.status == 'X':
                if plantao.agente.id in horas_por_agente:
                    horas_por_agente[plantao.agente.id] += plantao.horas
    else:
        # Gera escala automática 12x36 + rodízio de finais de semana
        sabados = []
        domingos = []
        for d in dias:
            if d.weekday() == 5:
                sabados.append(d)
            elif d.weekday() == 6:
                domingos.append(d)
        agentes_list = list(agentes)
        num_pares = len(agentes_list) // 2
        resto = len(agentes_list) % 2
        rodizio = []
        for i in range(num_pares):
            rodizio.append([agentes_list[2*i], agentes_list[2*i+1]])
        if resto:
            rodizio.append([agentes_list[-1], None])
        if len(rodizio) > 0:
            for idx, (sab, dom) in enumerate(zip(sabados, domingos)):
                par = rodizio[idx % len(rodizio)]
                if idx % 2 == 0:
                    ag_sab, ag_dom = par[0], par[1]
                else:
                    ag_sab, ag_dom = par[1], par[0]
                if ag_sab and horas_por_agente[ag_sab.id] < 120:
                    if sab not in escala_dias:
                        escala_dias[sab] = []
                    escala_dias[sab].append(ag_sab)
                    horas_por_agente[ag_sab.id] += 12
                if ag_dom and horas_por_agente[ag_dom.id] < 120:
                    if dom not in escala_dias:
                        escala_dias[dom] = []
                    escala_dias[dom].append(ag_dom)
                    horas_por_agente[ag_dom.id] += 12
        for agente in agentes:
            inicio = agente.data_inicio_escala
            ciclo = 2
            for d in dias:
                if d.weekday() in [5,6]:
                    continue
                if inicio and (d - inicio).days >= 0 and ((d - inicio).days % ciclo) == 0:
                    if horas_por_agente[agente.id] < 120:
                        if d not in escala_dias:
                            escala_dias[d] = []
                        escala_dias[d].append(agente)
                        horas_por_agente[agente.id] += 12

    # Lista de agentes de férias no mês
    agentes_ferias = []
    for agente in Agente.objects.exclude(data_inicio_escala__isnull=True):
        if agente.ferias_inicio and agente.ferias_fim:
            if not (agente.ferias_fim < dias[0] or agente.ferias_inicio > dias[-1]):
                agentes_ferias.append(agente)

    # Monta estrutura de calendário (lista de semanas)
    calendar.setfirstweekday(calendar.MONDAY)
    cal = monthcalendar(ano, mes)
    calendario = []
    for semana in cal:
        semana_dias = []
        for dia_num in semana:
            if dia_num == 0:
                semana_dias.append(None)
            else:
                d = date(ano, mes, dia_num)
                # Contingente: apenas quem está com status 'X', 'P' ou 'R'
                agentes_dia = []
                for agente in agentes:
                    key = (agente.id, d)
                    status = status_por_agente_dia.get(key)
                    if status in ['X', 'P', 'R']:
                        agentes_dia.append(agente)
                semana_dias.append({'day': dia_num, 'agentes': agentes_dia})
        calendario.append(semana_dias)

    meses_pt = [
        {'value': 1, 'nome': 'Janeiro'},
        {'value': 2, 'nome': 'Fevereiro'},
        {'value': 3, 'nome': 'Março'},
        {'value': 4, 'nome': 'Abril'},
        {'value': 5, 'nome': 'Maio'},
        {'value': 6, 'nome': 'Junho'},
        {'value': 7, 'nome': 'Julho'},
        {'value': 8, 'nome': 'Agosto'},
        {'value': 9, 'nome': 'Setembro'},
        {'value': 10, 'nome': 'Outubro'},
        {'value': 11, 'nome': 'Novembro'},
        {'value': 12, 'nome': 'Dezembro'},
    ]
    horas_agentes = [(agente, horas_por_agente[agente.id]) for agente in agentes]
    dias_semana_letras = ['S', 'T', 'Q', 'Q', 'S', 'S', 'D']  # Segunda a Domingo
    # Montar matriz de status: status_matrix[agente_idx][dia_idx] = status
    status_matrix = []
    total_dias_agentes = []
    flat_dias = [d for semana in calendario for d in semana if d]
    for agente in agentes:
        linha = []
        total_dias = 0
        for dia in flat_dias:
            d_obj = date(ano, mes, dia['day'])
            key = (agente.id, d_obj)
            status = status_por_agente_dia.get(key)
            if status is not None:
                linha.append(status)
            else:
                f_inicio = agente.ferias_inicio
                f_fim = agente.ferias_fim
                if f_inicio and f_fim and f_inicio <= d_obj <= f_fim:
                    linha.append('F')
                elif (
                    d_obj in escala_dias and agente in escala_dias[d_obj]
                    and agente.data_inicio_escala and d_obj >= agente.data_inicio_escala
                ):
                    linha.append('X')
                else:
                    linha.append('')
            # Contar dias escalados
            if status in ['X', 'P', 'R']:
                total_dias += 1
        status_matrix.append(linha)
        total_dias_agentes.append(total_dias)
    agentes_status = list(zip(agentes, status_matrix, total_dias_agentes))

    # Lista das letras dos dias da semana para cada dia do mês (na ordem dos dias exibidos)
    dias_semana_letras_mes = []
    dias_fim_de_semana = []
    for semana in calendario:
        for dia in semana:
            if dia:
                d = date(ano, mes, dia['day'])
                dias_semana_letras_mes.append(dias_semana_letras[d.weekday()])
                dias_fim_de_semana.append(d.weekday() in [5, 6])  # 5=sábado, 6=domingo

    # Lista de tuplas (letra, is_fds) para o cabeçalho dos dias da semana
    dias_semana_header = list(zip(dias_semana_letras_mes, dias_fim_de_semana))

    return render(request, 'controle_escala.html', {
        'calendario': calendario,
        'mes': mes,
        'ano': ano,
        'meses': meses_pt,
        'agentes_status': agentes_status,
        'horas_por_agente': horas_por_agente,
        'horas_agentes': horas_agentes,
        'agentes_ferias': agentes_ferias,
        'dias_semana_letras': dias_semana_letras,
        'dias_semana_letras_mes': dias_semana_letras_mes,
        'dias_fim_de_semana': dias_fim_de_semana,
        'dias_semana_header': dias_semana_header,
    }) 