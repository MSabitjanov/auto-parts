from rest_framework.serializers import ModelSerializer

from apps.users.models import User, MasterSkill, Region, Master, Seller

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}