from django.contrib import admin
from orcamento.models import Categoria, Lancamento, Orcamento, Autorizacao, Faturamento
# Register your models here.

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    list_display_links= ('id', 'nome')
    search_fields = ('nome',)

admin.site.register(Categoria, CategoriaAdmin)

class LancamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoria', 'descricao', 'valor_pago', 'data_pagamento')
    list_display_link = ('id', 'descricao')
    search_fields = ('descricao', 'data_pagamento')
    
admin.site.register(Lancamento, LancamentoAdmin)
admin.site.register(Faturamento)

class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'data_orcamento', 'descricao', 'valor_orc')
admin.site.register(Orcamento, OrcamentoAdmin)


admin.site.register(Autorizacao)