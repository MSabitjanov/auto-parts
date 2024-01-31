import os
from django.db import models
from django.contrib.gis.db import models as geomodels
from django.utils.timezone import now

# from django.contrib.gis.db import models as geomodels
from django.contrib.auth.models import AbstractUser
from mptt.models import MPTTModel, TreeForeignKey

from .utils import default_working_hours
from .managers import CustomUserManager


def get_upload_path(instance, filename):
    return os.path.join("account/avatars/", now().date().strftime("%Y/%m/%d"), filename)


class User(AbstractUser):
    username = None
    email = models.EmailField("Email адресс", unique=True)
    phone_number = models.CharField("Номер телефона", max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to=get_upload_path, blank=True)
    wishlist_master = models.ManyToManyField(
        "users.Master", blank=True, related_name="wishlist_master"
    )
    wishlist_parts = models.ManyToManyField(
        "parts.AutoParts", blank=True, related_name="wishlist_auto_parts"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активный")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"Пользователь {self.email}"

    def perform_soft_delete(self):
        self.is_active = False
        self.save()


class MasterSkill(MPTTModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родительская специализация",
        help_text="Родительская специализация мастера",
    )

    class Meta:
        verbose_name = "Специализация мастера"
        verbose_name_plural = "Специализации мастеров"

    def __str__(self):
        return f"Специализация {self.name}"


class Region(MPTTModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Регион",
        help_text="Регион, в котором находится район",
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

    def __str__(self):
        return f"Регион {self.name}"


class Master(geomodels.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Пользователь",
    )
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name="Дата рождения"
    )
    start_of_carrier = models.DateField(
        blank=True,
        null=True,
        verbose_name="Начало карьеры",
        help_text="Нужен для подсчета опыта работы мастера",
    )
    skilled_at = models.ManyToManyField(
        MasterSkill,
        verbose_name="Специализация мастера",
        related_name="masters",
        blank=True,
    )
    last_visited = models.DateTimeField(
        auto_now=True, verbose_name="Последнее посещение"
    )
    date_of_join = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )
    phone_number = models.CharField(
        max_length=20, blank=True, verbose_name="Номер телефона"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    is_recommended = models.BooleanField(default=False, verbose_name="Рекомендованный")
    website = models.URLField(null=True, blank=True, verbose_name="Сайт")
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг")
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Регион",
        related_name="masters",
    )
    address = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Адрес"
    )
    company_name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Название Компании"
    )
    location = geomodels.PointField(blank=True, null=True, verbose_name="Местоположение")

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

    def __str__(self):
        return f"Мастер {self.user.email}"


class Seller(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, verbose_name="Пользователь"
    )
    company_name = models.CharField(
        max_length=50, blank=True, verbose_name="Название компании"
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Регион",
        related_name="sellers",
    )
    company_phone = models.CharField(
        max_length=20, blank=True, verbose_name="Номер телефона компании"
    )
    website = models.URLField(blank=True, verbose_name="Сайт")
    working_hours = models.JSONField(
        default=default_working_hours, verbose_name="Рабочие часы"
    )
    seller_phone = models.CharField(
        max_length=20, blank=True, verbose_name="Номер телефона продавца"
    )
    company_info = models.TextField(blank=True, verbose_name="Информация о компании")
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг")
    date_of_join = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )
    seller_images = models.ManyToManyField(
        "images.SellerImage", blank=True, related_name="sellers"
    )
    location = geomodels.PointField(blank=True, null=True, verbose_name="Местоположение")

    class Meta:
        verbose_name = "Продавец"
        verbose_name_plural = "Продавцы"

    def __str__(self):
        return f"Продавец {self.user.email}"
