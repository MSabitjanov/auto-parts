from rest_framework import serializers

from apps.parts.models import AutoPartsCategory, Brand, AutoParts
from apps.images.api.serializers import AutoPartsImagesSerializer
from apps.parts.utils import normalize_brand_name

class RecursivePartCategorySerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

    class Meta:
        ref_name = "RecursivePartSerializer"


class FilterCommentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class AutoPartsCategorySerializer(serializers.ModelSerializer):
    children = RecursivePartCategorySerializer(many=True)

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = AutoPartsCategory
        fields = "id", "name", "children"


class AutoPartListCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoPartsCategory
        fields = "id", "name", "parent"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class AutoPartSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=AutoPartsCategory.objects.all(), required=False)
    company_name = serializers.CharField(source="seller.company_name", read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = AutoParts
        read_only_fields = ["seller", "rating", "is_active"]
        fields = (
            "id",
            "category",
            "brand",
            "seller",
            "company_name",
            "name",
            "description",
            "characteristics",
            "is_new",
            "price",
            "date_of_pubication",
            "last_updated",
            "rating",
            "image_url",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = AutoPartsCategorySerializer(instance.category).data
        return representation

    def create(self, validated_data):
        brand_name = validated_data.pop("brand").get("name") if "brand" in validated_data else None

        if brand_name:
            noramlized_brand_name = normalize_brand_name(brand_name)
            brand, created = Brand.objects.get_or_create(name=noramlized_brand_name)
            validated_data["brand"] = brand

        auto_part = AutoParts.objects.create(**validated_data)
        return auto_part

    def get_image_url(self, obj):
        if obj.images.exists():
            return [image.image.url for image in obj.images.all()]
        return None
