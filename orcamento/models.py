from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Lancamento(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=200)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateField(auto_now = False, auto_now_add = False)

    def __str__(self):
        return self.descricao

class Orcamento(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    data_orcamento = models.DateField()
    descricao = models.CharField(max_length=200, blank=True)
    valor_orc = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.categoria.nome} - {self.descricao}'

class Faturamento(models.Model):
    faturamento_data = models.DateField()
    faturamento_valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.faturamento_data} - {self.faturamento_valor}'

class Autorizacao(models.Model):

    class Meta:
        permissions = [
            ("pode_despachar", "Pode despachar autorizações"),
        ]
    
    STATUS = [
        ('APR', 'Aprovado'),
        ('REP', 'Reprovado'),
        ('AGU', 'Aguardando')
    ]
    
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    data_criacao = models.DateField(auto_now_add=True)
    data_autorizacao = models.DateField(auto_now=True)
    valor_autorizacao = models.DecimalField(max_digits=11, decimal_places=2)
    autorizacao_status = models.CharField(choices=STATUS, default='AGU', max_length=3, blank=False, null=False)
    justificativa = models.TextField(blank=False)
    despacho = models.TextField(blank=True)
    descreve_utilizacao = models.TextField(blank=True)
    utilizada = models.BooleanField(default=False, blank=True)
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE,related_name='solicitante', null=True)
    despachante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='despachante', null=True, blank=True)
    
    def __str__(self):
        return f'{self.data_criacao} / {self.categoria} / {self.valor_autorizacao} / {self.autorizacao_status}'
