from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('testa_arquivo', views.testa_arquivo , name='testa_arquivo'),
    #path('exibe_lancamentos', views.exibir_lancamentos , name='exibe_lancamentos'),
    #path('<int:var1>/<int:var2>', views.exibir_lancamentos2 , name='exibe_lancamentos2'),
    path('orcamento', views.orcamento, name='orcamento'),
    path('cadastra_orcamento', views.cadastra_orcamento, name='cadastra_orcamento'),
    path('detalhes/<int:id>/<int:m>', views.detalhes, name='detalhes'),
    path('cadastra_faturamento', views.cadastra_faturamento, name='cadastra_faturamento'),
    path('resultado',views.resultado, name='resultado'),
    path('exclui_faturamento/<int:id>',views.exclui_faturamento, name='exclui_faturamento'),
    path('atualiza_faturamento/<int:id>', views.atualiza_faturamento, name='atualiza_faturamento'),
    path('cria_autorizacao', views.cria_autorizacao, name='cria_autorizacao'),
    path('lista_autorizacao', views.lista_autorizacao, name='lista_autorizacao'),
    path('carrega_autorizacao/<int:id>', views.carrega_autorizacao , name='carrega_autorizacao'),
    path('edita_autorizacao', views.edita_autorizacao , name='edita_autorizacao'),
    path('exclui_autorizacao/<int:id>', views.exclui_autorizacao , name='exclui_autorizacao'),
    path('despacha_autorizacao', views.despacha_autorizacao , name='despacha_autorizacao'),
    path('detalha_autorizacao/<int:id>', views.detalha_autorizacao , name='detalha_autorizacao'),

]