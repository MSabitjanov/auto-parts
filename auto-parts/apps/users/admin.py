from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from mptt.admin import MPTTModelAdmin

from modeltranslation.admin import TranslationAdmin

from .models import User, Master, Seller, MasterSkill, Region


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "id",
        "first_name",
        "last_name",
        "phone_number",
    )
    search_fields = ("email",)
    search_help_text = "Поиск по email"
    date_hierarchy = "date_joined"

    readonly_fields = "last_login", "date_joined"
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "profile_image",
                    "wishlist_master",
                    "wishlist_parts",
                ]
            },
        ),
        (
            "More",
            {
                "classes": ["collapse"],
                "fields": [
                    "password",
                    "date_joined",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "is_staff",
                    "is_active",
                ],
            },
        ),
    ]


@admin.register(Master)
class MasterAdmin(TranslationAdmin, OSMGeoAdmin):
    list_display = (
        "user",
        "region",
        "rating",
        "start_of_carrier",
        "phone_number",
        "is_recommended",
        "date_of_birth",
        "last_visited",
        "date_of_join",
    )
    search_fields = ("user__email", "phone_number")
    search_help_text = "Поиск по email, номеру телефона"
    date_hierarchy = "date_of_join"
    list_editable = ("is_recommended",)
    readonly_fields = ("rating",)
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "user",
                    "region",
                    "start_of_carrier",
                    "date_of_birth",
                    "phone_number",
                    "website",
                    "working_hours",
                    "is_recommended",
                    "rating",
                    "skilled_at",
                    "description",
                    "location",
                ]
            },
        ),
    ]


@admin.register(Seller)
class SellerAdmin(TranslationAdmin, OSMGeoAdmin):
    list_display = (
        "user",
        "region",
        "company_name",
        "company_phone",
        "seller_phone",
        "website",
        "company_info",
        "rating",
        "date_of_join",
        # "location",
    )
    search_fields = ("user__email", "company_name", "company_phone", "seller_phone")
    search_help_text = "Поиск по email, названию компании, номеру телефона компании, номеру телефона продавца"
    date_hierarchy = "date_of_join"
    list_filter = (
        "region",
        "rating",
    )

    readonly_fields = "rating", "date_of_join"
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "user",
                    "region",
                    "company_name",
                    "company_phone",
                    "seller_phone",
                    "website",
                    "working_hours",
                    "company_info",
                    "rating",
                    "date_of_join",
                    "seller_images",
                    "location",
                ]
            },
        ),
    ]


@admin.register(MasterSkill)
class MasterSkillAdmin(MPTTModelAdmin, TranslationAdmin):
    list_display = ("name", "id", "parent")
    search_fields = ("name",)
    search_help_text = "Поиск по названию"
    mptt_level_indent = 30


@admin.register(Region)
class RegionAdmin(MPTTModelAdmin, TranslationAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    search_help_text = "Поиск по названию"
    mptt_level_indent = 30
