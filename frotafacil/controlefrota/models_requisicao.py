from django.db import models
from .models_veiculo import Veiculo
from django.contrib.auth.models import User
from django.utils import timezone

class Requisicao(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('finalizada', 'Finalizada'),
    ]
    unidade = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    data_utilizacao = models.DateTimeField()
    itinerario = models.CharField(max_length=200)
    natureza_servico = models.CharField(max_length=200)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, related_name='requisicoes')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativa')
    STATUS_APROVACAO_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('recusada', 'Recusada'),
    ]
    status_aprovacao = models.CharField(max_length=10, choices=STATUS_APROVACAO_CHOICES, default='pendente')
    data_saida = models.DateTimeField(null=True, blank=True)
    data_chegada = models.DateTimeField(null=True, blank=True)
    km_saida = models.CharField(max_length=20)
    km_chegada = models.CharField(max_length=20, null=True, blank=True)
    ocorrencias = models.TextField(blank=True)
    assinatura_motorista = models.CharField(max_length=100, blank=True)
    assinatura_usuario = models.CharField(max_length=100, blank=True)
    motivo_km_saida_divergente = models.TextField(blank=True)
    nome_motorista = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Requisição {self.id} - {self.veiculo} - {self.usuario}"

    class Meta:
        verbose_name = 'Requisição'
        verbose_name_plural = 'Requisição' 