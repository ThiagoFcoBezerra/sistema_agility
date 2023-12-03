from django.urls import path
from . import views


urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('atualiza_game', views.atualiza_game, name='atualiza_game'),
    path('apura_game', views.apura_game, name='apura_game'),
]