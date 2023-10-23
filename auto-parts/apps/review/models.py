from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from apps.parts.models import AutoParts
from apps.users.models import Master

User = get_user_model()


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="%(class)s_reviews",
    )
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def perform_soft_delete(self):
        self.active = False
        self.save()


class MasterReview(Review):
    reviewed_object = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        verbose_name="Мастер",
        related_name="master_reviews",
    )

    class Meta:
        verbose_name = "Отзыв мастера"
        verbose_name_plural = "Отзывы мастеров"

    def __str__(self):
        return f"{self.user} - {self.reviewed_object}"


class AutoPartsReview(Review):
    reviewed_object = models.ForeignKey(
        AutoParts,
        on_delete=models.CASCADE,
        verbose_name="Запчасть",
        related_name="auto_parts_reviews",
    )

    class Meta:
        verbose_name = "Отзыв запчасти"
        verbose_name_plural = "Отзывы запчастей"

    def __str__(self):
        return f"{self.user} - {self.reviewed_object}"
