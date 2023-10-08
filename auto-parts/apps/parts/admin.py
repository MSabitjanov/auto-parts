from django.contrib import admin

from .models import AutoPartsCategory, Brand, AutoParts


@admin.register(AutoPartsCategory)
class AutoPartsCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "parent",
        "characteristics",
    )
    list_filter = ("parent",)
    search_fields = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(AutoParts)
class AutoPartsAdmin(admin.ModelAdmin):
    list_display = (
        "category",
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
    readonly_fields = ("is_new", "rating")
