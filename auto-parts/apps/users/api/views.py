from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from apps.users.models import User, MasterSkill, Region, Master, Seller
from apps.core.api.api_permissions import IsOwnerOrReadOnly

from .serializers import (
    MasterSerializer,
    SellerSerializer,
    UserSerializer,
    MasterSkillSerializer,
    RegionSerializer,
)


class UserViewSet(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.perform_soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MasterSkillListAPIView(ListAPIView):
    queryset = MasterSkill.objects.all()
    serializer_class = MasterSkillSerializer


class RegionListAPIView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class MasterViewSet(ModelViewSet):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        if Master.objects.filter(user=user).exists():
            raise ValidationError("You already have a master profile")
        serializer.save(user=self.request.user)


class SellerViewSet(ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        if Seller.objects.filter(user=user).exists():
            raise ValidationError("You already have a seller profile")
        serializer.save(user=self.request.user)
