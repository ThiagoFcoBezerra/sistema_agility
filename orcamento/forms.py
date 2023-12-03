
from django.forms import ModelForm
from orcamento.models import Lancamento, Categoria, Orcamento


class LancamentoForm(ModelForm):
    class Meta:
        model = Lancamento
        fields = '__all__'
        labels = {
            'categoria': 'Categoria',
            'descricao': 'Descrição',
            'valor_pago': 'Valor Pago',
            'Data_pagamento': 'Data do Pagamento'
        }

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = ('nome',)
        labels = {'nome': 'Nome da Categoria'}

class OrcamentoForm(ModelForm):
    class Meta:
        model = Orcamento
        fields = '__all__'
        labels = {
            'categoria': 'Categoria',
            'data_orcamento' : 'Data do Orcamento',
            'descricao' : 'Descrição',
            'valor_orc' : 'Valor'
        }