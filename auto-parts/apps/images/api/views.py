from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets, mixins

from apps.images.models import AutoPartsImages, MasterImages
from apps.core.api.api_permissions import IsAutoPartOwnerOrReadOnly

from .serializers import MasterImagesSerializer, AutoPartsImagesSerializer


class ImageViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Custom ViewSet для изображений, без ListView
    """

    pass


class MasterImagesViewSet(ImageViewSet):
    """
    ViewSet для изображений мастеров.
    """

    queryset = MasterImages.objects.all()
    serializer_class = MasterImagesSerializer


class AutoPartsImagesViewSet(ImageViewSet):
    """
    ViewSet для изображений автозапчастей.
    """

    queryset = AutoPartsImages.objects.all()
    serializer_class = AutoPartsImagesSerializer
    permission_classes = [IsAutoPartOwnerOrReadOnly]
