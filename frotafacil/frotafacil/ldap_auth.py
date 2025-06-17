from ldap3 import Server, Connection, NTLM, ALL, ALL_ATTRIBUTES, SUBTREE
import os
import re
from dotenv import load_dotenv
load_dotenv()

def autenticar_usuario_ad(username, password):
    servidor = Server('go.trf1.gov.br', get_info=ALL)

    usuario_servico = os.getenv('AD_USER')
    senha_servico = os.getenv('AD_PASSWORD')
    base_dn = "OU=Secao Judiciaria do Estado de Goias,DC=go,DC=trf1,DC=gov,DC=br"
    
    print("[DEBUG] usuário serviço bruto:", usuario_servico)
    print("[DEBUG] usuário serviço repr:", repr(usuario_servico))
    print("[DEBUG] usuário digitado bruto:", username)
    print("[DEBUG] usuário digitado repr:", repr(username))

    if '\\' not in username:
        dominio = os.getenv("USERDOMAIN", "jfgo")
        username = f"{dominio}\\{username}"

    try:
        print(f"[DEBUG] Login recebido: {username}")
        print(f"[DEBUG] Conectando com conta de serviço: {usuario_servico}")

        with Connection(servidor, user=usuario_servico, password=senha_servico,
                        authentication=NTLM, auto_bind=True) as conn:

            usuario_busca = username.split("\\")[1]
            print(f"[DEBUG] Buscando sAMAccountName: {usuario_busca}")

            conn.search(
                search_base=base_dn,
                search_filter=f'(sAMAccountName={usuario_busca})',
                search_scope=SUBTREE,
                attributes=ALL_ATTRIBUTES
            )

            if not conn.entries:
                print("[ERRO] Usuário não encontrado no AD.")
                return False

            usuario_dn = conn.entries[0].entry_dn
            print(f"[DEBUG] DN encontrado: {usuario_dn}")
            
            match = re.search(r'CN=([^,]+)', usuario_dn)
            nome_completo = match.group(1) if match else usuario_busca
            
        # Segunda conexão com login NTLM (domínio\usuário)
        usuario_login_ntlm = f"jfgo\\{usuario_busca}"
        print(f"[DEBUG] Tentando autenticar com: {usuario_login_ntlm}")

        with Connection(servidor, user=usuario_login_ntlm, password=password,
                        authentication=NTLM, auto_bind=True) as conn_user:
            if conn_user.bound:
                print("[DEBUG] Autenticado com sucesso.")
                return {
                    'username': usuario_login_ntlm,
                    'nome_completo': nome_completo
                }
            else:
                return False

    except Exception as e:
        print(f"[ERRO] Erro ao autenticar no AD: {e}")
        return False