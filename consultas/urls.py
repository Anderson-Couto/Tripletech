from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('agendar', views.agendar, name='agendar'),
    path('atualizar', views.atualizar, name='atualizar'),
    path('minha-consulta', views.revisao_consulta, name='minha_consulta'),
]
