from django.contrib import admin
from orcamento.models import Categoria, Lancamento, Orcamento, Autorizacao
# Register your models here.


admin.site.register(Categoria)
admin.site.register(Lancamento)
admin.site.register(Orcamento)
admin.site.register(Autorizacao)