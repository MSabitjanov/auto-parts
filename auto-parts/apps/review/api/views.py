from rest_framework.viewsets import ModelViewSet

from apps.review.models import MasterReview, AutoPartsReview
from apps.core.api.api_permissions import IsOwnerOrReadOnly

from .serializers import ReviewSerializer


class MasterReviewViewSet(ModelViewSet):
    queryset = MasterReview.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AutoPartsReviewViewSet(ModelViewSet):
    queryset = AutoPartsReview.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
