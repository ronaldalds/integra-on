from django.contrib.admin import ModelAdmin, register
from .models import Chamado, Interacao


@register(Chamado)
class ChamadoAdmin(ModelAdmin):
    list_display = (
        "andamento",
        "chave",
        "cod_chamado",
        "qnt_interacao",
        "nome_grupo",
        "nome_categoria",
        "data_finalizacao",
        "nome_operador",
        "nome_status",
        "nome_sistema",
        )
    list_display_links = list_display
    list_filter = ("andamento", "nome_status", "nome_categoria", "nome_operador")

    search_fields = [
        "chave",
        "cod_chamado",
        "nome_categoria",
    ]

    readonly_fields = [
        "total_horas_1_atendimento",
        "total_horas_1_2_atendimento",
        "tempo_restante_1",
        "tempo_restante_2",
    ]


@register(Interacao)
class InteracaoAdmin(ModelAdmin):
    list_display = (
        "chave",
        "chamado",
        "data_criacao",
        "seguencia",
        "status_acao_nome_relatorio",
        "fantasia_fornecedor",
        "chamado_aprovadores",
        "tempo_corrido_interacao",
    )

    search_fields = [
        "chamado__cod_chamado",
        "chamado__assunto",
    ]

    readonly_fields = [
        "tempo_corrido_interacao",
    ]
