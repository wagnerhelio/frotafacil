from django.contrib import admin
from .models import ConfiguracaoAutenticacao

@admin.register(ConfiguracaoAutenticacao)
class ConfiguracaoAutenticacaoAdmin(admin.ModelAdmin):
    list_display = (
        'ad_user', 'azure_tenant_id'
    )
    fieldsets = (
        ('Autenticação AD', {
            'fields': ('ad_user', 'ad_password')
        }),
        ('Autenticação Azure', {
            'fields': (
                'azure_tenant_id', 'azure_client_id', 'azure_resource',
                'azure_audience', 'azure_relying_party_id', 'azure_client_secret'
            )
        }),
    )
