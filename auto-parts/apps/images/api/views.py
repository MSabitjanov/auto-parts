from rest_framework import viewsets, mixins, serializers
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.images.models import AutoPartsImages, MasterImages, SellerImage
from apps.core.api.api_permissions import IsAutoPartOwnerOrReadOnly, IsMasterOrReadOnly

from .serializers import MasterImagesSerializer, AutoPartsImagesSerializer, SellerImagesSerializer


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
    permission_classes = [IsMasterOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(master=self.request.user.master)


class AutoPartsImagesViewSet(ImageViewSet):
    """
    ViewSet для изображений автозапчастей.
    """

    queryset = AutoPartsImages.objects.all()
    serializer_class = AutoPartsImagesSerializer
    permission_classes = [IsAutoPartOwnerOrReadOnly]


class SellerImagesCreateRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView, CreateAPIView):
    """
    View для изображений продавцов.
    """
    queryset = SellerImage.objects.all()
    serializer_class = SellerImagesSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        image = SellerImage.objects.filter(uploaded_by=self.request.user).first()
        return image
    
    def perform_create(self, serializer):
        user = self.request.user
        if SellerImage.objects.filter(uploaded_by=user).exists():
            raise serializers.ValidationError("У вас уже есть изображение продавца")
        serializer.save(uploaded_by=self.request.user)

