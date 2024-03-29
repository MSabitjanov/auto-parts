from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from modeltranslation.admin import TranslationAdmin

from .models import AutoPartsCategory, Brand, AutoParts


@admin.register(AutoPartsCategory)
class AutoPartsCategoryAdmin(MPTTModelAdmin, TranslationAdmin):
    list_display = (
        "name",
        "id",
        "parent",
        "characteristics",
    )
    list_filter = ("parent",)
    search_fields = ("name",)
    mptt_level_indent = 30


@admin.register(Brand)
class BrandAdmin(TranslationAdmin):
    list_display = ("name", "id")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(AutoParts)
class AutoPartsAdmin(TranslationAdmin):
    list_display = (
        "category",
        "id",
        "brand",
        "seller",
        "is_new",
        "price",
        "rating",
        "characteristics",
        "date_of_pubication",
        "last_updated",
    )
    list_filter = ("category", "brand", "seller", "is_new")
    search_fields = ("category", "brand", "seller__email", "is_new")
    readonly_fields = ("rating",)
