# Generated by Django 4.0.3 on 2023-01-25 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_alter_contato_data_agendamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='relato',
            name='relato',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]