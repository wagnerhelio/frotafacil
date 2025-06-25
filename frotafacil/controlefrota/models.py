# Models are defined in models_veiculo.py
from .models_veiculo import Veiculo
from django.db import models

# Create your models here.

class ControleAprovacoes(models.Model):
    aprovacao_automatica = models.BooleanField('Aprovação automática de requisições', default=False)

    def __str__(self):
        return "Controle de Aprovações"

    class Meta:
        verbose_name = 'Controle de Aprovações'
        verbose_name_plural = 'Controle de Aprovações'