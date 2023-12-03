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


class MasterSkillSerializer(ModelSerializer):
    class Meta:
        model = MasterSkill
        fields = "id", "name", "parent"


class RegionSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = "id", "name", "parent"


class MasterSerializer(ModelSerializer):
    class Meta:
        model = Master
        fields = "__all__"
        read_only_fields = (
            "user",
            "is_recommeded",
            "rating",
            "last_visited",
            "date_of_join",
        )


class SellerSerializer(ModelSerializer):
    class Meta:
        model = Seller
        fields = "__all__"
        read_only_fields = ("user", "date_of_join", "rating")


class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
