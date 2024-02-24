from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from apps.users.models import User, MasterSkill, Region, Master, Seller
from apps.images.api.serializers import SellerImagesSerializer, MasterImagesSerializer


class MasterSerializerForWishlist(ModelSerializer):
    class Meta:
        model = Master
        fields = "__all__"

class UserSerializer(ModelSerializer):
    
    is_seller = serializers.SerializerMethodField()
    is_master = serializers.SerializerMethodField()
    wishlist_master = MasterSerializerForWishlist(many=True, read_only=True)

    class Meta:
        model = User
        exclude = "is_superuser", "is_staff", "groups", "user_permissions"
        extra_kwargs = {
            "password": {"write_only": True},
            "is_active": {"read_only": True},
        }

    def get_is_seller(self, obj):
        return hasattr(obj, "seller")

    def get_is_master(self, obj):
        return hasattr(obj, "master")


class UserSerializerForChat(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "profile_image")


class RecursiveMasterSkillSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterMasterSkillSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class MasterSkillSerializer(ModelSerializer):
    children = RecursiveMasterSkillSerializer(many=True)

    class Meta:
        list_serializer_class = FilterMasterSkillSerializer
        model = MasterSkill
        fields = "id", "name", "children"


class MasterSkillSerializerAll(ModelSerializer):
    class Meta:
        model = MasterSkill
        fields = "id", "name"


class RegionRecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterRegionSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RegionSerializer(ModelSerializer):
    children = RegionRecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterRegionSerializer
        model = Region
        fields = "id", "name", "children"


class MasterSerializer(ModelSerializer):
    """
    Serializer for master profile. Serves all methods except list.
    """
    skilled_at = serializers.PrimaryKeyRelatedField(
        queryset=MasterSkill.objects.all(),
        many=True,
        required=False,
    )
    master_name = serializers.CharField(source="user.get_full_name", read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Master
        fields = "__all__"
        read_only_fields = (
            "user",
            "is_recommeded",
            "rating",
            "last_visited",
            "date_of_join",
            "image_url",
        )

    def get_image_url(self, obj):
        if obj.images.exists():
            return [image.image.url for image in obj.images.all()]
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['skilled_at'] = MasterSkillSerializerAll(instance.skilled_at.all(), many=True).data
        return representation

    
class MasterReadSerializer(ModelSerializer):
    """
    Serializer for master profile. Serves all methods except list.
    """
    from apps.review.api.serializers import MasterReviewSerializer

    user = UserSerializer()
    skilled_at = MasterSkillSerializerAll(many=True, read_only=True)
    master_name = serializers.CharField(source="user.get_full_name", read_only=True)
    image_url = serializers.SerializerMethodField()
    reviews = MasterReviewSerializer(many=True, read_only=True, source="master_reviews")
    region = RegionSerializer()

    class Meta:
        model = Master
        fields = "__all__"
        read_only_fields = (
            "user",
            "is_recommeded",
            "rating",
            "last_visited",
            "date_of_join",
            "image_url",
        )

    def get_image_url(self, obj):
        if obj.images.exists():
            images_data = []
            for image in obj.images.all():
                image_data = {
                    "id": image.id,
                    "url": image.image.url,
                }
                images_data.append(image_data)
            return images_data
        return None


class MasterListSerializer(ModelSerializer):
    """
    Serializer for master profile. Serves only list method.
    """

    skilled_at = MasterSkillSerializerAll(many=True, read_only=True)
    master_name = serializers.CharField(source="user.get_full_name", read_only=True)
    image_url = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    region = RegionSerializer()

    class Meta:
        model = Master
        fields = "__all__"
        read_only_fields = (
            "user",
            "is_recommeded",
            "rating",
            "reviews_count",
            "last_visited",
            "date_of_join",
            "image_url",
        )

    def get_image_url(self, obj):
        if obj.images.exists():
            return obj.images.first().image.url
        return None

    def get_reviews_count(self, obj):
        return obj.master_reviews.count()

    
class SellerSerializer(ModelSerializer):
    seller_images = SellerImagesSerializer(many=True, read_only=True)
    user = UserSerializer()
    region = RegionSerializer()

    class Meta:
        model = Seller
        fields = "__all__"
        read_only_fields = ("user", "date_of_join", "rating")


class SellerCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Seller
        fields = "__all__"
        read_only_fields = ("user", "date_of_join", "rating")
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation


class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )

            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
