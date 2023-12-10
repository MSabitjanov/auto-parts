from django.db import models
from django.contrib.auth import get_user_model

from apps.users.models import Master
from apps.parts.models import AutoParts


User = get_user_model() # noqa


def get_upload_path_for_master(instance, filename):
    return f"master_images/{instance.master.user.email}/{filename}"


def get_upload_path_for_part(instance, filename):
    return f"auto_parts_by/{instance.auto_part.seller.user.email}/{filename}"

def get_upload_path_for_seller(instance, filename):
    return f"seller_images/{instance.uploaded_by.email}/{filename}"


class MasterImages(models.Model):
    """
    Модель изображений мастеров.
    """

    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        verbose_name="Мастер",
        related_name="images",
    )
    image = models.ImageField(
        upload_to=get_upload_path_for_master, verbose_name="Изображение"
    )

    class Meta:
        verbose_name = "Изображение мастера"
        verbose_name_plural = "Изображения мастеров"

    def __str__(self):
        return f"Изображение мастера {self.master.user.email}"


class AutoPartsImages(models.Model):
    """
    Модель изображений автозапчастей.
    """

    auto_part = models.ForeignKey(
        AutoParts,
        on_delete=models.CASCADE,
        verbose_name="Автозапчасть",
        related_name="images",
    )
    image = models.ImageField(
        upload_to=get_upload_path_for_part, verbose_name="Изображение"
    )

    class Meta:
        verbose_name = "Изображение автозапчасти"
        verbose_name_plural = "Изображения автозапчастей"

    def __str__(self):
        return f"Изображение автозапчасти {self.auto_part.id}"


class SellerImage(models.Model):
    """
    Модель изображений продавцов.
    """

    image = models.ImageField(
        upload_to=get_upload_path_for_seller, verbose_name="Изображение"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Загружено")
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Загрузил",
        related_name="images",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Изображение продавца"
        verbose_name_plural = "Изображения продавцов"

    def __str__(self):
        return f"Изображение продавца {self.uploaded_by.email}"
