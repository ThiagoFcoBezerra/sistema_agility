from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Motivo(models.Model):
    descricao = models.CharField(max_length=30)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.descricao

class Contato(models.Model):
    OPCAO_RESULTADO = (
        ('SIM', 'Produto Vendido'),
        ('NAO', 'Venda Não Realizada'),

    )
    data = models.DateField(auto_now_add=True)
    cliente = models.CharField(max_length=30)
    motivo = models.ForeignKey(Motivo,on_delete=models.CASCADE)
    concluido = models.BooleanField(default= False)
    resultado = models.CharField(max_length=3, choices=OPCAO_RESULTADO, blank=True)
    data_agendamento = models.DateField(blank=True, null=True)

class Relato(models.Model):
    data = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)
    relato = models.TextField()
