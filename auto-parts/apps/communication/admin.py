from django.contrib import admin

from .models import Chat, Messages


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "seller_name",
        "customer_name",
        "unread_messages_count",
        "last_message_received_time",
    )
    list_display_links = ("id", "seller_name", "customer_name")
    search_fields = ("user__email",)
    search_help_text = "Email пользователя"
    readonly_fields = ("unread_messages_count", "last_message_received_time")


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = (
        "sender",
        "chat",
        "is_read",
        "content",
        "attachment",
        "send_time",
    )
    search_fields = ("sender__email", "chat__id")
    search_help_text = "Email пользователя"
    readonly_fields = (
        "is_read",
        "send_time",
    )
