# Generated by Django 4.0.3 on 2022-12-20 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_meta_data_atualizacao_meta_pontos_anterior'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meta',
            old_name='pontos_anterior',
            new_name='realizado_anterior',
        ),
    ]
