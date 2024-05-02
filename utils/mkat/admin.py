from django.contrib.admin import ModelAdmin, register
from .models import UserMkat


@register(UserMkat)
class UserMkatAdmin(ModelAdmin):
    list_display = ("nome", "token", "ativo")
    list_display_links = list_display
