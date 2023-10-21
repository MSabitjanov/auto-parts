from rest_framework.serializers import ModelSerializer

from apps.users.models import User, MasterSkill, Region, Master, Seller


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = "is_superuser", "is_staff", "groups", "user_permissions"
        extra_kwargs = {
            "password": {"write_only": True},
            "is_active": {"read_only": True},
        }


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
