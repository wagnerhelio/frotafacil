from django.db import models

class Agente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    matricula = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.nome} ({self.matricula})" 