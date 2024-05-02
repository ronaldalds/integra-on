from django.contrib.admin import ModelAdmin, register
from .models import (
    UserTelegram,
    BotTelegram,
    TipoOs,
    TecnicoMensagem,
    TempoSla,
    InformacaoOs,
    Log,
    ErrorOs
)


@register(UserTelegram)
class UserTelegramAdmin(ModelAdmin):
    list_display = ("mk", "nome", "chat_id", "ativo")
    list_display_links = list_display
    list_filter = ("mk", "ativo")
    search_fields = ["nome", "chat_id"]


@register(BotTelegram)
class BotTelegramAdmin(ModelAdmin):
    list_display = ("nome", "token", "ativo")
    list_display_links = list_display


@register(TipoOs)
class TipoOsAdmin(ModelAdmin):
    list_display = ("tipo", "sla", "ativo")
    list_display_links = list_display
    list_filter = ("ativo",)
    search_fields = ["tipo",]


@register(TecnicoMensagem)
class TecnicoMensagemAdmin(ModelAdmin):
    list_display = (
        "nome_tecnico",
        "chat_id",
        "mensagem",
        "sla",
        "cod_os",
        "data_envio",
        "envio",
    )
    list_display_links = list_display
    list_filter = ("envio", "data_envio")
    search_fields = ["nome_tecnico", "cod_os"]


@register(TempoSla)
class TempoSlaAdmin(ModelAdmin):
    list_display = ("sla",)
    list_display_links = list_display


@register(InformacaoOs)
class InformacaoOsAdmin(ModelAdmin):
    list_display = ("id_tipo_os", "nome")
    list_display_links = list_display


@register(Log)
class LogAdmin(ModelAdmin):
    list_display = ("data_envio",)
    list_display_links = list_display
    list_filter = ("data_envio",)


@register(ErrorOs)
class ErrorOsAdmin(ModelAdmin):
    list_display = (
        "os",
        "tipo",
        "operador",
        "detalhe",
        "created_at",
    )
    list_display_links = list_display
    list_filter = ("created_at", "operador")
    search_fields = ["operador", "os"]
