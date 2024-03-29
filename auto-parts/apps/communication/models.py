import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ValidationError

User = get_user_model()


class Chat(models.Model):
    """
    Модель чата, в которой хранятся все чаты пользователей.
    Мастера и покупатели могут общаться только в рамках одного чата.
    """

    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(
        User, verbose_name="Участники", related_name="chats"
    )
    unread_messages_count = models.PositiveSmallIntegerField(
        verbose_name="Количество непрочитанных сообщений", default=0
    )
    last_message_received_time = models.DateTimeField(
        verbose_name="Время последнего сообщения", blank=True, null=True
    )
    last_message = models.CharField(
        max_length=100, verbose_name="Последнее сообщение", blank=True, null=True
    )
    is_active = models.BooleanField(verbose_name="Активный чат", default=True)

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"

    def __str__(self):
        return f"Чат {self.id}"
    
    def perform_soft_delete(self):
        self.is_active = False
        self.save()


def get_upload_path(instance, filename):
    return f"{instance.chat.id}/{filename}"

class Messages(models.Model):
    """
    Все сообщения которые отправляются в чате.
    """

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
    content = models.TextField(verbose_name="Cообщение", null=True, blank=True)
    attachment = models.FileField(
        upload_to=get_upload_path, blank=True, verbose_name="Вложение"
    )
    send_time = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"Сообщение {self.id}"
