# Generated by Django 4.0.3 on 2023-01-25 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0004_relato_relato'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contato',
            name='agendamento',
        ),
    ]
