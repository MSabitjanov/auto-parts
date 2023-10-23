from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from apps.parts.models import AutoPartsCategory, Brand, AutoParts
from apps.core.api.api_permissions import IsOwnerOrReadOnly, IsSellerOrReadOnly

from .serializers import (
    AutoPartsCategorySerializer,
    BrandSerializer,
    AutoPartSerializer,
)


class AutoPartsCategoryListAPIView(ListAPIView):
    queryset = AutoPartsCategory.objects.all()
    serializer_class = AutoPartsCategorySerializer


class BrandListAPIView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class AutoPartViewSet(ModelViewSet):
    queryset = AutoParts.objects.all()
    serializer_class = AutoPartSerializer
    permission_classes = [IsSellerOrReadOnly]
