from django.urls import path
from .views_veiculo import (
    cadastrar_veiculo_views,
    editar_veiculo_view,
    listar_veiculo_views,
    excluir_veiculo_view,
    home_veiculo_view,
    exportar_veiculos_pdf
)
from .views_requisicao import (
    listar_requisicao,
    cadastrar_requisicao,
    finalizar_requisicao,
    home_requisicao,
    editar_requisicao,
    excluir_requisicao,
    aprovar_requisicao,
    recusar_requisicao,
    visualizar_requisicao,
    toggle_aprovacao_automatica,
    exportar_requisicoes_pdf
)
from .views_agente import home_agente_view, cadastrar_agente_view, listar_agente_view, buscar_ldap_view

urlpatterns = [
    #Veículo
    path('veiculo/', home_veiculo_view, name='home_veiculo'),
    path('cadastrar_veiculo/', cadastrar_veiculo_views, name='cadastrar_veiculo'),
    path('editar_veiculo/<int:veiculo_id>/', editar_veiculo_view, name='editar_veiculo'),
    path('listar_veiculo/', listar_veiculo_views, name='listar_veiculo'),
    path('excluir_veiculo/<int:veiculo_id>/', excluir_veiculo_view, name='excluir_veiculo'),
    path('veiculo/exportar_pdf/', exportar_veiculos_pdf, name='exportar_veiculos_pdf'),
    #Requisição
    path('requisicao/', home_requisicao, name='home_requisicao'),
    path('requisicao/cadastrar_requisicao/', cadastrar_requisicao, name='cadastrar_requisicao'),
    path('requisicao/listar_requisicao/', listar_requisicao, name='listar_requisicao'),
    path('requisicao/finalizar_requisicao/<int:pk>/', finalizar_requisicao, name='finalizar_requisicao'),
    path('requisicao/editar_requisicao/<int:pk>/', editar_requisicao, name='editar_requisicao'),
    path('requisicao/excluir_requisicao/<int:pk>/', excluir_requisicao, name='excluir_requisicao'),
    path('requisicao/aprovar_requisicao/<int:pk>/', aprovar_requisicao, name='aprovar_requisicao'),
    path('requisicao/recusar_requisicao/<int:pk>/', recusar_requisicao, name='recusar_requisicao'),
    path('requisicao/visualizar_requisicao/<int:pk>/', visualizar_requisicao, name='visualizar_requisicao'),
    path('requisicao/toggle_aprovacao_automatica/', toggle_aprovacao_automatica, name='toggle_aprovacao_automatica'),
    path('requisicao/exportar_pdf/', exportar_requisicoes_pdf, name='exportar_requisicoes_pdf'),
    path('agente/', home_agente_view, name='home_agente'),
    path('agente/novo/', cadastrar_agente_view, name='cadastrar_agente'),
    path('agente/listar/', listar_agente_view, name='listar_agente'),
    path('agente/buscar-ldap/', buscar_ldap_view, name='buscar_ldap'),
]
