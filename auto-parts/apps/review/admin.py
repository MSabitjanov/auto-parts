from django.contrib import admin

from .models import MasterReview, AutoPartsReview, ReviewStatistics


@admin.register(MasterReview)
class MasterReviewAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "reviewed_object",
        "comment",
        "rating",
        "created_at",
        "active",
    )

    search_fields = ("user__email", "comment")
    search_help_text = "Поиск по email, комментарию"
    list_filter = ("active",)
    date_hierarchy = "created_at"
    readonly_fields = ("rating", "created_at")


@admin.register(AutoPartsReview)
class AutoPartsReviewAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "reviewed_object",
        "comment",
        "rating",
        "created_at",
        "active",
    )

    search_fields = ("user__email", "comment")
    search_help_text = "Поиск по email, комментарию"
    list_filter = ("active",)
    date_hierarchy = "created_at"
    # readonly_fields = ("rating", "created_at")
    
    
@admin.register(ReviewStatistics)
class ReviewStatisticsAdmin(admin.ModelAdmin):
    list_display = ("id", "master_review", "auto_parts_review", "total_review_numbers", "total_review_score")
