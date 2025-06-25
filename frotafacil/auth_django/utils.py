from .models import ConfiguracaoAutenticacao

def get_adfs_settings():
    config = ConfiguracaoAutenticacao.objects.first()
    if not config:
        return None
    return {
        "AUDIENCE": config.azure_audience,
        "CLIENT_ID": config.azure_client_id,
        "CLIENT_SECRET": config.azure_client_secret,
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