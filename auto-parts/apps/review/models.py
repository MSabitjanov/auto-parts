from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import F

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
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        review_statistics, created = ReviewStatistics.objects.get_or_create(master_review=self.reviewed_object)
        review_statistics.update_review_statistics(self, created)


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
    
    def save(self, *args, **kwargs):
        original_rating = 0
        if self.pk:
            original_rating = AutoPartsReview.objects.get(pk=self.pk).rating
        super().save(*args, **kwargs)
        review_statistics, created = ReviewStatistics.objects.get_or_create(auto_parts_review=self.reviewed_object)
        review_statistics.update_review_statistics(self, created, original_rating)


class ReviewStatistics(models.Model):
    master_review = models.ForeignKey(Master, on_delete=models.CASCADE, null=True, blank=True, related_name="review_statistics")
    auto_parts_review = models.ForeignKey(AutoParts, on_delete=models.CASCADE, null=True, blank=True, related_name="review_statistics")
    total_review_numbers = models.PositiveIntegerField(default=0)
    total_review_score = models.PositiveIntegerField(default=0)
    
    @property
    def average_rating(self):
        if self.total_review_numbers:
            return round(self.total_review_score / self.total_review_numbers, 1)
        else:
            return 0
    
    def update_review_statistics(self, review, created, original_rating):
        if created:
            self.total_review_numbers += 1
            self.total_review_score += review.rating
        else:
            self.total_review_score = self.total_review_score - original_rating + review.rating

        if isinstance(review, MasterReview):
            self.master_review = review.reviewed_object
            self.master_review.rating = self.average_rating
            self.master_review.save()
        elif isinstance(review, AutoPartsReview):
            self.auto_parts_review = review.reviewed_object
            self.auto_parts_review.rating = self.average_rating
            self.auto_parts_review.save()
        else:
            raise ValueError("Invalid review type")

        self.save()