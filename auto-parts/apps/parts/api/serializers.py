from rest_framework import serializers

from apps.parts.models import AutoPartsCategory, Brand, AutoParts


class AutoPartsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoPartsCategory
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class AutoPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoParts
        read_only_fields = ["seller", "rating", "is_active"]
        fields = "__all__"
        # exclude = ("is_active",)
        extra_kwargs = {"is_new": {"required": True}}
        # extra_kwargs = {"brand": {"required": True}, "category": {"required": True}}
