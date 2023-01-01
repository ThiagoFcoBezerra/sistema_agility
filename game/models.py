import datetime
from django.db import models

# Create your models here.

class Game(models.Model):
    ano_refencia = models.IntegerField()
    objetivo = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    pontos = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'Game {self.ano_refencia} => {self.pontos}'

class GameMensal(models.Model):
    game_ano = models.ForeignKey(Game, on_delete= models.CASCADE)
    mes_referencia = models.IntegerField()
    objetivo = models.DecimalField(max_digits=4, decimal_places=0)
    pontos = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        data = datetime.date(2000, self.mes_referencia,1)
        return f'{data.strftime("%B")} - {self.game_ano}'

class Area(models.Model):
    game_mes = models.ForeignKey(GameMensal, on_delete=models.CASCADE)
    area_nome = models.CharField(max_length=50)
    pontos = models.DecimalField(max_digits=6, decimal_places=2)
    peso = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.area_nome} - {self.game_mes}'

class Meta(models.Model):

    class Meta:
        permissions = [
            ("Atualiza_metas", "Pode atualizar metas"),
        ]
    meta_area = models.ForeignKey(Area, on_delete=models.CASCADE)
    meta_nome = models.CharField(max_length=50)
    pontos = models.DecimalField(max_digits=6,decimal_places=2)
    peso = models.DecimalField(max_digits=6, decimal_places=2)
    realizado_anterior = models.DecimalField(max_digits=6,decimal_places=2, default=0)
    realizado = models.DecimalField(max_digits=6, decimal_places=2)
    orcado = models.DecimalField(max_digits=6, decimal_places=2)
    data_atualizacao = models.DateField(blank=True, default=datetime.datetime(2000,1,10))

    def __str__(self) -> str:
        return f'{self.meta_nome} - {self.meta_area}'
