# Models are defined in models_veiculo.py
from .models_veiculo import Veiculo
from django.db import models

# Create your models here.

class ConfiguracaoSistema(models.Model):
    aprovacao_automatica = models.BooleanField('Aprovação automática de requisições', default=False)

    def __str__(self):
        return f"Aprovação automática: {'ON' if self.aprovacao_automatica else 'OFF'}"

    class Meta:
        verbose_name = 'Configuração do Sistema'
        verbose_name_plural = 'Configurações do Sistema'
