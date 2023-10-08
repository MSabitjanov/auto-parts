from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "content_type",
        "object_id",
        "reviewed_object",
        "comment",
        "rating",
        "part_reviews",
        "master_reviews",
        "active",
        "created_at",
    )
    search_fields = ("user__email", "comment")
    search_help_text = "Поиск по email, комментарию"
    list_filter = ("active",)
    date_hierarchy = "created_at"
    readonly_fields = ("user", "rating", "active", "content_type", "object_id")
