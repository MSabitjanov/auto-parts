from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


from apps.users.models import User, MasterSkill, Region, Master, Seller
from apps.core.api.api_permissions import IsOwnerOrReadOnly

from .serializers import (
    MasterSerializer,
    SellerSerializer,
    UserSerializer,
    MasterSkillSerializer,
    RegionSerializer,
    EmailAuthTokenSerializer,
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


class MasterBySkillListAPIView(ListAPIView):
    serializer_class = MasterSerializer

    def get_queryset(self):
        skill_id = self.kwargs.get("skill_id")
        skill = MasterSkill.objects.get(id=skill_id)
        descendants = skill.get_descendants(include_self=True)
        return Master.objects.filter(skilled_at__in=descendants)


class SellerViewSet(ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        if Seller.objects.filter(user=user).exists():
            raise ValidationError("You already have a seller profile")
        serializer.save(user=self.request.user)


class CustomObtainAuthToken(ObtainAuthToken):
    """
    Custom view to obtain a token by providing email and password.
    """

    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
