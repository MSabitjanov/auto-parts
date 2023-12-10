from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from django.contrib.auth import authenticate

from apps.users.models import User, MasterSkill, Region, Master, Seller


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = "is_superuser", "is_staff", "groups", "user_permissions"
        extra_kwargs = {
            "password": {"write_only": True},
            "is_active": {"read_only": True},
        }


class UserSerializerForChat(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")


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


class RegionSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = "id", "name", "parent"


class MasterSerializer(ModelSerializer):
    skilled_at = MasterSkillSerializer(many=True)
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
            return obj.images.first().image.url
        return None


class SellerSerializer(ModelSerializer):
    class Meta:
        model = Seller
        fields = "__all__"
        read_only_fields = ("user", "date_of_join", "rating")


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
