from django.contrib import admin

from .models import MasterImages, AutoPartsImages


@admin.register(MasterImages)
class MasterImagesAdmin(admin.ModelAdmin):
    list_display = (
        "master",
        "image",
    )
    search_fields = ("master__user__email",)
    search_help_text = "Поиск по email"


@admin.register(AutoPartsImages)
class AutoPartsImagesAdmin(admin.ModelAdmin):
    list_display = (
        "auto_part",
        "image",
    )
    search_fields = ("auto_part__seller__user__email",)
    search_help_text = "Поиск по email"
