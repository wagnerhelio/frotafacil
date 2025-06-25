from ldap3 import Server, Connection, NTLM, ALL, ALL_ATTRIBUTES, SUBTREE
import os
import re

def autenticar_usuario_ad(username, password):
    servidor = Server('go.trf1.gov.br', get_info=ALL)

    # TODO: Buscar usuário e senha do AD a partir do modelo ConfiguracaoAutenticacao.
    base_dn = "OU=Secao Judiciaria do Estado de Goias,DC=go,DC=trf1,DC=gov,DC=br"
    
    print("[DEBUG] usuário serviço bruto:", username)
    print("[DEBUG] usuário serviço repr:", repr(username))
    print("[DEBUG] usuário digitado bruto:", username)
    print("[DEBUG] usuário digitado repr:", repr(username))

    if '\\' not in username:
        dominio = os.getenv("USERDOMAIN", "jfgo")
        username = f"{dominio}\\{username}"

    try:
        print(f"[DEBUG] Login recebido: {username}")

        with Connection(servidor, user=username, password=password,
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
            
        return {
            'username': username,
            'nome_completo': nome_completo
        }

    except Exception as e:
        print(f"[ERRO] Erro ao autenticar no AD: {e}")
        return False 