# Generated by Django 5.0.4 on 2024-05-02 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mkat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermkat',
            name='ativo',
            field=models.BooleanField(default=False),
        ),
    ]