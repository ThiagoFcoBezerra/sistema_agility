# Generated by Django 4.0.3 on 2023-01-25 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contato',
            name='agendamento',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contato',
            name='concluido',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='contato',
            name='sucesso',
            field=models.BooleanField(default=False),
        ),
    ]