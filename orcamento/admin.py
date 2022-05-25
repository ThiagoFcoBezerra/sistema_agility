from django.contrib import admin
from orcamento.models import Categoria, Lancamento, Orcamento
# Register your models here.


admin.site.register(Categoria)
admin.site.register(Lancamento)
admin.site.register(Orcamento)