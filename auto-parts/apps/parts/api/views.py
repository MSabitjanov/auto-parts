from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from apps.parts.models import AutoPartsCategory, Brand, AutoParts
from apps.core.api.api_permissions import IsOwnerOrReadOnly, IsSellerOrReadOnly

from .serializers import (
    AutoPartsCategorySerializer,
    BrandSerializer,
    AutoPartSerializer,
)


class AutoPartsCategoryListAPIView(ListAPIView):
    queryset = AutoPartsCategory.objects.prefetch_related("children")
    serializer_class = AutoPartsCategorySerializer


class AutoPartByCategory(ListAPIView):
    serializer_class = AutoPartSerializer

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        category = AutoPartsCategory.objects.get(id=category_id)
        descendants = category.get_descendants(include_self=True)
        return AutoParts.objects.filter(category__in=descendants)


class BrandListAPIView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class AutoPartViewSet(ModelViewSet):
    queryset = AutoParts.objects.all()
    serializer_class = AutoPartSerializer
    permission_classes = [IsSellerOrReadOnly]

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.perform_soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.seller, is_active=True)


class SellerAutoParts(ListAPIView):
    serializer_class = AutoPartSerializer

    def get_queryset(self):
        seller_id = self.kwargs.get("seller_id")
        return AutoParts.objects.filter(seller_id=seller_id)