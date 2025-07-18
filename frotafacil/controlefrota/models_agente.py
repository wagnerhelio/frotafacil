from django.db import models
from django.conf import settings

class Agente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    matricula = models.CharField(max_length=30, unique=True)
    ferias_inicio = models.DateField(null=True, blank=True, verbose_name='Início das Férias')
    ferias_fim = models.DateField(null=True, blank=True, verbose_name='Fim das Férias')
    data_inicio_escala = models.DateField(null=True, blank=True, verbose_name='Início da Escala')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} ({self.matricula})"

class PlantaoAgente(models.Model):
    agente = models.ForeignKey('Agente', on_delete=models.CASCADE, related_name='plantoes')
    data = models.DateField()
    horas = models.PositiveIntegerField(default=12)
    status = models.CharField(max_length=1, default='X')

    class Meta:
        unique_together = ('agente', 'data')
        verbose_name = 'Plantão do Agente'
        verbose_name_plural = 'Plantões dos Agentes'

    def __str__(self):
        return f"{self.agente.nome} - {self.data} ({self.horas}h)" 