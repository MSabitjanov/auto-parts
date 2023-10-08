from django.db import models

from mptt.models import MPTTModel
from taggit.managers import TaggableManager

from apps.users.models import Seller


class AutoPartsCategory(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родительская категория",
        help_text="Если это родительская категория, то оставьте это поле пустым.",
    )
    characteristics = TaggableManager(
        help_text="Введите характеристики через запятую(Например, если это шина, то радиус, ширина, высота. Если это двигатель, то объем, мощность, тип. )",
        verbose_name="Характеристики",
    )

    class Meta:
        verbose_name = "Категория автозапчастей"
        verbose_name_plural = "Категории автозапчастей"

    def __str__(self):
        return f"Категория {self.name}"


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название бренда")

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return f"Бренд {self.name}"


class AutoParts(models.Model):
    """
    This model is used to store information about auto parts.
    Characteristics field is used to store additional information about auto parts,
    for example, engine type, engine volume in json format.
    This information will be taken form characteristics field in Category model.
    """

    category = models.ForeignKey(
        AutoPartsCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
        related_name="parts",
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Бренд",
        related_name="parts",
    )
    seller = models.ForeignKey(
        Seller, on_delete=models.SET_NULL, null=True, verbose_name="Продавец"
    )
    is_new = models.BooleanField(default=True, verbose_name="Новый")
    price = models.PositiveIntegerField(verbose_name="Цена")
    description = models.TextField(blank=True, verbose_name="Описание")
    characteristics = models.JSONField(
        blank=True, null=True, verbose_name="Дополнительные атрибуты"
    )
    date_of_pubication = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации"
    )
    last_updated = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг")

    class Meta:
        verbose_name = "Автозапчасть"
        verbose_name_plural = "Автозапчасти"

    def __str__(self):
        return f"Автозапчасть {self.brand.name} {self.category.name}"
