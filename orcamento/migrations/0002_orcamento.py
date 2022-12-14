# Generated by Django 4.0.3 on 2022-03-28 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orcamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_orcamento', models.DateField()),
                ('descricao', models.CharField(max_length=200)),
                ('valor_orc', models.DecimalField(decimal_places=2, max_digits=10)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orcamento.categoria')),
            ],
        ),
    ]
