# Generated by Django 4.0.3 on 2024-05-14 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('almox', '0003_alter_pedido_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='localizacao',
            name='producao',
            field=models.BooleanField(default=False),
        ),
    ]
