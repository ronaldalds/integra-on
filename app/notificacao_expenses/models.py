from django.db import models


class GestorExpense(models.Model):
    nome = models.CharField(max_length=128)
    setor = models.CharField(max_length=128)
    ativo = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Gestores Expense"

    def __str__(self) -> str:
        return self.nome


class UserVexpenses(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=256)
    gestor_id = models.ForeignKey(GestorExpense, on_delete=models.PROTECT)
    operacao = models.CharField(max_length=128, blank=True, null=True)
    ativo = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.nome


class LogNotificacao(models.Model):
    user_id = models.ForeignKey(UserVexpenses, on_delete=models.PROTECT)
    grupo = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    avulso = models.IntegerField()
    aberto = models.IntegerField()



class Notificar(models.Model):
    nome = models.CharField(max_length=256)
    gestor_id = models.ForeignKey(GestorExpense, on_delete=models.PROTECT)
    grupo = models.BigIntegerField()
    operacao = models.CharField(max_length=128)
    token_bot = models.CharField(max_length=256)
    ativo = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.nome
