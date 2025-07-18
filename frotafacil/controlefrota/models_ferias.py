from django.db import models
from .models_agente import Agente

class FeriasAgente(models.Model):
    agente = models.ForeignKey(Agente, on_delete=models.CASCADE, related_name='ferias_periodos')
    data_inicio = models.DateField()
    data_fim = models.DateField()
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.agente.nome} ({self.data_inicio} a {self.data_fim})" 