from django.db import models

# Create your models here.

class ConfiguracaoAutenticacao(models.Model):
    ad_user = models.CharField("Usuário AD", max_length=255, blank=True, null=True)
    ad_password = models.CharField("Senha AD", max_length=255, blank=True, null=True)
    azure_tenant_id = models.CharField("Azure Tenant ID", max_length=255, blank=True, null=True)
    azure_client_id = models.CharField("Azure Client ID", max_length=255, blank=True, null=True)
    azure_resource = models.CharField("Azure Resource", max_length=255, blank=True, null=True)
    azure_audience = models.CharField("Azure Audience", max_length=255, blank=True, null=True)
    azure_relying_party_id = models.CharField("Azure Relying Party ID", max_length=255, blank=True, null=True)

    def __str__(self):
        return "Configuração de Autenticação"

    class Meta:
        verbose_name = 'Configuração de Autenticação'
        verbose_name_plural = 'Configurações de Autenticação'
