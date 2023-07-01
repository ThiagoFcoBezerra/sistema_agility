from django.contrib import admin
from orcamento.models import Categoria, Lancamento, Orcamento, Autorizacao, Faturamento
# Register your models here.


admin.site.register(Categoria)
admin.site.register(Lancamento)
admin.site.register(Faturamento)

class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'data_orcamento', 'descricao', 'valor_orc')
admin.site.register(Orcamento, OrcamentoAdmin)
admin.site.register(Autorizacao)