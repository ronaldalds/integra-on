from django.db import models


class TokenVexpenses(models.Model):
    nome = models.CharField(max_length=128)
    token = models.CharField(max_length=256)
