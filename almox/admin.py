from django.contrib import admin
from almox.models import Produto, Categoria, Marca, Fornecedor, Unidade, Localizacao, Movimentacao, Pedido, ItemPedido, ItemProduto

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'marca')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    
admin.site.register(Produto, ProdutoAdmin)

class ItemProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'produto', 'numero_serie')
    list_display_links = ('id', 'produto', 'numero_serie')
    search_fields = ('numero_serie',)
    
admin.site.register(ItemProduto, ItemProdutoAdmin)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    
admin.site.register(Categoria, CategoriaAdmin)

class MarcaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    
admin.site.register(Marca, MarcaAdmin)

class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    
admin.site.register(Fornecedor, FornecedorAdmin)

class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sigla')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    
admin.site.register(Unidade, UnidadeAdmin)

class LocalizacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'local')
    list_display_links = ('id', 'local')
    search_fields = ('local',)
    
admin.site.register(Localizacao, LocalizacaoAdmin)

class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'data')
    list_display_links = ('id', 'data')
    
admin.site.register(Movimentacao, MovimentacaoAdmin)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_pedido')
    list_display_links = ('id',)
    
admin.site.register(Pedido, PedidoAdmin)

class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'produto')
    list_display_links = ('id',)
    
admin.site.register(ItemPedido, ItemPedidoAdmin)

# Register your models here.
