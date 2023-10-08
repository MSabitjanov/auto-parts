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
        related_name="reviews",
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    reviewed_object = GenericForeignKey("content_type", "object_id")
    comment = models.TextField(verbose_name="Комментарий")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка")
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    # Setting generic relation in order to get all reviews for a specific part
    part_reviews = GenericRelation(AutoParts, related_query_name="part_reviews")
    # Setting generic relation in order to get all reviews for a specific master
    master_reviews = GenericRelation(Master, related_query_name="master_reviews")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв от {self.user.email}"
