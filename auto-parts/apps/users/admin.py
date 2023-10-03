from django.contrib import admin

from .models import User, Master, Seller, MasterSkill, Region


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
    )
    search_fields = ("email",)
    search_help_text = "'Email' bo'yicha qidirish"
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
class MasterAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "date_of_birth",
        "start_of_carrier",
        "last_visited",
    )
    search_fields = ("user__email",)
    search_help_text = "Поиск по email"
    date_hierarchy = "last_visited"

    readonly_fields = ("last_visited",)
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "user",
                    "date_of_birth",
                    "start_of_carrier",
                    "skilled_at",
                    "last_visited",
                ]
            },
        ),
    ]


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "company_name",
        "region",
        "company_phone",
        "website",
        "working_hours",
        "seller_phone",
        "company_info",
        "rating",
        "date_of_join",
        # "location",
    )
    search_fields = ("user__email",)
    search_help_text = "Поиск по email"
    date_hierarchy = "date_of_join"

    readonly_fields = "date_of_join", "rating", "date_of_join"
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "user",
                    "company_name",
                    "region",
                    "company_phone",
                    "website",
                    "working_hours",
                    "seller_phone",
                    "company_info",
                    "rating",
                    "date_of_join",
                    # "location",
                ]
            },
        ),
    ]


@admin.register(MasterSkill)
class MasterSkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    search_help_text = "Поиск по названию"
