from django.db import models


class UserTelegram(models.Model):
    chat_id = models.BigIntegerField(primary_key=True, unique=True)
    mk = models.IntegerField()
    nome = models.CharField(max_length=256)
    ativo = models.BooleanField(default=False)


class BotTelegram(models.Model):
    nome = models.CharField(max_length=256)
    token = models.CharField(max_length=256)
    ativo = models.BooleanField(default=False)


class TipoOs(models.Model):
    tipo = models.CharField(max_length=300)
    sla = models.IntegerField()
    ativo = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.tipo)

    class Meta:
        verbose_name_plural = 'Tipo O.S.'


class TecnicoMensagem(models.Model):
    nome_tecnico = models.CharField(max_length=128)
    chat_id = models.BigIntegerField()
    mensagem = models.TextField()
    sla = models.IntegerField()
    cod_os = models.IntegerField()
    data_envio = models.DateTimeField(auto_now=True)
    envio = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.chat_id)

    class Meta:
        verbose_name_plural = 'Mensagens'


class TempoSla(models.Model):
    sla = models.IntegerField(primary_key=True, unique=True)

    def __str__(self) -> str:
        return f"{self.sla}"

    class Meta:
        verbose_name_plural = 'S.L.A.'


class InformacaoOs(models.Model):
    id_tipo_os = models.ForeignKey(TipoOs, on_delete=models.CASCADE)
    nome = models.CharField(max_length=300)

    def __str__(self) -> str:
        return f"{self.nome} - {self.id_tipo_os}"

    class Meta:
        verbose_name_plural = 'Informacões O.S.'


class Log(models.Model):
    data_envio = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Logs'


class ErrorOs(models.Model):
    os = models.BigIntegerField(primary_key=True, unique=True)
    tipo = models.CharField(max_length=128)
    operador = models.CharField(max_length=128)
    detalhe = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

