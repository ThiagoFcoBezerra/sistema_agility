# Generated by Django 4.0.3 on 2024-04-06 19:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Faturamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faturamento_data', models.DateField()),
                ('faturamento_valor', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Orcamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_orcamento', models.DateField()),
                ('descricao', models.CharField(blank=True, max_length=200)),
                ('valor_orc', models.DecimalField(decimal_places=2, max_digits=10)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orcamento.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Lancamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=200)),
                ('valor_pago', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_pagamento', models.DateField()),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orcamento.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Autorizacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateField(auto_now_add=True)),
                ('data_autorizacao', models.DateField(auto_now=True)),
                ('valor_autorizacao', models.DecimalField(decimal_places=2, max_digits=11)),
                ('autorizacao_status', models.CharField(choices=[('APR', 'Aprovado'), ('REP', 'Reprovado'), ('AGU', 'Aguardando')], default='AGU', max_length=3)),
                ('justificativa', models.TextField()),
                ('despacho', models.TextField(blank=True)),
                ('descreve_utilizacao', models.TextField(blank=True)),
                ('utilizada', models.BooleanField(blank=True, default=False)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orcamento.categoria')),
                ('despachante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='despachante', to=settings.AUTH_USER_MODEL)),
                ('solicitante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitante', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('pode_despachar', 'Pode despachar autorizações')],
            },
        ),
    ]
