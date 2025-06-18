from django.urls import path
from .views_veiculo import (
    cadastrar_veiculo_views,
    editar_veiculo_view,
    listar_veiculo_views,
    excluir_veiculo_view,
    home_veiculo_view
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
)

urlpatterns = [
    path('', home_veiculo_view, name='home_veiculo'),
    path('cadastrar/', cadastrar_veiculo_views, name='cadastrar_veiculo'),
    path('editar/<int:veiculo_id>/', editar_veiculo_view, name='editar_veiculo'),
    path('listar/', listar_veiculo_views, name='listar_veiculo'),
    path('excluir/<int:veiculo_id>/', excluir_veiculo_view, name='excluir_veiculo'),
    path('requisicao/', listar_requisicao, name='listar_requisicao'),
    path('requisicao/cadastrar/', cadastrar_requisicao, name='cadastrar_requisicao'),
    path('requisicao/finalizar/<int:pk>/', finalizar_requisicao, name='finalizar_requisicao'),
    path('requisicao/home/', home_requisicao, name='home_requisicao'),
    path('requisicao/editar/<int:pk>/', editar_requisicao, name='editar_requisicao'),
    path('requisicao/excluir/<int:pk>/', excluir_requisicao, name='excluir_requisicao'),
    path('requisicao/aprovar/<int:pk>/', aprovar_requisicao, name='aprovar_requisicao'),
    path('requisicao/recusar/<int:pk>/', recusar_requisicao, name='recusar_requisicao'),
    path('requisicao/visualizar/<int:pk>/', visualizar_requisicao, name='visualizar_requisicao'),
    path('requisicao/toggle_aprovacao_automatica/', toggle_aprovacao_automatica, name='toggle_aprovacao_automatica'),
]
