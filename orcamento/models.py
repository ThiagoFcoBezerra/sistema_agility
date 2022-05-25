from tkinter import CASCADE
from django.db import models

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




