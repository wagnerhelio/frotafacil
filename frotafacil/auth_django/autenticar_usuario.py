from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django_auth_adfs.backend import AdfsAuthCodeBackend
from django_auth_adfs.config import settings as adfs_settings
from auth_django.models import ConfiguracaoAutenticacao
from ldap3 import Server, Connection, NTLM, ALL, ALL_ATTRIBUTES, SUBTREE
import os
import re

class DjangoAndLdapBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        print(f"[DEBUG] Iniciando autenticação para usuário: {username}")
        User = get_user_model()
        # 1. Autenticação local
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                print(f"[DEBUG] Usuário autenticado localmente: {user.username}")
                return user
            else:
                print(f"[DEBUG] Senha incorreta para usuário local: {username}")
        except User.DoesNotExist:
            print(f"[DEBUG] Usuário {username} não encontrado localmente. Tentando LDAP...")

        # 2. Autenticação LDAP
        config = ConfiguracaoAutenticacao.objects.first()
        if not config:
            print("[ERRO] Configuração de autenticação de serviço não encontrada no banco de dados.")
            return None

        usuario_servico = config.ad_user
        senha_servico = config.ad_password
        print(f"[DEBUG] Usuário de serviço para LDAP: {usuario_servico}")
        servidor = Server('go.trf1.gov.br', get_info=ALL)
        base_dn = "DC=go,DC=trf1,DC=gov,DC=br"
        dominio = os.getenv("USERDOMAIN", "jfgo")
        username_ad = username if '\\' in username else f"{dominio}\\{username}"
        print(f"[DEBUG] Username para autenticação no AD: {username_ad}")

        try:
            print("[DEBUG] Conectando no AD com usuário de serviço...")
            with Connection(servidor, user=usuario_servico, password=senha_servico,
                            authentication=NTLM, auto_bind=True) as conn:
                usuario_busca = username_ad.split("\\")[1]
                print(f"[DEBUG] Buscando sAMAccountName no AD: {usuario_busca}")
                conn.search(
                    search_base=base_dn,
                    search_filter=f'(sAMAccountName={usuario_busca})',
                    search_scope=SUBTREE,
                    attributes=ALL_ATTRIBUTES
                )
                if not conn.entries:
                    print(f"[ERRO] Usuário {usuario_busca} não encontrado no AD.")
                    return None
                usuario_dn = conn.entries[0].entry_dn
                print(f"[DEBUG] DN encontrado para usuário: {usuario_dn}")
                print(f"[DEBUG] Tentando autenticar {username_ad} com senha informada...")
                with Connection(servidor, user=username_ad, password=password,
                                authentication=NTLM, auto_bind=True) as conn_user:
                    print(f"[DEBUG] Autenticação LDAP bem-sucedida para {username_ad}")
                    match = re.search(r'CN=([^,]+)', usuario_dn)
                    nome_completo = match.group(1) if match else usuario_busca
                    user, created = User.objects.get_or_create(username=username_ad)
                    print(f"[DEBUG] Usuário {'criado' if created else 'recuperado'} no Django: {user.username}")
                    if hasattr(user, 'first_name'):
                        print(f"[DEBUG] Atualizando nome completo do usuário para: {nome_completo}")
                        user.first_name = nome_completo
                        user.save()
                    if request is not None:
                        print(f"[DEBUG] Salvando nome completo na sessão: {nome_completo}")
                        request.session['nome_completo_ad'] = nome_completo
                    return user
        except Exception as e:
            print(f"[ERRO] Erro ao autenticar no AD: {e}")
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None 

class DynamicAdfsAuthCodeBackend(AdfsAuthCodeBackend):
    def authenticate(self, request, **kwargs):
        print("[DEBUG] Iniciando autenticação Azure AD/EntraID...")
        adfs_config = get_adfs_settings()
        if adfs_config:
            print("[DEBUG] Configurações ADFS carregadas do banco de dados.")
            for key, value in adfs_config.items():
                setattr(adfs_settings, key, value)
        else:
            print("[ERRO] Não foi possível carregar configurações ADFS do banco de dados.")
        return super().authenticate(request, **kwargs) 

def get_adfs_settings():
    config = ConfiguracaoAutenticacao.objects.first()
    if not config:
        print("[ERRO] Configuração de autenticação Azure não encontrada no banco de dados.")
        return None
    print("[DEBUG] get_adfs_settings retornando configurações do Azure AD.")
    return {
        "AUDIENCE": config.azure_audience,
        "CLIENT_ID": config.azure_client_id,
        "TENANT_ID": config.azure_tenant_id,
        "RELYING_PARTY_ID": config.azure_relying_party_id,
        "AUTHORITY": f"https://login.microsoftonline.com/{config.azure_tenant_id}",
        "CLAIM_MAPPING": {
            "first_name": "given_name",
            "last_name": "family_name",
            "email": "upn",
        },
        "USERNAME_CLAIM": "upn",
        "GROUP_CLAIM": "roles",
    } 