# Generated by Django 4.0.3 on 2022-12-20 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='objetivo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
