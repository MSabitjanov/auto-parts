from django.db import models

from django.contrib.auth.models import AbstractUser
from mptt.models import MPTTModel, TreeForeignKey


class User(AbstractUser):
    username = None
    profile_image = models.ImageField(upload_to="profile_images", blank=True)
    wishlist_master = models.ManyToManyField("users.Master", blank=True)
    wishlist_parts = models.ManyToManyField("parts.AutoParts", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"Пользователь {self.email}"


class MasterSkill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Специализация {self.name}"


class Region(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return f"Регион {self.name}"


class Master(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name="Пользователь")
    date_of_birth = models.DateField(blank=True, null=True,  verbose_name="Дата рождения")
    start_of_carrier = models.DateField(blank=True, null=True verbose_name="Начало карьеры", help_text="Нужен для подсчета опыта работы мастера")
    skilled_at = models.ManyToManyField(MasterSkill, verbose_name="Специализация мастера", related_name="masters")
    last_visited = models.DateTimeField(auto_now=True, verbose_name="Последнее посещение")
    date_of_join = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Номер телефона")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_recommended = models.BooleanField(default=False, verbose_name="Рекомендованный")
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Регион", related_name="masters")
    location = models.PointField(blank=True, null=True, verbose_name="Местоположение")

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

    def __str__(self):
        return f"Мастер {self.user.email}"


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name="Пользователь")
    company_name = models.CharField(max_length=50, blank=True, verbose_name="Название компании")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Регион", related_name="sellers")
    company_phone = models.CharField(max_length=20, blank=True, verbose_name="Номер телефона")
    website = models.URLField(blank=True, verbose_name="Сайт")
    working_hours = models.JSONField(default="default_working_hours", verbose_name="Рабочие часы")
    seller_phone = models.CharField(max_length=20, blank=True, verbose_name="Номер телефона продавца")
    company_info = models.TextField(blank=True, verbose_name="Информация о компании")
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг")
    date_of_join = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    location = models.PointField(blank=True, null=True, verbose_name="Местоположение")

    class Meta:
        verbose_name = "Продавец"
        verbose_name_plural = "Продавцы"

    def __str__(self):
        return f"Продавец {self.user.email}"
    
    @classmethod
    def default_working_hours(cls):
        week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        working_hours = [
            {
                "day": day,
                "is_open": False,
                "hours": [{"start": "00:00", "end": "00:00"}]
            } 
            for day in week_days
        ]
        return working_hours
