from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import mixins

from django.db.models import Avg
from django.contrib.gis.geos import fromstr

from apps.users.models import User, MasterSkill, Region, Master, Seller
from apps.core.api.api_permissions import IsOwnerOrReadOnly

from .serializers import (
    MasterListSerializer,
    MasterSerializer,
    MasterReadSerializer,
    SellerSerializer,
    UserSerializer,
    MasterSkillSerializer,
    RegionSerializer,
    EmailAuthTokenSerializer,
    MasterSkillSerializerAll,
)


class UserViewSet(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.perform_soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MasterSkillListAPIView(ListAPIView):
    queryset = MasterSkill.objects.all()
    serializer_class = MasterSkillSerializer


class MasterSkillListAllAPIView(ListAPIView):
    queryset = MasterSkill.objects.all()
    serializer_class = MasterSkillSerializerAll


class RegionListAPIView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class CustomMasterModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):

    pass


class MasterViewSet(CustomMasterModelViewSet):
    """
    Serves all methods except list.
    """
    queryset = Master.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MasterReadSerializer
        return MasterSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if Master.objects.filter(user=user).exists():
            raise ValidationError("You already have a master profile")
        latitude = self.request.data.get('latitude', None)
        longitude = self.request.data.get('longitude', None)

        # Check if both latitude and longitude are provided
        if latitude is not None and longitude is not None:
            # Create a Point object from the latitude and longitude
            location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
            serializer.save(user=user, location=location)
        else:
            serializer.save(user=user)
    
    def perform_update(self, serializer):
        latitude = self.request.data.get('latitude', None)
        longitude = self.request.data.get('longitude', None)

        # Check if both latitude and longitude are provided
        if latitude is not None and longitude is not None:
            # Create a Point object from the latitude and longitude
            location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
            serializer.save(location=location)
        else:
            serializer.save()


class MasterListAPIView(ListAPIView):
    queryset = Master.objects.all()
    serializer_class = MasterListSerializer

    def get_queryset(self):
        queryset = Master.objects.annotate(average_rating=Avg('master_reviews__rating'))
        return queryset.order_by('-average_rating')


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
        latitude = self.request.data.get('latitude', None)
        longitude = self.request.data.get('longitude', None)

        # Check if both latitude and longitude are provided
        if latitude is not None and longitude is not None:
            # Create a Point object from the latitude and longitude
            location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
            serializer.save(user=user, location=location)
        else:
            serializer.save(user=user)
    
    def perform_update(self, serializer):
        latitude = self.request.data.get('latitude', None)
        longitude = self.request.data.get('longitude', None)

        # Check if both latitude and longitude are provided
        if latitude is not None and longitude is not None:
            # Create a Point object from the latitude and longitude
            location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
            serializer.save(location=location)
        else:
            serializer.save()


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
