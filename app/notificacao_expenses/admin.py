from django.contrib.admin import ModelAdmin, register
from .models import GestorExpense, UserVexpenses, LogNotificacao, Notificar


@register(GestorExpense)
class GestorExpenseAdmin(ModelAdmin):
    list_display = (
        "nome",
        "setor",
        "ativo",
        )
    list_display_links = list_display
    list_filter = ("setor", "ativo")

    search_fields = [
        "nome",
        "setor",
    ]


@register(UserVexpenses)
class UserVexpensesAdmin(ModelAdmin):
    list_display = (
        "id",
        "nome",
        "gestor_id",
        "operacao",
        "ativo",
        )
    list_display_links = list_display
    list_filter = ("gestor_id__nome", "ativo")
    search_fields = [
        "id",
        "nome",
        "gestor_id__nome",
    ]


@register(LogNotificacao)
class LogNotificacaoAdmin(ModelAdmin):
    list_display = (
        "user_id",
        "grupo",
        "created_at",
        "avulso",
        "aberto",
    )
    list_display_links = list_display
    search_fields = [
        "user_id__nome",
        "user_id__gestor_id__nome",
    ]


@register(Notificar)
class NotificarAdmin(ModelAdmin):
    list_display = (
        "nome",
        "gestor_id",
        "grupo",
        "operacao",
        "token_bot",
        "ativo",
    )
    list_display_links = list_display
    list_filter = ("gestor_id__nome", "ativo")
    search_fields = [
        "gestor_id__nome"
    ]
