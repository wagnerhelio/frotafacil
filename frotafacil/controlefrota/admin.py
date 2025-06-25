from django.contrib import admin
from .models_veiculo import Veiculo
from .models_requisicao import Requisicao
from .models import ControleAprovacoes

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'ano_fabricacao')
    list_filter = ('marca', 'ano_fabricacao')
    search_fields = ('placa', 'marca', 'modelo')
    ordering = ('placa',)

@admin.register(Requisicao)
class RequisicaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'veiculo', 'usuario', 'status', 'data_saida', 'data_chegada')
    list_filter = ('status', 'veiculo')
    search_fields = ('veiculo__placa', 'usuario__username', 'unidade', 'itinerario')

@admin.register(ControleAprovacoes)
class ControleAprovacoesAdmin(admin.ModelAdmin):
    list_display = ('aprovacao_automatica',)