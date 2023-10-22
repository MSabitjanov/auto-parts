from rest_framework.serializers import ModelSerializer

from apps.review.models import MasterReview, AutoPartsReview


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = MasterReview
        fields = (
            "user",
            "reviewed_object",
            "comment",
            "rating",
            "created_at",
        )
        read_only_fields = ("user", "created_at", "rating")


class AutoPartsReviewSerializer(ModelSerializer):
    class Meta:
        model = AutoPartsReview
        fields = (
            "user",
            "reviewed_object",
            "comment",
            "rating",
            "created_at",
        )
        read_only_fields = ("user", "created_at", "rating")
