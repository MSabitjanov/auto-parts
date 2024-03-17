from rest_framework import serializers
from .serializers import UserSerializer

from apps.users.models import Master, Seller
from apps.parts.models import AutoParts, AutoPartsCategory, Brand
from apps.parts.api.serializers import AutoPartsCategorySerializer, BrandSerializer
from apps.users.api.serializers import RegionSerializer, MasterSkillSerializer, SellerSerializer

class MasterSerializerForWishlist(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    skilled_at = MasterSkillSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Master
        fields = "__all__"

    def get_image_url(self, obj):
        if obj.images.exists():
            return [image.image.url for image in obj.images.all()]
        return None

class SellerSerializerForWishlist(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    class Meta:
        model = Seller
        fields = "__all__"


class AutoPartSerializerForWishlist(serializers.ModelSerializer):
    seller = SellerSerializerForWishlist(read_only=True)
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all()) 
    category = serializers.PrimaryKeyRelatedField(
        queryset=AutoPartsCategory.objects.all(), required=False
    )
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = AutoParts
        fields = "__all__"
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["category"] = AutoPartsCategorySerializer(instance.category).data
        representation["brand"] = BrandSerializer(instance.brand).data
        return representation

    def get_image_url(self, obj):
        if obj.images.exists():
            image_urls = []
            for image in obj.images.all():
                image_data = {"id": image.id, "image_url": image.image.url}
                image_urls.append(image_data)
            return image_urls
        return None

class UserSerializerForProfile(UserSerializer):
    wishlist_master = MasterSerializerForWishlist(many=True, read_only=True)
    wishlist_parts = AutoPartSerializerForWishlist(many=True, read_only=True)