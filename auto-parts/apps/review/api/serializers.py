from rest_framework.serializers import ModelSerializer

from apps.review.models import MasterReview, AutoPartsReview


class MasterReviewSerializer(ModelSerializer):
    class Meta:
        model = MasterReview
        fields = (
            "id",
            "user",
            "reviewed_object",
            "comment",
            "rating",
            "created_at",
        )
        read_only_fields = (
            "user",
            "created_at",
        )


class AutoPartsReviewSerializer(ModelSerializer):
    class Meta:
        model = AutoPartsReview
        fields = (
            "id",
            "user",
            "reviewed_object",
            "comment",
            "rating",
            "created_at",
        )
        read_only_fields = (
            "user",
            "created_at",
        )
