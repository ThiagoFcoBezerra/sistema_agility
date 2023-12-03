from django.urls import path
from cliente import views


urlpatterns = [
    path('contatos', views.contatos, name='contatos'),
    path('cria_motivo', views.cria_motivo, name='cria_motivo'),
    path('cria_contato', views.cria_contato, name='cria_contato'),
    path('cria_relato/<int:id>', views.cria_relato, name='cria_relato'),
]