# Models are defined in models_veiculo.py
from .models_veiculo import Veiculo
from django.db import models
from .models_agente import Agente
from .models_ferias import FeriasAgente
from django.contrib.auth.models import User

# Create your models here.

class ControleAprovacoes(models.Model):
    aprovacao_automatica = models.BooleanField('Aprovação automática de requisições', default=False)

    def __str__(self):
        return "Controle de Aprovações"

    class Meta:
        verbose_name = 'Controle de Aprovações'
        verbose_name_plural = 'Controle de Aprovações'

class Notificacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
    mensagem = models.CharField(max_length=255)
    lida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username}: {self.mensagem[:30]}{'...' if len(self.mensagem) > 30 else ''}"