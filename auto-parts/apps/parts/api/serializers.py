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
        fields = "__all__"
        read_only_fields = ["seller", "rating"]
