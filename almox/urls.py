from django.urls import path
from almox import views


urlpatterns = [
    path('pedidos', views.pedidos, name='pedidos'),
    path('produtos', views.produtos, name='produtos'),
    path('cadastro', views.cadastra_produto, name='cadastro'),
    path('edita_produto/<int:id>', views.edita_produto, name='edita_produto'),
    path('cadastra_pedido/<int:id>', views.cadastra_pedido, name='cadastro_pedido'),
    path('fecha_pedido/<int:id>', views.fecha_pedido, name='fecha_pedido'),
    path('despacha_pedido/<int:id>', views.despacha_pedido, name='despacha_pedido'),
    path('cadastra_item_produto/<int:id>', views.entrada_item_produto, name='cadastra_item_produto'),
    path('move_itens/<int:id>',views.move_itens, name='move_itens'),
    path('recupera_itens/<int:id>',views.recupera_itens, name='recupera_itens'),
    path('entrega_pedido/<int:id>',views.entrega_pedido, name='entrega_pedido'),
    path('recebe_pedido/<int:id>',views.recebe_pedido, name='recebe_pedido'),
    path('cadastra_categoria',views.cadastra_categoria, name='cadastra_categoria'),
    path('cadastra_marca',views.cadastra_marca, name='cadastra_marca'),
    path('cadastra_fornecedor',views.cadastra_fornecedor, name='cadastra_fornecedor'),
    path('cadastra_unidade',views.cadastra_unidade, name='cadastra_unidade'),
    path('cadastra_local',views.cadastra_local, name='cadastra_local'),
    path('detalha_local/<int:id>',views.detalha_local, name='detalha_local'),
    path('lista_locais',views.lista_locais, name='lista_locais'),
    path('lista_itens/<int:id>',views.lista_itens, name='lista_itens'),
    path('lista_movimento/<int:id>',views.lista_movimento, name='lista_movimento'),
]
