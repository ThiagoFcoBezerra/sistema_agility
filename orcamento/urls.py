from django.urls import path
from orcamento import views


urlpatterns = [
    path('', views.index, name='index'),
    path('testa_arquivo', views.testa_arquivo , name='testa_arquivo'),
    path('exibe_lancamentos', views.exibir_lancamentos , name='exibe_lancamentos'),
    path('<int:var1>/<int:var2>', views.exibir_lancamentos2 , name='exibe_lancamentos2'),
    path('<int:var1>', views.orcamento, name='orcamento'),
    path('cadastra_orcamento', views.cadastra_orcamento, name='cadastra_orcamento'),
    path('detalhes/<int:id>/<int:m>', views.detalhes, name='detalhes'),
]