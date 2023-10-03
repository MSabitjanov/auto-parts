from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
    user = models.ManyToManyField(
        User, verbose_name="Пользователь", related_name="chats"
    )
    seller_name = models.CharField(max_length=50, verbose_name="Имя продавца")
    customer_name = models.CharField(max_length=50, verbose_name="Имя покупателя")
    unread_messages_count = models.PositiveSmallIntegerField(
        verbose_name="Количество непрочитанных сообщений", default=0
    )
    last_message_received_time = models.DateTimeField(
        verbose_name="Время последнего сообщения"
    )

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"

    def __str__(self):
        return f"Чат {self.id}"


class Messages(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Отправитель",
        related_name="sender",
    )
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, verbose_name="Чат", related_name="messages"
    )
    is_read = models.BooleanField(verbose_name="Прочитано", default=False)
    content = models.TextField(verbose_name="Cообщение")
    attachment = models.FileField(
        upload_to="attachments/", blank=True, verbose_name="Вложение"
    )
    send_time = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки")
