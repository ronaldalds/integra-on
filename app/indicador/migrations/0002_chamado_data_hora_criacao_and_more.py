# Generated by Django 5.0.4 on 2024-04-30 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicador', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamado',
            name='data_hora_criacao',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interacao',
            name='data_hora_criacao',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
