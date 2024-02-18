from rest_framework.serializers import ModelSerializer, ValidationError

from apps.review.models import MasterReview, AutoPartsReview

class MasterReviewSerializer(ModelSerializer):
    from apps.users.api.serializers import UserSerializerForChat
    
    user = UserSerializerForChat(read_only=True)

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
    
    def validate_rating(self, value):
        if value not in range(1, 6):
            raise ValidationError("Rating must be in range 1-5")
        return value


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

    def validate_rating(self, value):
        if value not in range(1, 6):
            raise ValidationError("Rating must be in range 1-5")
        return value