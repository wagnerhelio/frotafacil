from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models_agente import Agente
from .forms_agente import AgenteForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from auth_django.ldap_auth import autenticar_usuario_ad
from ldap3 import Server, Connection, NTLM, ALL, ALL_ATTRIBUTES, SUBTREE
import json
import os

@login_required
def home_agente_view(request):
    total_agente = Agente.objects.count()
    # Por enquanto, todos os agentes são considerados ativos
    # Você pode adicionar um campo 'ativo' no modelo se precisar
    agente_ativo = total_agente
    agente_inativo = 0
    
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
    Busca dados do usuário no Active Directory por matrícula
    """
    servidor = Server('go.trf1.gov.br', get_info=ALL)
    base_dn = "OU=Secao Judiciaria do Estado de Goias,DC=go,DC=trf1,DC=gov,DC=br"
    
    try:
        # Usar credenciais de serviço ou anônimo para busca
        # Você pode precisar configurar credenciais específicas para busca
        with Connection(servidor, auto_bind=True) as conn:
            
            # Buscar usuário pela matrícula (sAMAccountName)
            conn.search(
                search_base=base_dn,
                search_filter=f'(sAMAccountName={matricula})',
                search_scope=SUBTREE,
                attributes=['displayName', 'mail', 'cn', 'sAMAccountName']
            )

            if conn.entries:
                entry = conn.entries[0]
                
                # Extrair nome completo
                nome_completo = entry.displayName.value if hasattr(entry, 'displayName') else entry.cn.value
                
                # Extrair email
                email = entry.mail.value if hasattr(entry, 'mail') else f'{matricula}@go.trf1.gov.br'
                
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