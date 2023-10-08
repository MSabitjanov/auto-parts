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
    )
    search_fields = ("user__email",)
    search_help_text = "Поиск по email"
    readonly_fields = ("content_type", "object_id")
