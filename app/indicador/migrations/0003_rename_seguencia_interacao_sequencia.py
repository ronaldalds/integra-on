# Generated by Django 5.0.4 on 2024-04-30 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicador', '0002_chamado_data_hora_criacao_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interacao',
            old_name='seguencia',
            new_name='sequencia',
        ),
    ]
