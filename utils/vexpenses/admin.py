from django.contrib.admin import ModelAdmin, register
from .models import TokenVexpenses


@register(TokenVexpenses)
class TokenVexpensesAdmin(ModelAdmin):
    list_display = (
        "id",
        "nome",
        "token",
        )
    list_display_links = list_display
