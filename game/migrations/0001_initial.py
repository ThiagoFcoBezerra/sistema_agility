# Generated by Django 4.0.3 on 2024-04-06 19:17

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_nome', models.CharField(max_length=50)),
                ('pontos', models.DecimalField(decimal_places=2, max_digits=6)),
                ('peso', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano_refencia', models.CharField(max_length=10)),
                ('objetivo', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('pontos', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_nome', models.CharField(max_length=50)),
                ('pontos', models.DecimalField(decimal_places=2, max_digits=6)),
                ('peso', models.DecimalField(decimal_places=2, max_digits=6)),
                ('realizado_anterior', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('realizado', models.DecimalField(decimal_places=2, max_digits=6)),
                ('orcado', models.DecimalField(decimal_places=2, max_digits=6)),
                ('data_atualizacao', models.DateField(blank=True, default=datetime.datetime(2000, 1, 10, 0, 0))),
                ('meta_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.area')),
            ],
            options={
                'permissions': [('Atualiza_metas', 'Pode atualizar metas')],
            },
        ),
        migrations.CreateModel(
            name='GameMensal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes_referencia', models.CharField(max_length=20)),
                ('objetivo', models.DecimalField(decimal_places=0, max_digits=4)),
                ('pontos', models.DecimalField(decimal_places=2, max_digits=6)),
                ('game_ano', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.game')),
            ],
        ),
        migrations.AddField(
            model_name='area',
            name='game_mes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.gamemensal'),
        ),
    ]
