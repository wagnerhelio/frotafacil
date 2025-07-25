from django.db import models

class Veiculo(models.Model):
    ano_referencia = models.PositiveIntegerField(blank=True, null=True)
    mes_referencia = models.PositiveIntegerField(blank=True, null=True)
    localizacao_tribunal = models.CharField(max_length=100, blank=True, null=True)
    localizacao_secao = models.CharField(max_length=100, blank=True, null=True)
    localizacao_subsecao = models.CharField(max_length=100, blank=True, null=True)
    registro_patrimonial = models.CharField(max_length=50, blank=True, null=True)
    classificacao_grupo = models.CharField(max_length=20, blank=True, null=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    placa = models.CharField(max_length=10, unique=True)
    ano_fabricacao = models.PositiveIntegerField()
    potencia_cv = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    complemento_ac = models.BooleanField(default=False)
    complemento_dh = models.BooleanField(default=False)
    complemento_ve = models.BooleanField(default=False)
    complemento_te = models.BooleanField(default=False)
    complemento_bag = models.BooleanField(default=False)
    complemento_abs = models.BooleanField(default=False)
    tipo_combustivel = models.CharField(max_length=50, blank=True, null=True)
    estado_conservacao = models.CharField(max_length=50, blank=True, null=True)
    valor_atual_mercado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.placa} - {self.modelo} ({self.ano_fabricacao})"