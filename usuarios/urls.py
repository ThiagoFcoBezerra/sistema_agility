from django.urls import path
from . import views


urlpatterns = [
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('usuarios', views.usuarios, name='usuarios'),
    path('exclui_usuario/<int:id>', views.exclui_usuario, name='exclui_usuario'),
    path('edita_usuario/<int:id>', views.edita_usuario, name='edita_usuario'),
    path('cira_grupo', views.cria_grupo, name='cria_grupo'),
]