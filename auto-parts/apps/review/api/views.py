from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from apps.review.models import MasterReview, AutoPartsReview
from apps.core.api.api_permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .serializers import MasterReviewSerializer, AutoPartsReviewSerializer


class BaseReviewViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def validate_review_data(self, serializer):
        rating = serializer.validated_data.get("rating", 0)
        comment = serializer.validated_data.get("comment", None)

        if rating == 0 and comment is None:
            raise serializers.ValidationError("You must provide rating or comment")

        if rating not in range(0, 6):
            raise serializers.ValidationError("Rating must be in range 1-5")

    def get_queryset(self):
        return super().get_queryset().filter(active=True)

    def perform_create(self, serializer):
        self.validate_review_data(serializer)

        review = (
            self.get_queryset()
            .filter(
                user=self.request.user,
                reviewed_object=serializer.validated_data["reviewed_object"],
            )
            .first()
        )
        if review:
            serializer.update(review, serializer.validated_data)
        else:
            serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.perform_soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MasterReviewViewSet(BaseReviewViewSet):
    queryset = MasterReview.objects.all()
    serializer_class = MasterReviewSerializer


class AutoPartsReviewViewSet(BaseReviewViewSet):
    queryset = AutoPartsReview.objects.all()
    serializer_class = AutoPartsReviewSerializer
