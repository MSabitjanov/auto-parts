from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from apps.parts.models import AutoPartsCategory, Brand, AutoParts
from apps.core.api.api_permissions import IsOwnerOrReadOnly, IsSellerOrReadOnly
from apps.images.models import AutoPartsImages

from .serializers import (
    AutoPartListCategorySerializer,
    AutoPartsCategorySerializer,
    BrandSerializer,
    AutoPartSerializer,
    AutoPartDetailSerializer,
)


class AutoPartsCategoryListAPIView(ListAPIView):
    """
    Для рекурсивного вывода категорий
    """
    queryset = AutoPartsCategory.objects.prefetch_related("children")
    serializer_class = AutoPartsCategorySerializer


class AutoPartCategoriesListAPIView(ListAPIView):
    """
    Для вывода категорий без рекурсии
    """
    queryset = AutoPartsCategory.objects.all()
    serializer_class = AutoPartListCategorySerializer


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
    detail_serializer_class = AutoPartDetailSerializer
    permission_classes = [IsSellerOrReadOnly]

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.perform_soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        auto_part_instance = serializer.save(seller=self.request.user.seller, is_active=True)
        auto_part_id = auto_part_instance.id
        images = self.request.data.getlist("images")
        if images:
            for image in images:
                AutoPartsImages.objects.create(auto_part_id=auto_part_id, image=image)

class SellerAutoParts(ListAPIView):
    serializer_class = AutoPartSerializer

    def get_queryset(self):
        seller_id = self.kwargs.get("seller_id")
        return AutoParts.objects.filter(seller_id=seller_id)
    
    
class SearchAutoPart(ListAPIView):
    serializer_class = AutoPartSerializer

    def get_queryset(self):
        query = self.request.query_params.get("query")
        return AutoParts.objects.filter(name__icontains=query)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)